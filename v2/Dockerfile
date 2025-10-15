# Dockerfile for Keycloak
FROM quay.io/keycloak/keycloak:23.0.6 as builder

WORKDIR /opt/keycloak
RUN kc.sh build

FROM quay.io/keycloak/keycloak:23.0.6
COPY --from=builder /opt/keycloak/lib/quarkus/ /opt/keycloak/lib/quarkus/
WORKDIR /opt/keycloak
ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]
```

```yaml
# Docker Compose for Keycloak
version: '3.8'

services:
  keycloak:
    build:
      context: .
      dockerfile: Dockerfile
    command: start-dev --import-realm
    environment:
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: admin
      KC_DB: dev-file
    ports:
      - "8080:8080"
    volumes:
      - ./realm-config:/opt/keycloak/data/import
