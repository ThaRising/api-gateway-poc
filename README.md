# API Gateway

This is a proof-of-concept for an
infrastructure design to be used
in Drizm infrastructure.

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