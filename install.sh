#!/bin/bash
set -e

# =======================================================
# Lightweight Sub Web Manager - One-Click Install Script
# =======================================================

echo "========================================"
echo " Starting installation of Sub Web Manager"
echo "========================================"

# 1. Update and install dependencies
echo "[1/4] Installing system dependencies..."
apt-get update -y
apt-get install -y python3 python3-pip python3-venv git

# 2. Setup application directory
INSTALL_DIR="/opt/sub-web-manager"
echo "[2/4] Setting up application directory at $INSTALL_DIR..."
mkdir -p $INSTALL_DIR
cd $INSTALL_DIR

# Download files if this script is run from a remote URL
if [ ! -f "app.py" ]; then
    echo "Downloading app.py..."
    curl -fsSLO "https://raw.githubusercontent.com/liuyue840/sub-web-manager/main/app.py"
    curl -fsSLO "https://raw.githubusercontent.com/liuyue840/sub-web-manager/main/requirements.txt"
fi

# 3. Setup Python virtual environment
echo "[3/4] Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Setup systemd service
echo "[4/4] Configuring systemd service..."
cat << 'SERVICE_EOF' > /etc/systemd/system/sub-web.service
[Unit]
Description=Lightweight Sub Web Manager
After=network.target

[Service]
User=root
WorkingDirectory=/opt/sub-web-manager
ExecStart=/opt/sub-web-manager/venv/bin/python app.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
SERVICE_EOF

# Reload and start service
systemctl daemon-reload
systemctl enable sub-web
systemctl restart sub-web

echo "========================================"
echo " Installation Completed Successfully!"
echo " The Web Panel is running on port 8123."
echo " Access it via: http://YOUR_IP:8123"
echo "========================================"
