#!/usr/bin/env python3
"""
Project Revelare Web - Comprehensive Development Environment Installer
Installs complete coding, cybersecurity, and pentesting toolkit for Windows
Includes: Node.js, Python, Git, VS Code, Docker, WSL2, security tools, and more
"""
import os
import subprocess
import sys
import ctypes
import logging
from datetime import datetime

# Comprehensive tool installation definitions
DEVELOPMENT_TOOLS = {
    "core": [
        ("OpenJS.NodeJS", "Node.js Runtime", "node --version"),
        ("Python.Python.3.12", "Python 3.12", "python --version"),
        ("Git.Git", "Git Version Control", "git --version"),
        ("Microsoft.VisualStudioCode", "Visual Studio Code", "code --version"),
        ("Microsoft.WindowsTerminal", "Windows Terminal", "wt --version"),
        ("Microsoft.PowerShell", "PowerShell 7", "pwsh --version"),
    ],
    "containers": [
        ("Docker.DockerDesktop", "Docker Desktop", "docker --version"),
        ("Microsoft.WSL", "Windows Subsystem for Linux", "wsl --version"),
    ],
    "databases": [
        ("PostgreSQL.PostgreSQL", "PostgreSQL Database", "psql --version"),
        ("MongoDB.DatabaseTools", "MongoDB Tools", "mongodump --version"),
        ("Redis.Redis", "Redis Database", "redis-server --version"),
    ],
    "cloud": [
        ("Amazon.AWSCLI", "AWS CLI", "aws --version"),
        ("Microsoft.AzureCLI", "Azure CLI", "az --version"),
        ("Google.CloudSDK", "Google Cloud SDK", "gcloud --version"),
    ]
}

SECURITY_TOOLS = {
    "network": [
        ("Nmap.Nmap", "Network Mapper", "nmap --version"),
        ("Wireshark.Wireshark", "Network Protocol Analyzer", "wireshark --version"),
        ("Ethereal.WinPcap", "WinPcap", None),
    ],
    "pentesting": [
        ("Metasploit.Metasploit", "Metasploit Framework", "msfconsole --version"),
        ("BurpSuite.BurpSuiteCommunity", "Burp Suite Community", None),
        ("OWASP.ZAP", "OWASP ZAP", "zap.sh --version"),
    ],
    "forensics": [
        ("Autopsy.Autopsy", "Digital Forensics Platform", None),
        ("Volatility.Volatility", "Memory Forensics", "vol.py --version"),
    ],
    "utilities": [
        ("7zip.7zip", "7-Zip Archive Manager", "7z --version"),
        ("GnuPG.GnuPG", "GnuPG Encryption", "gpg --version"),
        ("Hashicorp.Vault", "Vault Secrets Management", "vault --version"),
    ]
}

CODING_EXTENSIONS = {
    "vscode": [
        "ms-python.python",
        "ms-vscode.vscode-typescript-next",
        "bradlc.vscode-tailwindcss",
        "esbenp.prettier-vscode",
        "ms-vscode.vscode-json",
        "redhat.vscode-yaml",
        "ms-vscode.powershell",
        "ms-vscode-remote.remote-wsl",
        "ms-vscode-remote.remote-containers",
        "github.copilot",
        "github.copilot-chat",
        "ms-vscode.vscode-github-actions",
        "ms-vscode.vscode-docker",
        "ms-azuretools.vscode-azurefunctions",
        "ms-azuretools.vscode-azureresourcegroups",
    ]
}

PYTHON_PACKAGES = [
    "pip", "setuptools", "wheel",
    "requests", "beautifulsoup4", "selenium",
    "pandas", "numpy", "matplotlib", "seaborn",
    "flask", "django", "fastapi",
    "pytest", "black", "flake8", "mypy",
    "jupyter", "notebook", "ipython",
    "cryptography", "pycryptodome",
    "scapy", "paramiko", "netaddr",
    "python-nmap", "python-whois",
    "shodan", "censys", "virustotal-api",
    "yara-python", "pefile", "capstone",
    "keystone-engine", "unicorn","scoop",
]

NODE_PACKAGES = [
    "npm", "yarn", "pnpm",
    "typescript", "@types/node",
    "eslint", "prettier", "nodemon",
    "express", "fastify", "koa",
    "react", "vue", "angular",
    "webpack", "vite", "rollup",
    "jest", "mocha", "cypress",
    "wrangler", "vercel", "netlify-cli",
]

SYSTEM_UTILITIES = [
    ("Microsoft.PowerToys", "PowerToys", None),
    ("Microsoft.DotNet.SDK.8", ".NET 8 SDK", "dotnet --version"),
    ("JetBrains.IntelliJIDEA.Community", "IntelliJ IDEA Community", None),
    ("JetBrains.PyCharm.Community", "PyCharm Community", None),
    ("SublimeHQ.SublimeText", "Sublime Text", None),
    ("Notepad++.Notepad++", "Notepad++", None),
    ("Figma.Figma", "Figma Desktop", None),
    ("OBSProject.OBSStudio", "OBS Studio", None),
]

# Setup debug logging
def setup_logging():
    """Setup comprehensive debug logging"""
    log_filename = f"install_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return log_filename

def debug_log(message, level="INFO"):
    """Log debug message with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")
    if level == "DEBUG":
        logging.debug(message)
    elif level == "INFO":
        logging.info(message)
    elif level == "WARNING":
        logging.warning(message)
    elif level == "ERROR":
        logging.error(message)

def is_admin():
    """Check if script is running as administrator"""
    debug_log("Checking administrator privileges...", "DEBUG")
    try:
        result = ctypes.windll.shell32.IsUserAnAdmin()
        debug_log(f"Admin check result: {result}", "DEBUG")
        return result
    except Exception as e:
        debug_log(f"Error checking admin privileges: {e}", "ERROR")
        return False

def run_as_admin():
    """Restart script as administrator"""
    debug_log("Attempting to restart as administrator...", "INFO")
    if is_admin():
        debug_log("Already running as administrator", "INFO")
        return True
    else:
        debug_log("This script requires administrator privileges.", "WARNING")
        debug_log("Restarting as administrator...", "INFO")
        try:
            debug_log(f"Executing: {sys.executable} {' '.join(sys.argv)}", "DEBUG")
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            debug_log("Successfully restarted as administrator", "INFO")
            return True
        except Exception as e:
            debug_log(f"Failed to restart as administrator: {e}", "ERROR")
            return False

def run_command(command, description, allow_failure=False):
    """Run a command with error handling and debug logging"""
    debug_log(f"Starting command execution: {description}", "INFO")
    debug_log(f"Command to execute: {command}", "DEBUG")
    
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    try:
        debug_log("Executing command...", "DEBUG")
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        debug_log("Command executed successfully", "INFO")
        debug_log(f"Exit code: {result.returncode}", "DEBUG")
        debug_log(f"STDOUT length: {len(result.stdout)} characters", "DEBUG")
        debug_log(f"STDERR length: {len(result.stderr)} characters", "DEBUG")
        
        print("✅ SUCCESS!")
        if result.stdout:
            debug_log(f"Command output: {result.stdout}", "DEBUG")
            print("Output:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        debug_log(f"Command failed with exit code: {e.returncode}", "ERROR")
        debug_log(f"STDOUT: {e.stdout}", "DEBUG")
        debug_log(f"STDERR: {e.stderr}", "DEBUG")
        
        print(f"❌ ERROR: Command failed with exit code {e.returncode}")
        if e.stdout:
            debug_log(f"Output: {e.stdout}", "DEBUG")
            print("Output:", e.stdout)
        if e.stderr:
            debug_log(f"Error: {e.stderr}", "DEBUG")
            print("Error:", e.stderr)
        
        if not allow_failure:
            debug_log("Command failure not allowed, prompting user", "WARNING")
            response = input("\nDo you want to continue anyway? (Y/N): ").upper()
            debug_log(f"User response: {response}", "DEBUG")
            if response != 'Y':
                debug_log("User chose to cancel installation", "WARNING")
                print("Installation cancelled.")
                return False
        return True
    except Exception as e:
        debug_log(f"Unexpected error during command execution: {e}", "ERROR")
        print(f"❌ UNEXPECTED ERROR: {e}")
        response = input("\nDo you want to continue anyway? (Y/N): ").upper()
        debug_log(f"User response to unexpected error: {response}", "DEBUG")
        if response != 'Y':
            debug_log("User chose to cancel installation", "WARNING")
            print("Installation cancelled.")
            return False
        return True

def check_command_exists(command):
    """Check if a command exists in PATH"""
    try:
        subprocess.run(f"where {command}", shell=True, capture_output=True, check=True)
        return True
    except:
        return False

def check_command_exists(command):
    """Check if a command exists in PATH"""
    debug_log(f"Checking if command exists: {command}", "DEBUG")
    try:
        result = subprocess.run(f"where {command}", shell=True, capture_output=True, check=True)
        debug_log(f"Command '{command}' found in PATH", "DEBUG")
        debug_log(f"Command path: {result.stdout.strip()}", "DEBUG")
        return True
    except subprocess.CalledProcessError:
        debug_log(f"Command '{command}' not found in PATH", "DEBUG")
        return False
    except Exception as e:
        debug_log(f"Error checking command existence: {e}", "ERROR")
        return False

def install_tool_category(category_name, tools_dict, category_title):
    """Install a category of tools"""
    debug_log(f"Starting installation of {category_name}: {category_title}", "INFO")
    print(f"\n🔧 {category_title}")
    print("=" * 60)
    
    installed_count = 0
    total_count = sum(len(tools) for tools in tools_dict.values())
    
    for subcategory, tools in tools_dict.items():
        debug_log(f"Installing {subcategory} tools", "INFO")
        print(f"\n📦 {subcategory.title()} Tools:")
        
        for package_id, tool_name, version_check in tools:
            debug_log(f"Processing tool: {tool_name} ({package_id})", "DEBUG")
            print(f"  • {tool_name}...", end=" ")
            
            # Check if tool is already installed
            if version_check and check_command_exists(version_check.split()[0]):
                debug_log(f"{tool_name} already installed", "INFO")
                print("✅ Already installed")
                installed_count += 1
                continue
            
            # Install the tool
            install_command = f"winget install {package_id} --accept-package-agreements --accept-source-agreements --silent"
            debug_log(f"Installing {tool_name} with command: {install_command}", "DEBUG")
            
            try:
                result = subprocess.run(install_command, shell=True, capture_output=True, text=True, timeout=300)
                if result.returncode == 0:
                    debug_log(f"Successfully installed {tool_name}", "INFO")
                    print("✅ Installed")
                    installed_count += 1
                else:
                    debug_log(f"Failed to install {tool_name}: {result.stderr}", "WARNING")
                    print("⚠️  Installation failed")
            except subprocess.TimeoutExpired:
                debug_log(f"Timeout installing {tool_name}", "WARNING")
                print("⏰ Timeout")
            except Exception as e:
                debug_log(f"Error installing {tool_name}: {e}", "ERROR")
                print("❌ Error")
    
    debug_log(f"Completed {category_name}: {installed_count}/{total_count} tools installed", "INFO")
    print(f"\n📊 {category_name.title()} Summary: {installed_count}/{total_count} tools installed")
    return installed_count, total_count

def install_python_packages():
    """Install Python packages for development and security"""
    debug_log("Starting Python package installation", "INFO")
    print(f"\n🐍 Installing Python Packages")
    print("=" * 60)
    
    if not check_command_exists("python"):
        debug_log("Python not found, skipping package installation", "WARNING")
        print("⚠️  Python not found, skipping package installation")
        return 0, len(PYTHON_PACKAGES)
    
    installed_count = 0
    total_count = len(PYTHON_PACKAGES)
    
    # Install packages in batches to avoid timeout
    batch_size = 5
    for i in range(0, len(PYTHON_PACKAGES), batch_size):
        batch = PYTHON_PACKAGES[i:i + batch_size]
        debug_log(f"Installing Python package batch: {batch}", "DEBUG")
        
        try:
            install_command = f"python -m pip install {' '.join(batch)} --upgrade"
            debug_log(f"Installing batch with command: {install_command}", "DEBUG")
            
            result = subprocess.run(install_command, shell=True, capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                installed_count += len(batch)
                debug_log(f"Successfully installed batch: {batch}", "INFO")
                print(f"✅ Installed batch: {', '.join(batch)}")
            else:
                debug_log(f"Failed to install batch: {result.stderr}", "WARNING")
                print(f"⚠️  Failed batch: {', '.join(batch)}")
        except subprocess.TimeoutExpired:
            debug_log(f"Timeout installing batch: {batch}", "WARNING")
            print(f"⏰ Timeout batch: {', '.join(batch)}")
        except Exception as e:
            debug_log(f"Error installing batch: {e}", "ERROR")
            print(f"❌ Error batch: {', '.join(batch)}")
    
    debug_log(f"Python packages installation completed: {installed_count}/{total_count}", "INFO")
    print(f"\n📊 Python Packages Summary: {installed_count}/{total_count} packages installed")
    return installed_count, total_count

def install_node_packages():
    """Install Node.js packages globally"""
    debug_log("Starting Node.js package installation", "INFO")
    print(f"\n📦 Installing Node.js Packages")
    print("=" * 60)
    
    if not check_command_exists("npm"):
        debug_log("npm not found, skipping package installation", "WARNING")
        print("⚠️  npm not found, skipping package installation")
        return 0, len(NODE_PACKAGES)
    
    installed_count = 0
    total_count = len(NODE_PACKAGES)
    
    for package in NODE_PACKAGES:
        debug_log(f"Installing Node.js package: {package}", "DEBUG")
        print(f"  • {package}...", end=" ")
        
        try:
            install_command = f"npm install -g {package}"
            debug_log(f"Installing with command: {install_command}", "DEBUG")
            
            result = subprocess.run(install_command, shell=True, capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                installed_count += 1
                debug_log(f"Successfully installed {package}", "INFO")
                print("✅ Installed")
            else:
                debug_log(f"Failed to install {package}: {result.stderr}", "WARNING")
                print("⚠️  Failed")
        except subprocess.TimeoutExpired:
            debug_log(f"Timeout installing {package}", "WARNING")
            print("⏰ Timeout")
        except Exception as e:
            debug_log(f"Error installing {package}: {e}", "ERROR")
            print("❌ Error")
    
    debug_log(f"Node.js packages installation completed: {installed_count}/{total_count}", "INFO")
    print(f"\n📊 Node.js Packages Summary: {installed_count}/{total_count} packages installed")
    return installed_count, total_count

def install_vscode_extensions():
    """Install VS Code extensions"""
    debug_log("Starting VS Code extension installation", "INFO")
    print(f"\n🔌 Installing VS Code Extensions")
    print("=" * 60)
    
    if not check_command_exists("code"):
        debug_log("VS Code not found, skipping extension installation", "WARNING")
        print("⚠️  VS Code not found, skipping extension installation")
        return 0, len(CODING_EXTENSIONS["vscode"])
    
    installed_count = 0
    total_count = len(CODING_EXTENSIONS["vscode"])
    
    for extension in CODING_EXTENSIONS["vscode"]:
        debug_log(f"Installing VS Code extension: {extension}", "DEBUG")
        print(f"  • {extension}...", end=" ")
        
        try:
            install_command = f"code --install-extension {extension}"
            debug_log(f"Installing with command: {install_command}", "DEBUG")
            
            result = subprocess.run(install_command, shell=True, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                installed_count += 1
                debug_log(f"Successfully installed {extension}", "INFO")
                print("✅ Installed")
            else:
                debug_log(f"Failed to install {extension}: {result.stderr}", "WARNING")
                print("⚠️  Failed")
        except subprocess.TimeoutExpired:
            debug_log(f"Timeout installing {extension}", "WARNING")
            print("⏰ Timeout")
        except Exception as e:
            debug_log(f"Error installing {extension}: {e}", "ERROR")
            print("❌ Error")
    
    debug_log(f"VS Code extensions installation completed: {installed_count}/{total_count}", "INFO")
    print(f"\n📊 VS Code Extensions Summary: {installed_count}/{total_count} extensions installed")
    return installed_count, total_count

def main():
    """Main installation process - Comprehensive Development Environment Setup"""
    # Setup logging
    log_filename = setup_logging()
    debug_log("Starting Comprehensive Development Environment Installer", "INFO")
    debug_log(f"Debug log file: {log_filename}", "INFO")
    debug_log(f"Python version: {sys.version}", "DEBUG")
    debug_log(f"Script arguments: {sys.argv}", "DEBUG")
    debug_log(f"Current working directory: {os.getcwd()}", "DEBUG")
    
    print("🚀 Comprehensive Development Environment Installer")
    print("=" * 80)
    print("🎯 This will install a complete coding, cybersecurity, and pentesting toolkit")
    print("📦 Includes: Development tools, security tools, databases, cloud CLI, and more")
    print("=" * 80)
    debug_log("Displaying welcome message", "DEBUG")
    
    # Check if running as admin
    debug_log("Checking administrator privileges", "INFO")
    if not is_admin():
        debug_log("Not running as admin, attempting to restart", "WARNING")
        if not run_as_admin():
            debug_log("Failed to restart as administrator", "ERROR")
            print("❌ Cannot proceed without administrator privileges.")
            input("Press Enter to exit...")
            return
        return
    
    debug_log("Confirmed running as administrator", "INFO")
    print("✅ Running as administrator")
    
    # Installation summary tracking
    total_installed = 0
    total_available = 0
    
    # Step 1: Core Development Tools
    debug_log("Starting Step 1: Core Development Tools", "INFO")
    installed, available = install_tool_category("core", DEVELOPMENT_TOOLS, "Core Development Tools")
    total_installed += installed
    total_available += available
    
    # Step 2: Refresh environment variables
    debug_log("Starting Step 2: Environment refresh", "INFO")
    print("\n🔄 Refreshing environment variables...")
    run_command("refreshenv", "Refreshing environment variables", allow_failure=True)
    
    # Step 3: Container & Database Tools
    debug_log("Starting Step 3: Container & Database Tools", "INFO")
    installed, available = install_tool_category("containers", {"containers": DEVELOPMENT_TOOLS["containers"]}, "Container & Database Tools")
    total_installed += installed
    total_available += available
    
    installed, available = install_tool_category("databases", {"databases": DEVELOPMENT_TOOLS["databases"]}, "Database Tools")
    total_installed += installed
    total_available += available
    
    # Step 4: Cloud CLI Tools
    debug_log("Starting Step 4: Cloud CLI Tools", "INFO")
    installed, available = install_tool_category("cloud", {"cloud": DEVELOPMENT_TOOLS["cloud"]}, "Cloud CLI Tools")
    total_installed += installed
    total_available += available
    
    # Step 5: Security Tools
    debug_log("Starting Step 5: Security Tools", "INFO")
    installed, available = install_tool_category("security", SECURITY_TOOLS, "Security & Pentesting Tools")
    total_installed += installed
    total_available += available
    
    # Step 6: System Utilities
    debug_log("Starting Step 6: System Utilities", "INFO")
    installed, available = install_tool_category("utilities", {"utilities": SYSTEM_UTILITIES}, "System Utilities")
    total_installed += installed
    total_available += available
    
    # Step 7: Python Packages
    debug_log("Starting Step 7: Python Packages", "INFO")
    installed, available = install_python_packages()
    total_installed += installed
    total_available += available
    
    # Step 8: Node.js Packages
    debug_log("Starting Step 8: Node.js Packages", "INFO")
    installed, available = install_node_packages()
    total_installed += installed
    total_available += available
    
    # Step 9: VS Code Extensions
    debug_log("Starting Step 9: VS Code Extensions", "INFO")
    installed, available = install_vscode_extensions()
    total_installed += installed
    total_available += available
    
    # Step 10: Project-specific setup
    debug_log("Starting Step 10: Project-specific setup", "INFO")
    print(f"\n📁 Project-Specific Setup")
    print("=" * 60)
    
    project_dir = r"E:\Scripts\project-revelare-web"
    debug_log(f"Checking project directory: {project_dir}", "DEBUG")
    if os.path.exists(project_dir):
        debug_log(f"Project directory found: {project_dir}", "INFO")
        print(f"✅ Project directory found: {project_dir}")
        
        # Get Cloudflare resource IDs if wrangler is available
        if check_command_exists("wrangler"):
            debug_log("Wrangler found, getting Cloudflare resources", "INFO")
            print("\n☁️  Getting Cloudflare resource IDs...")
            print("Getting KV namespace list...")
            run_command("wrangler kv:namespace list", "Listing KV namespaces", allow_failure=True)
            
            print("\nGetting D1 database list...")
            run_command("wrangler d1 list", "Listing D1 databases", allow_failure=True)
        else:
            debug_log("Wrangler not found, skipping Cloudflare setup", "WARNING")
            print("⚠️  Wrangler not found, skipping Cloudflare resource discovery")
    else:
        debug_log(f"Project directory not found: {project_dir}", "WARNING")
        print(f"⚠️  Project directory not found: {project_dir}")
    
    # Final Summary
    debug_log("Installation process completed", "INFO")
    print(f"\n🎉 Installation Complete!")
    print("=" * 80)
    print(f"📊 Overall Summary: {total_installed}/{total_available} tools installed")
    print("=" * 80)
    print("🎯 Your Windows PC is now equipped with:")
    print("  • Complete development environment (Node.js, Python, Git, VS Code)")
    print("  • Container tools (Docker, WSL2)")
    print("  • Database tools (PostgreSQL, MongoDB, Redis)")
    print("  • Cloud CLI tools (AWS, Azure, Google Cloud)")
    print("  • Security tools (Nmap, Wireshark, Metasploit, Burp Suite)")
    print("  • Pentesting tools (OWASP ZAP, Volatility)")
    print("  • Forensics tools (Autopsy)")
    print("  • System utilities (PowerToys, .NET SDK)")
    print("  • VS Code extensions for enhanced development")
    print("  • Python packages for security and development")
    print("  • Node.js packages for web development")
    print("=" * 80)
    print("🚀 Next steps:")
    print("1. Restart your computer to ensure all PATH changes take effect")
    print("2. Open VS Code and explore the installed extensions")
    print("3. Test your tools: 'node --version', 'python --version', 'git --version'")
    print("4. For security tools: 'nmap --version', 'wireshark --version'")
    print("5. Update wrangler.json with your actual Cloudflare resource IDs")
    print(f"6. Check debug log: {log_filename}")
    print("=" * 80)
    
    debug_log("Installation completed, waiting for user input", "DEBUG")
    input("\nPress Enter to exit...")
    debug_log("Script execution finished", "INFO")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        debug_log("Installation cancelled by user (Ctrl+C)", "WARNING")
        print("\n\n❌ Installation cancelled by user.")
        input("Press Enter to exit...")
    except Exception as e:
        debug_log(f"Unexpected error in main execution: {e}", "ERROR")
        print(f"\n❌ Unexpected error: {e}")
        input("Press Enter to exit...")
