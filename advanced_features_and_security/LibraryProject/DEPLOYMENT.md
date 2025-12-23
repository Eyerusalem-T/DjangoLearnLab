server {
listen 80;
server_name yourdomain.com www.yourdomain.com;
return 301 https://$host$request_uri;
}

server {
listen 443 ssl;
server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/ssl/certs/your_certificate.pem;
    ssl_certificate_key /etc/ssl/private/your_private_key.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Forwarded-For $remote_addr;
    }

}
