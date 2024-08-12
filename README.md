### Nome do Projeto

**Salesforce JWT Authentication Toolkit**

### README.md

```markdown
# Salesforce JWT Authentication Toolkit

🔐 **Um Toolkit para Autenticação JWT com Salesforce** 🔐

Este projeto fornece um conjunto de scripts Python para facilitar a autenticação via JWT com Salesforce. Ele inclui funcionalidades para converter arquivos JKS para PKCS12, PKCS12 para PEM, gerar tokens JWT e obter tokens de acesso da Salesforce.

## 🛠️ Funcionalidades

1. **Converter JKS para PKCS12**: Converte arquivos de armazenamento de chaves JKS para o formato PKCS12.
2. **Converter PKCS12 para PEM**: Converte arquivos PKCS12 para o formato PEM, separando a chave privada e o certificado.
3. **Gerar JWT**: Cria um token JWT usando a chave privada para autenticação.
4. **Obter Token de Acesso**: Envia o JWT para o Salesforce e obtém o token de acesso.

## 🚀 Como Usar

### Requisitos

- Python 3.x
- Biblioteca `cryptography`
- Biblioteca `pyjwt`
- Biblioteca `requests`

### Instalação

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/salesforce-jwt-authentication-toolkit.git
cd salesforce-jwt-authentication-toolkit
```

Instale as dependências:

```bash
pip install cryptography pyjwt requests
```

### Configuração

1. **Configuração do Ambiente Salesforce**:
    - Crie um App conectado no Salesforce e configure-o para permitir autenticação via JWT.
    - Certifique-se de que o usuário está habilitado e que a política de OAuth está ativada.

2. **Configuração dos Arquivos**:
    - Substitua os caminhos e senhas nos parâmetros de configuração no script.

### Execução

Execute o script Python para realizar as conversões e gerar o token JWT:

```bash
python seu_script.py
```

### Exemplo de Saída

```plaintext
===============================
   Resultado da Importação
===============================
Aviso: O alias 'certificado_de_teste_2024' já existe na área de armazenamento de chaves de destino.
      O alias será substituído.

Status da Importação:
   - Alias importado com sucesso: certificado_de_teste_2024

Resumo do Comando de Importação:
   - Entradas importadas com êxito: 1
   - Entradas que falharam ou foram canceladas: 0
===============================
   Conteúdo do Arquivo PEM
===============================

-----BEGIN PRIVATE KEY-----
...
-----END PRIVATE KEY-----
-----BEGIN CERTIFICATE-----
...
-----END CERTIFICATE-----

===============================
   Token JWT Gerado
===============================

eyJhbGciOiJSUzI1NiIsImtpZCI6Ik5UQXhNakF6...
===============================
   Resposta do Token de Acesso
===============================

{
    "access_token": "00D5g00000VbFs4!AQkAQQAy...",
    "token_type": "Bearer",
    "instance_url": "https://cap39-dev-ed.my.salesforce.com",
    "id": "https://login.salesforce.com/id/00D5g00000VbFs4!AQkAQQAy..."
}
```

## 🛠️ Funções do Código

### `convert_jks_to_p12(jks_file, p12_file, store_password)`

Converte um arquivo JKS para PKCS12 usando a ferramenta `keytool`.

**Parâmetros:**
- `jks_file`: Caminho para o arquivo JKS de origem.
- `p12_file`: Caminho para o arquivo PKCS12 de destino.
- `store_password`: Senha do armazenamento de chaves JKS.

### `convert_p12_to_pem(p12_file, pem_file, p12_password)`

Converte um arquivo PKCS12 para o formato PEM, separando a chave privada e o certificado.

**Parâmetros:**
- `p12_file`: Caminho para o arquivo PKCS12 de origem.
- `pem_file`: Caminho para o arquivo PEM de destino.
- `p12_password`: Senha do arquivo PKCS12.

### `generate_jwt(private_key_file, consumer_key, username, audience)`

Gera um token JWT usando a chave privada.

**Parâmetros:**
- `private_key_file`: Caminho para o arquivo PEM contendo a chave privada.
- `consumer_key`: Chave de consumidor.
- `username`: Nome de usuário para o JWT.
- `audience`: URL do público-alvo para o JWT.

**Retorno:**
- Token JWT gerado.

### `get_access_token(token, token_endpoint)`

Envia o token JWT para o endpoint do Salesforce e obtém o token de acesso.

**Parâmetros:**
- `token`: Token JWT a ser enviado.
- `token_endpoint`: URL do endpoint do Salesforce para autenticação.

**Retorno:**
- Resposta JSON do Salesforce contendo o token de acesso.

## 📜 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

## 🔗 Links Úteis

- [Documentação do JWT](https://jwt.io/)
- [Documentação da biblioteca cryptography](https://cryptography.io/)
- [Documentação da biblioteca requests](https://requests.readthedocs.io/)

## 👨‍💻 Contribuições

Contribuições são bem-vindas! Se você quiser colaborar, por favor, envie um pull request ou abra uma issue.

## 💬 Contato

Para mais informações ou dúvidas, entre em contato com [Leonel Dorneles Porto](mailto:leoneldornelesporto@outlook.com.br).

---

🔧 **Tecnologias Utilizadas:**
- Python
- JWT
- PKCS12
- PEM
- Salesforce OAuth

🚀 **Objetivo:**
Facilitar a integração e autenticação entre aplicações e Salesforce usando JWT para autenticação segura e eficiente.
