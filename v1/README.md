# oauth-lab

Laboratorio de Authenticação

- Requisitos:

  - Docker
  - VSCode
    - plugin plantuml
  - Noções:
    - API Gateway: [Kong](https://docs.konghq.com/hub/?category=authentication)
    - OAuth Server: [Keycloak](https://www.keycloak.org/)
    - [Hashicorp Vault](https://www.vaultproject.io/)

## OAuth - Autorization Code

Metodo utilizando OpenID (OAuth 2.0) com Keycloak

Traz a segurança de rapida rotação, porém uma complexidade alta de implementação, e a dependencia de requisições cruzadas, que tende a gerar um impacto em performance das requisições


## Token Admin

Em uma discussão com um usuario surgiu a ideia de uma abordagem da gestão de dois tokens para cada consumer, o que permite a rotação controlada, e expiração das imagens antigas.

A proposta é um Tool Token Admin que:
- Gera um novo token
- Registra um token no Provider Secrets 
- Replica nos Consumer Secrets
- Notifica o SRE para rebuild
- Expira o token anterior apos o tempo definido
- Notifica o SRE para ciência

O papel do Provider:
- Manter 2 tokens para cada Consumer
- Validar a requisição recebida
- Fazer refresh de segredos quando requisitado
- Remover o token expirado da autenticação

O papel do Consumer
- Enviar o Token configurado a cada requisição

O papel do Consumer tem variações para segredo estático ou dinâmico

### Consumer com segredo estático

Para este cenário será necessário restart ou redeploy para troca do segredo.

Existe a dependência do SRE Team, que garantirá o rebuild na frequencia definida.

O restart do serviço não deve gerar indisponibilidade.

### Consumer com segredo dinâmico

Em caso de consumers que atuam como serviços é relevante usar um endpoint para releitura do segredo atualizado, que deve ser cacheado para não inserir ônus de performance.

O reload de segredo pode dispensar autenticação, desde que exista um throtling e/ou range de origem definido, para coibir abusos externos.

 Ex: 1/minuto
     Requisicao do range: 10.184.0.0/16

