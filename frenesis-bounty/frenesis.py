cat > frenesis.py << 'EOF'
#!/usr/bin/env python3
"""
FRENESIS - Bug Bounty Automation Suite
Usage: python3 frenesis.py -t target.com [OPTIONS]
"""

import argparse
import os
import sys
import json
from datetime import datetime
from modules.utils import print_banner, timestamp, save_results, Colors
from modules.scanner import Scanner

def main():
    parser = argparse.ArgumentParser(description='FRENESIS Bug Bounty Suite')
    parser.add_argument('-t', '--target', required=True, help='Target domain')
    parser.add_argument('-o', '--output', help='Output directory')
    parser.add_argument('--quick', action='store_true', help='Quick scan (skip port scan)')
    parser.add_argument('--full', action='store_true', help='Full reconnaissance')
    
    args = parser.parse_args()
    
    print_banner()
    
    target = args.target.replace('https://', '').replace('http://', '').split('/')[0]
    timestamp_str = timestamp()
    workspace = args.output or f"output/{target}_{timestamp_str}"
    os.makedirs(workspace, exist_ok=True)
    
    print(f"{Colors.INFO}[TARGET]{Colors.RESET} {target}")
    print(f"{Colors.INFO}[WORKSPACE]{Colors.RESET} {workspace}")
    print(f"{Colors.INFO}[START]{Colors.RESET} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run scanner
    scanner = Scanner(target, workspace)
    results = scanner.run()
    
    # Save results
    results['timestamp'] = timestamp_str
    results['target'] = target
    results['workspace'] = workspace
    
    save_results(results, f"{workspace}/report.json")
    
    # Print summary
    print(f"\n{Colors.GREEN}{'='*50}{Colors.RESET}")
    print(f"{Colors.GREEN}[SCAN COMPLETE]{Colors.RESET}")
    print(f"{Colors.GREEN}{'='*50}{Colors.RESET}")
    print(f"Subdomains:   {results['subdomains']}")
    print(f"Live Hosts:   {results['live_hosts']}")
    print(f"Open Ports:   {results['open_ports']}")
    print(f"Vulnerabilities: {Colors.RED}{results['vulnerabilities']}{Colors.RESET}")
    print(f"Workspace:    {workspace}")
    
    if results['vulnerabilities'] > 0:
        print(f"\n{Colors.RED}[!] CRITICAL FINDINGS:{Colors.RESET}")
        for f in results['findings'][:5]:
            print(f"    {f[:100]}")
    
    print(f"\n{Colors.GREEN}[+] Report saved: {workspace}/report.json{Colors.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Scan interrupted by user{Colors.RESET}")
        sys.exit(0)
EOF

chmod +x frenesis.py