# API Gateway

This is a proof-of-concept for an
infrastructure design to be used
in Drizm infrastructure.

## Objectives

The objectives of this
Proof-of-Concept are to provide a
platform to build language-agnostic
distributed services on.

The objectives are as follows:  
- HTTP/2 for all services
- Centralized Authn and Authz 
  for all services
- Observability for all services
- Strict but not limiting security
- Ease of debugging and testing

All the above objectives should
optimally be achieved at the lowest
possible maintenance effort,
as to provide as many of the benefits
of distributed systems with as
little of its drawbacks.

The following technologies are
being used:  
- Traefik (Reverse-Proxy / Edge-Router)
- Jaeger (Tracing)
- Elasticsearch, FluentD, Kibana (Logging)
- Prometheus, Cortex (Monitoring)
- JOSE, PASETO (Authn)
- Open Policy Agent (Authz)

## Preparations

```bash
cd ./gateway/certs

# If this is your first time using MkCert
mkcert -install

mkcert fastapi_service
mkcert auth_service
cp "$(mkcert -CAROOT)/rootCA.pem" ../root.pem

mkcert localhost 127.0.0.1 ::1
mv ./localhost+2.pem ./chain.pem
mv ./localhost+2-key.pem ./key.pem
```

## Running

```bash
sudo chmod -R 777 ./gateway
cd docker
docker-compose -p gatewaytest \
    -f docker-compose.yml \
    up --build --force-recreate -V --remove-orphans
```

You can now view the application
at ``https://localhost:10000``.
