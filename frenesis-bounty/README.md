cat > README.md << 'EOF'
# 🔥 FRENESIS - Bug Bounty Automation Suite

[![License](https://img.shields.io/badge/license-MIT-red.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://python.org)
[![Tools](https://img.shields.io/badge/tools-subfinder%20%7C%20nuclei%20%7C%20httpx-blue.svg)](https://github.com/projectdiscovery)

## 🎯 Features

- **Automated Subdomain Enumeration** (subfinder + assetfinder)
- **Live Host Probing** (httpx with tech detection)
- **Port Scanning** (naabu top 100 ports)
- **Vulnerability Detection** (nuclei with critical/high severity)
- **JSON Report Generation**
- **Zero Censorship - Full Power**

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/frenesis-bounty.git
cd frenesis-bounty

# Run setup
chmod +x setup.sh
./setup.sh

# Start scanning
python3 frenesis.py -t target.com