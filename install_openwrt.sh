#!/bin/sh
set -e

# =======================================================
# Lightweight Sub Web Manager - OpenWrt Install Script
# =======================================================

echo "========================================"
echo " Starting OpenWrt installation"
echo "========================================"

# 1. Update and install dependencies
echo "[1/4] Installing system dependencies via opkg..."
opkg update
opkg install python3 python3-pip curl

# 2. Setup application directory
INSTALL_DIR="/opt/sub-web-manager"
echo "[2/4] Setting up application directory at $INSTALL_DIR..."
mkdir -p $INSTALL_DIR
cd $INSTALL_DIR

# Download files
if [ ! -f "app.py" ]; then
    echo "Downloading app.py..."
    curl -fsSLO "https://raw.githubusercontent.com/liuyue840/sub-web-manager/main/app.py"
fi

# 3. Install Flask (Globally for OpenWrt to save space and avoid venv overhead)
echo "[3/4] Installing Python dependencies (Flask)..."
pip3 install Flask --break-system-packages || pip3 install Flask

# 4. Setup OpenWrt procd service
echo "[4/4] Configuring OpenWrt procd init script..."
cat << 'SERVICE_EOF' > /etc/init.d/sub-web
#!/bin/sh /etc/rc.common

USE_PROCD=1
START=99
STOP=15

start_service() {
    procd_open_instance
    procd_set_param command /usr/bin/python3 /opt/sub-web-manager/app.py
    procd_set_param respawn
    procd_set_param stdout 1
    procd_set_param stderr 1
    procd_close_instance
}
SERVICE_EOF

chmod +x /etc/init.d/sub-web

# Enable and start service
/etc/init.d/sub-web enable
/etc/init.d/sub-web start

echo "========================================"
echo " Installation Completed Successfully!"
echo " The Web Panel is running on port 8123."
echo " Access it via: http://YOUR_ROUTER_IP:8123"
echo "========================================"
