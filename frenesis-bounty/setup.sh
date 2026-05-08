cat > setup.sh << 'EOF'
#!/bin/bash

echo "[+] FRENESIS Bug Bounty Setup"
echo "[+] Installing Python dependencies..."
pip3 install -r requirements.txt

echo "[+] Checking Go tools..."
if ! command -v subfinder &> /dev/null; then
    echo "[+] Installing subfinder..."
    go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
fi

if ! command -v httpx &> /dev/null; then
    echo "[+] Installing httpx..."
    go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
fi

if ! command -v nuclei &> /dev/null; then
    echo "[+] Installing nuclei..."
    go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
fi

if ! command -v naabu &> /dev/null; then
    echo "[+] Installing naabu..."
    go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
fi

echo "[+] Copying binaries..."
sudo cp ~/go/bin/* /usr/local/bin/ 2>/dev/null

echo "[+] Setup complete!"
echo "[+] Run: python3 frenesis.py -t target.com"
EOF

chmod +x setup.sh