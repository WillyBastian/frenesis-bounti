cat > modules/utils.py << 'EOF'
import subprocess
import sys
import time
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

class Colors:
    CRITICAL = Fore.RED + Style.BRIGHT
    HIGH = Fore.YELLOW + Style.BRIGHT
    MEDIUM = Fore.CYAN
    INFO = Fore.GREEN
    RESET = Style.RESET_ALL

def print_banner():
    banner = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════╗
{Fore.RED}║{Fore.GREEN}      ███████╗██████╗ ███████╗███╗   ██╗███████╗███████╗██╗███████╗{Fore.RED}║
{Fore.RED}║{Fore.GREEN}      ██╔════╝██╔══██╗██╔════╝████╗  ██║██╔════╝██╔════╝██║██╔════╝{Fore.RED}║
{Fore.RED}║{Fore.GREEN}      █████╗  ██████╔╝█████╗  ██╔██╗ ██║█████╗  ███████╗██║███████╗{Fore.RED}║
{Fore.RED}║{Fore.GREEN}      ██╔══╝  ██╔══██╗██╔══╝  ██║╚██╗██║██╔══╝  ╚════██║██║╚════██║{Fore.RED}║
{Fore.RED}║{Fore.GREEN}      ██║     ██║  ██║███████╗██║ ╚████║███████╗███████║██║███████║{Fore.RED}║
{Fore.RED}║{Fore.GREEN}      ╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝╚══════╝{Fore.RED}║
{Fore.RED}╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
{Fore.CYAN}                    Bug Bounty Automation Suite v3.0
{Fore.YELLOW}                  [ No Limits | No Censorship | Pure Power ]
{Style.RESET_ALL}
"""
    print(banner)

def run_command(cmd, timeout=180, silent=False):
    try:
        if not silent:
            print(f"{Fore.BLUE}[*]{Fore.RESET} Running: {cmd[:80]}...")
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return proc.stdout.strip(), proc.stderr.strip(), proc.returncode
    except subprocess.TimeoutExpired:
        return "", "timeout", -1
    except Exception as e:
        return "", str(e), -1

def save_results(data, filename):
    import json
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"{Fore.GREEN}[+]{Fore.RESET} Saved: {filename}")

def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")
EOF