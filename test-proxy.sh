#!/bin/bash
# Diagnostic script to test the krypto-dashboard deployment

echo "========================================="
echo "Krypto Dashboard Diagnostic Test"
echo "========================================="
echo ""

echo "1. Testing Docker container status..."
docker ps | grep krypto-dashboard-web
echo ""

echo "2. Testing direct access to container (port 5013)..."
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://127.0.0.1:5013/
echo ""

echo "3. Testing if HTML is served..."
curl -s http://127.0.0.1:5013/ | head -5
echo ""

echo "4. Recent container logs..."
docker logs --tail 20 krypto-dashboard-web_krypto-dashboard-web_1 2>&1
echo ""

echo "========================================="
echo "Next Steps:"
echo "========================================="
echo ""
echo "If the container is running and serving HTML:"
echo ""
echo "1. Go to Plesk → Domains → apps.kuracodez.space"
echo "2. Click 'Apache & Nginx Settings'"
echo "3. Add to 'Additional nginx directives':"
echo ""
cat << 'NGINX'
location = /krypto-dashboard {
    return 301 /krypto-dashboard/;
}

location /krypto-dashboard/ {
    proxy_pass http://127.0.0.1:5013/;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_connect_timeout 7d;
    proxy_send_timeout 7d;
    proxy_read_timeout 7d;
}
NGINX
echo ""
echo "4. Click 'OK' to save"
echo "5. Access: https://apps.kuracodez.space/krypto-dashboard"
echo ""
