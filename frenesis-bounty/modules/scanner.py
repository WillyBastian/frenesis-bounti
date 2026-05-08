cat > modules/scanner.py << 'EOF'
import os
import subprocess
from modules.utils import run_command, Colors

class Scanner:
    def __init__(self, target, workspace):
        self.target = target
        self.workspace = workspace
        self.findings = []
        
    def phase1_subdomains(self):
        print(f"\n{Colors.INFO}[PHASE 1]{Colors.RESET} Subdomain Enumeration")
        
        all_subs = set()
        
        # Subfinder
        out, _, _ = run_command(f"subfinder -d {self.target} -silent")
        for line in out.splitlines():
            all_subs.add(line.strip())
        
        # Assetfinder
        out, _, _ = run_command(f"assetfinder --subs-only {self.target} 2>/dev/null")
        for line in out.splitlines():
            all_subs.add(line.strip())
        
        # Save
        sub_file = f"{self.workspace}/subdomains.txt"
        with open(sub_file, 'w') as f:
            for sub in sorted(all_subs):
                f.write(sub + "\n")
        
        print(f"{Colors.GREEN}[+]{Colors.RESET} Found {len(all_subs)} subdomains")
        return list(all_subs)
    
    def phase2_probe(self, subdomains):
        print(f"\n{Colors.INFO}[PHASE 2]{Colors.RESET} Probing Live Hosts")
        
        if not subdomains:
            print(f"{Colors.YELLOW}[!]{Colors.RESET} No subdomains to probe")
            return []
        
        sub_file = f"{self.workspace}/subdomains.txt"
        live_file = f"{self.workspace}/live_hosts.txt"
        
        run_command(f"httpx -l {sub_file} -silent -status-code -title -o {live_file}")
        
        live_hosts = []
        if os.path.exists(live_file):
            with open(live_file, 'r') as f:
                live_hosts = [line.strip() for line in f if line.strip()]
        
        print(f"{Colors.GREEN}[+]{Colors.RESET} Found {len(live_hosts)} live hosts")
        return live_hosts
    
    def phase3_ports(self):
        print(f"\n{Colors.INFO}[PHASE 3]{Colors.RESET} Port Scanning")
        
        port_file = f"{self.workspace}/open_ports.txt"
        run_command(f"naabu -host {self.target} -top-ports 100 -silent -o {port_file}")
        
        ports = []
        if os.path.exists(port_file):
            with open(port_file, 'r') as f:
                ports = [line.strip() for line in f if line.strip()]
        
        print(f"{Colors.GREEN}[+]{Colors.RESET} Found {len(ports)} open ports")
        return ports
    
    def phase4_vuln(self, live_hosts):
        print(f"\n{Colors.INFO}[PHASE 4]{Colors.RESET} Vulnerability Scanning")
        
        if not live_hosts:
            print(f"{Colors.YELLOW}[!]{Colors.RESET} No live hosts")
            return []
        
        live_file = f"{self.workspace}/live_hosts.txt"
        crit_file = f"{self.workspace}/critical_findings.txt"
        
        run_command(f"nuclei -l {live_file} -severity critical,high -silent -o {crit_file}")
        
        critical = []
        if os.path.exists(crit_file):
            with open(crit_file, 'r') as f:
                critical = [line.strip() for line in f if line.strip()]
                for finding in critical:
                    self.findings.append(finding)
        
        print(f"{Colors.RED}[!]{Colors.RESET} Found {len(critical)} critical/high findings")
        return critical
    
    def run(self):
        subs = self.phase1_subdomains()
        live = self.phase2_probe(subs)
        ports = self.phase3_ports()
        vulns = self.phase4_vuln(live)
        
        return {
            'target': self.target,
            'subdomains': len(subs),
            'live_hosts': len(live),
            'open_ports': len(ports),
            'vulnerabilities': len(vulns),
            'findings': self.findings
        }
EOF