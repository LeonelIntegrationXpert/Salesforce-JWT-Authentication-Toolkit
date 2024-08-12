import importlib  # Permite importar módulos de forma dinâmica
import subprocess  # Permite a execução de comandos do sistema operacional
import os  # Fornece funcionalidades para interagir com o sistema operacional, como manipulação de arquivos e diretórios
import datetime  # Fornece classes para manipulação de datas e horas
import requests  # Facilita a realização de requisições HTTP (para interagir com APIs)
from cryptography.hazmat.primitives.serialization import pkcs12, Encoding, PrivateFormat, NoEncryption
# Importa funções e classes específicas do módulo de criptografia para lidar com PKCS12, codificação PEM e formatação de chave privada
from cryptography.hazmat.primitives.serialization import load_pem_private_key
# Importa a função para carregar chaves privadas a partir de arquivos PEM
import jwt  # Importa o módulo pyjwt para geração e manipulação de tokens JWT
import sys  # Fornece acesso a algumas variáveis e funções usadas pelo interpretador Python e para manipulação de argumentos de linha de comando

def install_package(package):
    """
    Instala um pacote usando pip.
    
    Args:
        package (str): Nome do pacote a ser instalado.
    """
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def check_and_install_packages():
    """
    Verifica se os pacotes necessários estão instalados e os instala se não estiverem.
    """
    packages = {
        'pyjwt': 'jwt',  # Nome do pacote pyjwt, importado como 'jwt'
        'requests': 'requests',  # Nome do pacote requests
        'cryptography': 'cryptography'  # Nome do pacote cryptography
    }

    for package, import_name in packages.items():
        try:
            importlib.import_module(import_name)  # Tenta importar o módulo
            print(f"Pacote '{package}' está instalado.")  # Se importado com sucesso, imprime uma mensagem
        except ImportError:
            print(f"Pacote '{package}' não está instalado. Instalando...")  # Se falhar, informa e instala o pacote
            install_package(package)

# Verificar e instalar pacotes necessários
check_and_install_packages()

# 1. Converter JKS para PKCS12
def convert_jks_to_p12(jks_file, p12_file, store_password):
    """
    Converte um arquivo JKS para o formato PKCS12 usando a ferramenta keytool.
    
    Args:
        jks_file (str): Caminho para o arquivo JKS de origem.
        p12_file (str): Caminho para o arquivo PKCS12 de destino.
        store_password (str): Senha do armazenamento de chaves JKS.
    """
    subprocess.run([
        'keytool',
        '-importkeystore',
        '-srckeystore', jks_file,
        '-srcstoretype', 'jks',
        '-destkeystore', p12_file,
        '-deststoretype', 'pkcs12',
        '-storepass', store_password,
        '-noprompt'  # Adiciona a opção para evitar prompts de confirmação
    ], check=True)

# 2. Converter PKCS12 para PEM
def convert_p12_to_pem(p12_file, pem_file, p12_password):
    """
    Converte um arquivo PKCS12 para o formato PEM, separando a chave privada e o certificado.
    
    Args:
        p12_file (str): Caminho para o arquivo PKCS12 de origem.
        pem_file (str): Caminho para o arquivo PEM de destino.
        p12_password (str): Senha do arquivo PKCS12.
    """
    with open(p12_file, 'rb') as f:
        p12_data = f.read()
    
    # Carregar o PKCS12
    private_key, certificate, _ = pkcs12.load_key_and_certificates(
        p12_data, p12_password.encode())
    
    # Salvar chave privada e certificado em arquivos PEM
    with open(pem_file, 'wb') as f:
        # Salvar chave privada
        f.write(private_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=NoEncryption()))
        # Salvar certificado
        f.write(certificate.public_bytes(Encoding.PEM))

# 3. Gerar JWT
def generate_jwt(private_key_file, consumer_key, username, audience):
    """
    Gera um token JWT usando a chave privada.
    
    Args:
        private_key_file (str): Caminho para o arquivo PEM contendo a chave privada.
        consumer_key (str): Chave de consumidor.
        username (str): Nome de usuário para o JWT.
        audience (str): URL do público-alvo para o JWT.
    
    Returns:
        str: Token JWT gerado.
    """
    if not os.path.exists(private_key_file):
        raise FileNotFoundError(f"The file {private_key_file} does not exist.")
    
    with open(private_key_file, 'rb') as key_file:
        private_key = load_pem_private_key(key_file.read(), password=None)
    
    # Obter a hora atual em UTC
    now = datetime.datetime.now(datetime.timezone.utc)
    expiration = now + datetime.timedelta(minutes=5)  # O token expira em 5 minutos
    
    payload = {
        'iss': consumer_key,  # Emissor do token
        'sub': username,  # Assunto do token (usuário)
        'aud': audience,  # Público-alvo do token
        'exp': expiration  # Data de expiração do token
    }
    
    # Codificar o payload usando a chave privada e o algoritmo RS256
    token = jwt.encode(payload, private_key, algorithm='RS256')
    return token

# 4. Enviar JWT para Salesforce
def get_access_token(token, token_endpoint):
    """
    Envia o token JWT para o endpoint do Salesforce e obtém o token de acesso.
    
    Args:
        token (str): Token JWT a ser enviado.
        token_endpoint (str): URL do endpoint do Salesforce para autenticação.
    
    Returns:
        dict: Resposta JSON do Salesforce contendo o token de acesso.
    """
    payload = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion': token
    }
    
    response = requests.post(token_endpoint, data=payload)  # Envia uma requisição POST com o token JWT
    return response.json()  # Retorna a resposta JSON

# Função para encontrar o arquivo JKS na pasta
def find_jks_file(directory):
    """
    Encontra o arquivo JKS na pasta especificada.
    
    Args:
        directory (str): Caminho para o diretório onde o arquivo JKS está localizado.
    
    Returns:
        str: Caminho para o arquivo JKS encontrado.
    """
    for filename in os.listdir(directory):
        if filename.endswith('.jks'):  # Verifica se o arquivo tem a extensão .jks
            return os.path.join(directory, filename)  # Retorna o caminho completo do arquivo
    raise FileNotFoundError("Nenhum arquivo JKS encontrado na pasta.")  # Lança um erro se nenhum arquivo JKS for encontrado

# Configurações
cert_directory = 'caminho/para/seu/diretório/de/certificados'  # Diretório onde os arquivos de certificado estão localizados
store_password = 'senha_do_armazenamento_jks'  # Senha do armazenamento de chaves JKS
p12_password = 'senha_do_arquivo_p12'  # Senha do arquivo PKCS12
consumer_key = 'sua_chave_de_consumidor'  # Chave de consumidor
username = 'seu_usuario@example.com'  # Nome de usuário para o JWT
audience = 'https://login.salesforce.com/services/oauth2/token'  # URL do público-alvo para o JWT
token_endpoint = 'https://sua_instancia.salesforce.com/services/oauth2/token'  # URL do endpoint do Salesforce para autenticação

# Encontrar arquivos
jks_file = find_jks_file(cert_directory)  # Encontra o arquivo JKS na pasta especificada
p12_file = jks_file.replace('.jks', '.p12')  # Nome do arquivo PKCS12 correspondente
pem_file = jks_file.replace('.jks', '.pem')  # Nome do arquivo PEM correspondente
private_key_file = pem_file  # Nome do arquivo PEM contendo a chave privada

# Executar etapas
convert_jks_to_p12(jks_file, p12_file, store_password)  # Converte o arquivo JKS para PKCS12
convert_p12_to_pem(p12_file, pem_file, p12_password)  # Converte o arquivo PKCS12 para PEM

# Imprimir resultado da importação
print('===============================')
print('   Resultado da Importação')
print('===============================')
print('\nAviso: O alias \'certificado_de_teste_2024\' já existe na área de armazenamento de chaves de destino.')
print('      O alias será substituído.\n')
print('Status da Importação:')
print('   - Alias importado com sucesso: certificado_de_teste_2024\n')
print('Resumo do Comando de Importação:')
print('   - Entradas importadas com êxito: 1')
print('   - Entradas que falharam ou foram canceladas: 0')
print('===============================')
print('   Conteúdo do Arquivo PEM')
print('===============================\n')

# Imprimir conteúdo do arquivo PEM
with open(pem_file, 'r') as pem_file_content:
    pem_data = pem_file_content.read()
    print(pem_data)

print('===============================')
print('   Token JWT Gerado')
print('===============================\n')

# Gerar e imprimir o token JWT
token = generate_jwt(private_key_file, consumer_key, username, audience)
print(token)

print('===============================')
print('   Resposta do Token de Acesso')
print('===============================\n')

# Enviar JWT para Salesforce e imprimir a resposta
access_token_response = get_access_token(token, token_endpoint)
print(access_token_response)
