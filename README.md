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
- Envoy (Reverse Proxy / Edge Router)
- Elasticsearch, FluentD, Kibana (Logging)
- Prometheus, Cortex (Monitoring)
- JOSE, PASETO (Authn)
- Open Policy Agent (Authz)

## Running

Before you can run this, a
certificate-chain file, and a private
key file for TLS will be expected to
be located at:  
- /gateway/chain.pem
- /gateway/key.pem

If you have mkcert installed,
you can generate them like so:  
```bash
cd gateway
mkcert localhost 127.0.0.1 ::1
```
Now simply rename the files to the
names above.

Run:  
```bash
sudo chmod -R 777 ./gateway
cd docker
docker-compose -p gatewaytest \
    -f docker-compose.yml \
    up --build --force-recreate -V
```
You can now view the application
at ``https://localhost:10000``.
