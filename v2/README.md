# Laboratório de Autenticação v2 - M2M com Factory Pattern

Este diretório contém uma biblioteca de autenticação agnóstica (`auth_factory.py`) que pode instanciar clientes para Keycloak ou AWS Cognito, focando no fluxo de Machine-to-Machine (M2M) com `client_credentials`.

## Estrutura

- `keycloak.py`: Implementação do cliente de autenticação para o Keycloak.
- `Cognito.py`: Implementação do cliente de autenticação para o AWS Cognito.
- `auth_factory.py`: Ponto de entrada que utiliza o padrão de projeto *Factory* para criar o cliente de autenticação correto com base nos parâmetros.
- `client.py`: Exemplo de como consumir a `auth_factory` para obter tokens de ambos os provedores.
- `keycloak_setup.py`: Script para automatizar a configuração do Keycloak (criação de realm e client).
- `docker-compose.yaml`: Arquivo para subir um ambiente local com Keycloak e um banco de dados MySQL.

---

## Guia de Configuração e Teste com Keycloak

Siga os passos abaixo para configurar um ambiente Keycloak local e testar a autenticação M2M.

### Passo 1: Instalar Dependências

Crie um ambiente virtual e instale as bibliotecas Python necessárias.

```bash
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/macOS:
# source venv/bin/activate

pip install -r requirements.txt
```

### Passo 2: Iniciar o Ambiente Docker

No terminal, na raiz do diretório `v2`, execute o comando para iniciar os contêineres do Keycloak e do banco de dados.

```bash
docker compose up -d
```

Aguarde um ou dois minutos para que os serviços sejam totalmente inicializados.

### Passo 2: Acessar o Console de Administração do Keycloak

1.  Abra seu navegador e acesse: `http://localhost:8080/auth/`
2.  Você será redirecionado para a página de login. Use as credenciais definidas no `docker-compose.yaml`:
    -   **Usuário:** `admin`
    -   **Senha:** `admin`

### Passo 3: Criar um Novo "Realm"

Um *Realm* gerencia um conjunto de usuários, credenciais, roles e clientes.

1.  No canto superior esquerdo, passe o mouse sobre "master" e clique em **Create Realm**.
2.  Digite um nome para o Realm (ex: `my-lab-realm`) e clique em **Create**.

### Passo 4: Criar um "Client" para a Aplicação

O *Client* representará sua aplicação (serviço) que precisa se autenticar.

1.  No menu de navegação à esquerda, certifique-se de que seu novo realm (`my-lab-realm`) está selecionado e clique em **Clients**.
2.  Na página de Clients, clique em **Create client**.
3.  Preencha as informações do cliente:
    -   **Client type**: Deixe como `OpenID Connect`.
    -   **Client ID**: Dê um nome único, por exemplo, `my-m2m-client`.
    -   Clique em **Next**.
4.  Na tela seguinte, configure o cliente para o fluxo M2M:
    -   Ative a opção **Client authentication**.
    -   Desative as opções **Standard flow** e **Direct access grants**.
    -   Clique em **Save**.

### Passo 5: Obter o "Client Secret"

Após salvar, você será redirecionado para a página de detalhes do cliente.

1.  Vá para a aba **Credentials**.
2.  Você verá o **Client secret**. Copie este valor. Ele será usado no seu script Python.

### Passo 6: Configurar e Executar o `client.py`

Agora, vamos usar as informações do Keycloak para testar a autenticação.

1.  Abra o arquivo `v2/client.py`.
2.  Localize a seção `Test Case 1: Keycloak` e atualize o dicionário `keycloak_config` com os dados que você acabou de configurar:

    ```python
    # Define Keycloak config (replace with your actual data)
    keycloak_config = {
        "server_url": "http://localhost:8080/auth", # Use a URL base com /auth
        "realm": "my-lab-realm",                   # O nome do realm que você criou
        "client_id": "my-m2m-client",              # O Client ID que você definiu
        "client_secret": "SEU_CLIENT_SECRET_AQUI"  # O secret que você copiou no passo 5
    }
    ```

3.  Salve o arquivo e execute-o no terminal:

    ```bash
    python client.py
    ```

Se tudo estiver correto, você verá uma saída indicando que a autenticação com o Keycloak foi bem-sucedida e os cabeçalhos de autorização foram gerados.
