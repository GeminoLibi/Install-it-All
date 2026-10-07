#!/usr/bin/env python3
"""
Comprehensive Windows installer for a coding, cybersecurity, and pentesting toolkit.
Installs languages, editors, databases, cloud CLIs, and security tools with winget
and Scoop. Package ids are ones published by winget or by Scoop's official buckets.
"""
import os
import subprocess
import sys
import ctypes
import logging
from datetime import datetime

# (package id, display name, version command or None)
# A version command marks the tool present when its executable is already on PATH.
DEVELOPMENT_TOOLS = {
    "core": [
        ("OpenJS.NodeJS.LTS", "Node.js LTS", "node --version"),
        ("Python.Python.3.12", "Python 3.12", "python --version"),
        ("Git.Git", "Git", "git --version"),
        ("Microsoft.VisualStudioCode", "Visual Studio Code", "code --version"),
        ("Microsoft.WindowsTerminal", "Windows Terminal", "wt --version"),
        ("Microsoft.PowerShell", "PowerShell 7", "pwsh --version"),
        ("GitHub.cli", "GitHub CLI", "gh --version"),
        ("Rustlang.Rustup", "Rustup", "rustup --version"),
        ("GoLang.Go", "Go", "go version"),
        ("EclipseAdoptium.Temurin.21.JDK", "Temurin JDK 21", "java -version"),
        ("astral-sh.uv", "uv", "uv --version"),
    ],
    "cli": [
        ("Kitware.CMake", "CMake", "cmake --version"),
        ("BurntSushi.ripgrep.MSVC", "ripgrep", "rg --version"),
        ("sharkdp.fd", "fd", "fd --version"),
        ("jqlang.jq", "jq", "jq --version"),
        ("astral-sh.ruff", "Ruff", "ruff --version"),
    ],
    "containers": [
        ("Docker.DockerDesktop", "Docker Desktop", "docker --version"),
        ("Microsoft.WSL", "Windows Subsystem for Linux", "wsl --version"),
    ],
    "databases": [
        ("PostgreSQL.PostgreSQL.17", "PostgreSQL 17", "psql --version"),
        ("MongoDB.DatabaseTools", "MongoDB Tools", "mongodump --version"),
        ("Redis.Redis", "Redis", "redis-server --version"),
        ("SQLite.SQLite", "SQLite", "sqlite3 --version"),
        ("DBeaver.DBeaver.Community", "DBeaver Community", None),
        ("DBBrowserForSQLite.DBBrowserForSQLite", "DB Browser for SQLite", None),
    ],
    "cloud": [
        ("Amazon.AWSCLI", "AWS CLI", "aws --version"),
        ("Microsoft.AzureCLI", "Azure CLI", "az --version"),
        ("Google.CloudSDK", "Google Cloud SDK", "gcloud --version"),
        ("Hashicorp.Terraform", "Terraform", "terraform --version"),
        ("Cloudflare.cloudflared", "cloudflared", "cloudflared --version"),
    ],
}

SECURITY_TOOLS = {
    "network": [
        ("WiresharkFoundation.Wireshark", "Wireshark", "tshark --version"),
    ],
    "pentesting": [
        ("PortSwigger.BurpSuite", "Burp Suite", None),
        ("ZAP.ZAP", "ZAP", "zap -version"),
        ("mitmproxy.mitmproxy", "mitmproxy", "mitmproxy --version"),
        ("ffuf.ffuf", "ffuf", "ffuf -V"),
        ("Maltego.Maltego", "Maltego", None),
    ],
    "forensics": [
        ("SleuthKit.Autopsy", "Autopsy", None),
        ("PassMark.OSFMount", "OSFMount", None),
        ("PassMark.VolatilityWorkbench", "Volatility Workbench", None),
        ("CGSecurity.TestDisk", "TestDisk and PhotoRec", None),
        ("OliverBetz.ExifTool", "ExifTool", "exiftool -ver"),
        ("VirusTotal.YARA", "YARA", "yara --version"),
        ("VirusTotal.vt-cli", "VirusTotal CLI", "vt version"),
        ("UB-Mannheim.TesseractOCR", "Tesseract OCR", "tesseract --version"),
        ("Gyan.FFmpeg", "FFmpeg", "ffmpeg -version"),
        ("Microsoft.WinDbg", "WinDbg", None),
    ],
    "reversing": [
        ("x64dbg.x64dbg", "x64dbg", None),
        ("WerWolv.ImHex", "ImHex", None),
        ("MHNexus.HxD", "HxD", None),
        ("hasherezade.PE-bear", "PE-bear", None),
        ("AngusJohnson.ResourceHacker", "Resource Hacker", None),
        ("horsicq.DIE-engine", "Detect It Easy", None),
        ("WinsiderSS.SystemInformer", "System Informer", None),
    ],
    "utilities": [
        ("7zip.7zip", "7-Zip", "7z --version"),
        ("GnuPG.Gpg4win", "Gpg4win", "gpg --version"),
        ("Hashicorp.Vault", "Vault", "vault --version"),
        ("Microsoft.Sysinternals.Suite", "Sysinternals Suite", None),
        ("KeePassXCTeam.KeePassXC", "KeePassXC", None),
        ("IDRIX.VeraCrypt", "VeraCrypt", None),
    ],
}

# Official Scoop buckets only. These are tools winget does not currently publish,
# or publishes only as a stale build (winget's Nmap package is still 7.80).
SCOOP_PACKAGES = [
    ("nmap", "Nmap", "nmap"),
    ("hashcat", "Hashcat", "hashcat"),
    ("gobuster", "Gobuster", "gobuster"),
    ("feroxbuster", "Feroxbuster", "feroxbuster"),
    ("amass", "Amass", "amass"),
    ("apktool", "apktool", "apktool"),
    ("gitleaks", "gitleaks", "gitleaks"),
    ("grype", "Grype", "grype"),
    ("chisel", "Chisel", "chisel"),
    ("cosign", "cosign", "cosign"),
    ("jadx", "JADX", "jadx"),
    ("ghidra", "Ghidra", "ghidraRun"),
    ("cutter", "Cutter", "cutter"),
    ("cyberchef", "CyberChef", None),
]

CODING_EXTENSIONS = {
    "vscode": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-vscode.vscode-typescript-next",
        "dbaeumer.vscode-eslint",
        "bradlc.vscode-tailwindcss",
        "esbenp.prettier-vscode",
        "ms-vscode.vscode-json",
        "redhat.vscode-yaml",
        "tamasfe.even-better-toml",
        "ms-vscode.powershell",
        "ms-vscode-remote.remote-wsl",
        "ms-vscode-remote.remote-containers",
        "github.copilot",
        "github.copilot-chat",
        "eamodio.gitlens",
        "GitHub.vscode-pull-request-github",
        "ms-vscode.vscode-github-actions",
        "ms-vscode.vscode-docker",
        "ms-azuretools.vscode-azurefunctions",
        "ms-azuretools.vscode-azureresourcegroups",
        "ms-vscode.hexeditor",
        "rust-lang.rust-analyzer",
        "golang.Go",
        "HashiCorp.terraform",
    ]
}

EDITORS = ["code", "cursor"]

PYTHON_PACKAGES = [
    "pip", "setuptools", "wheel",
    "requests", "beautifulsoup4", "selenium",
    "pandas", "numpy", "matplotlib", "seaborn",
    "flask", "django", "fastapi", "uvicorn",
    "pytest", "black", "flake8", "mypy",
    "jupyter", "notebook", "ipython",
    "cryptography", "pycryptodome",
    "scapy", "paramiko", "netaddr",
    "python-nmap", "python-whois",
    "shodan", "censys", "virustotal-api",
    "yara-python", "pefile", "capstone",
    "keystone-engine", "unicorn",
    "volatility3", "impacket", "sqlmap",
    "pillow", "exifread", "pypdf",
    "oletools", "lief", "python-registry", "pywin32",
    "theHarvester",
    "python-dotenv", "sqlalchemy",
    "psycopg2-binary", "pymongo",
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
    # Same `dotnet` command as SDK 8, so do not skip this just because dotnet exists.
    ("Microsoft.DotNet.SDK.10", ".NET 10 SDK", None),
    ("JetBrains.IntelliJIDEA.Community", "IntelliJ IDEA Community", None),
    ("JetBrains.PyCharm.Community", "PyCharm Community", None),
    ("SublimeHQ.SublimeText", "Sublime Text", None),
    ("Notepad++.Notepad++", "Notepad++", None),
    ("Figma.Figma", "Figma Desktop", None),
    ("OBSProject.OBSStudio", "OBS Studio", None),
    ("PuTTY.PuTTY", "PuTTY", None),
    ("WinSCP.WinSCP", "WinSCP", None),
    ("voidtools.Everything", "Everything", None),
]

WINGET_TIMEOUT_SECONDS = 900
SCOOP_TIMEOUT_SECONDS = 1200
METASPLOIT_TIMEOUT_SECONDS = 1800
JOHN_TIMEOUT_SECONDS = 900

# Rapid7's documented Windows silent install. INSTALLLOCATION is the drive
# or parent directory; the MSI creates metasploit-framework underneath it.
METASPLOIT_MSI_URL = "https://windows.metasploit.com/metasploitframework-latest.msi"
METASPLOIT_PARENT = r"C:\Tools"
METASPLOIT_BIN_CANDIDATES = [
    r"C:\Tools\metasploit-framework\bin",
    r"C:\metasploit-framework\bin",
    r"C:\Metasploit-framework\bin",
]

# Official Openwall Windows build of John the Ripper jumbo.
JOHN_ZIP_URL = "https://github.com/openwall/john-packages/releases/latest/download/winX64_1_JtR.zip"
JOHN_ROOT = r"C:\Tools\john"


def setup_logging():
    """Setup comprehensive debug logging"""
    log_filename = f"install_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler(sys.stdout),
        ],
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


def run_command(command, description, allow_failure=False, timeout=None):
    """Run a command with error handling and debug logging"""
    debug_log(f"Starting command execution: {description}", "INFO")
    debug_log(f"Command to execute: {command}", "DEBUG")

    print(f"\n{'=' * 60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'=' * 60}")

    try:
        debug_log("Executing command...", "DEBUG")
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True,
            timeout=timeout,
        )
        debug_log("Command executed successfully", "INFO")
        debug_log(f"Exit code: {result.returncode}", "DEBUG")
        debug_log(f"STDOUT length: {len(result.stdout)} characters", "DEBUG")
        debug_log(f"STDERR length: {len(result.stderr)} characters", "DEBUG")

        print("[ok] SUCCESS")
        if result.stdout:
            debug_log(f"Command output: {result.stdout}", "DEBUG")
            print("Output:", result.stdout)
        return True
    except subprocess.TimeoutExpired:
        debug_log(f"Timeout during command execution: {description}", "ERROR")
        print("[fail] TIMEOUT")
        if not allow_failure:
            response = input("\nDo you want to continue anyway? (Y/N): ").upper()
            debug_log(f"User response: {response}", "DEBUG")
            if response != "Y":
                debug_log("User chose to cancel installation", "WARNING")
                print("Installation cancelled.")
                return False
        return True
    except subprocess.CalledProcessError as e:
        debug_log(f"Command failed with exit code: {e.returncode}", "ERROR")
        debug_log(f"STDOUT: {e.stdout}", "DEBUG")
        debug_log(f"STDERR: {e.stderr}", "DEBUG")

        print(f"[fail] ERROR: Command failed with exit code {e.returncode}")
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
            if response != "Y":
                debug_log("User chose to cancel installation", "WARNING")
                print("Installation cancelled.")
                return False
        return True
    except Exception as e:
        debug_log(f"Unexpected error during command execution: {e}", "ERROR")
        print(f"[fail] UNEXPECTED ERROR: {e}")
        response = input("\nDo you want to continue anyway? (Y/N): ").upper()
        debug_log(f"User response to unexpected error: {response}", "DEBUG")
        if response != "Y":
            debug_log("User chose to cancel installation", "WARNING")
            print("Installation cancelled.")
            return False
        return True


def check_command_exists(command):
    """Check if a command exists in PATH"""
    debug_log(f"Checking if command exists: {command}", "DEBUG")
    if not command:
        return False
    finder = "where" if os.name == "nt" else "which"
    try:
        result = subprocess.run(
            [finder, command],
            capture_output=True,
            text=True,
            check=True,
        )
        debug_log(f"Command '{command}' found in PATH", "DEBUG")
        debug_log(f"Command path: {result.stdout.strip()}", "DEBUG")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        debug_log(f"Command '{command}' not found in PATH", "DEBUG")
        return False
    except Exception as e:
        debug_log(f"Error checking command existence: {e}", "ERROR")
        return False


def command_on_path(version_check):
    """True when the executable named by a version command is on PATH."""
    if not version_check:
        return False
    return check_command_exists(version_check.split()[0])


def _registry_path(root, subkey):
    import winreg

    try:
        with winreg.OpenKey(root, subkey) as key:
            value, _ = winreg.QueryValueEx(key, "Path")
            return os.path.expandvars(value or "")
    except OSError as e:
        debug_log(f"Could not read PATH from the registry: {e}", "WARNING")
        return ""


def refresh_process_path():
    """Reload PATH from the machine and user registry into this process."""
    if os.name != "nt":
        debug_log("PATH refresh is implemented for Windows only", "WARNING")
        return False
    import winreg

    debug_log("Refreshing PATH from the registry", "INFO")
    machine = _registry_path(
        winreg.HKEY_LOCAL_MACHINE,
        r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
    )
    user = _registry_path(winreg.HKEY_CURRENT_USER, "Environment")
    parts = [part for part in (machine, user) if part]
    if not parts:
        debug_log("Registry PATH was empty; leaving the process PATH unchanged", "WARNING")
        return False
    os.environ["Path"] = ";".join(parts)
    add_scoop_shims()
    debug_log("Process PATH refreshed", "DEBUG")
    return True


def add_scoop_shims():
    """Put Scoop shims on PATH for this process, including a fresh install."""
    candidates = []
    userprofile = os.environ.get("USERPROFILE", "")
    if userprofile:
        candidates.append(os.path.join(userprofile, "scoop", "shims"))
    programdata = os.environ.get("ProgramData", r"C:\ProgramData")
    candidates.append(os.path.join(programdata, "scoop", "shims"))
    path = os.environ.get("Path", "")
    path_lower = path.lower()
    for shim in candidates:
        if os.path.isdir(shim) and shim.lower() not in path_lower:
            path = shim + os.pathsep + path
            path_lower = path.lower()
            debug_log(f"Added Scoop shims to PATH: {shim}", "DEBUG")
    os.environ["Path"] = path


def install_tool_category(category_name, tools_dict, category_title):
    """Install a category of tools"""
    debug_log(f"Starting installation of {category_name}: {category_title}", "INFO")
    print(f"\n{category_title}")
    print("=" * 60)

    installed_count = 0
    total_count = sum(len(tools) for tools in tools_dict.values())

    for subcategory, tools in tools_dict.items():
        debug_log(f"Installing {subcategory} tools", "INFO")
        print(f"\n{subcategory.title()} tools:")

        for package_id, tool_name, version_check in tools:
            debug_log(f"Processing tool: {tool_name} ({package_id})", "DEBUG")
            print(f"  - {tool_name}...", end=" ")

            if command_on_path(version_check):
                debug_log(f"{tool_name} already installed", "INFO")
                print("[ok] Already installed")
                installed_count += 1
                continue

            install_command = (
                f"winget install --id {package_id} -e "
                "--accept-package-agreements --accept-source-agreements --silent"
            )
            debug_log(f"Installing {tool_name} with command: {install_command}", "DEBUG")

            try:
                result = subprocess.run(
                    install_command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=WINGET_TIMEOUT_SECONDS,
                )
                if result.returncode == 0:
                    debug_log(f"Successfully installed {tool_name}", "INFO")
                    print("[ok] Installed")
                    installed_count += 1
                else:
                    debug_log(f"Failed to install {tool_name}: {result.stderr}", "WARNING")
                    print("[warn] Installation failed")
            except subprocess.TimeoutExpired:
                debug_log(f"Timeout installing {tool_name}", "WARNING")
                print("[warn] Timeout")
            except Exception as e:
                debug_log(f"Error installing {tool_name}: {e}", "ERROR")
                print("[fail] Error")

    debug_log(f"Completed {category_name}: {installed_count}/{total_count} tools installed", "INFO")
    print(f"\n{category_name.title()} summary: {installed_count}/{total_count} tools installed")
    return installed_count, total_count


def ensure_rust_toolchain():
    """rustup's installer does not download a toolchain until asked."""
    if not check_command_exists("rustup"):
        debug_log("rustup not found, skipping toolchain install", "WARNING")
        return
    if check_command_exists("rustc"):
        debug_log("rustc already installed", "INFO")
        print("[ok] Rust toolchain already installed")
        return
    run_command(
        "rustup default stable",
        "Installing the stable Rust toolchain",
        allow_failure=True,
        timeout=WINGET_TIMEOUT_SECONDS,
    )


def install_scoop():
    """Install Scoop itself. The official installer refuses an elevated shell without -RunAsAdmin."""
    if check_command_exists("scoop"):
        debug_log("Scoop is already installed", "INFO")
        print("[ok] Scoop already installed")
        return True

    debug_log("Installing Scoop with the official installer", "INFO")
    print("\nInstalling Scoop")
    script = "& {$(irm get.scoop.sh)} -RunAsAdmin"
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script],
            capture_output=True,
            text=True,
            timeout=WINGET_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        debug_log("Timeout installing Scoop", "ERROR")
        print("[fail] Scoop install timed out")
        return False
    except Exception as e:
        debug_log(f"Error installing Scoop: {e}", "ERROR")
        print(f"[fail] Scoop install error: {e}")
        return False

    if result.stdout:
        debug_log(result.stdout, "DEBUG")
    if result.stderr:
        debug_log(result.stderr, "DEBUG")

    refresh_process_path()
    if result.returncode != 0 or not check_command_exists("scoop"):
        debug_log(f"Scoop install failed with exit code {result.returncode}", "ERROR")
        print("[fail] Scoop did not install. Scoop packages will be skipped.")
        return False

    print("[ok] Scoop installed")
    return True


def install_npcap_from_scoop_nmap():
    """Nmap's Scoop package bundles Npcap and does not install the driver itself."""
    if os.path.isdir(r"C:\Program Files\Npcap") or os.path.isdir(r"C:\Program Files\Npcap OEM"):
        debug_log("Npcap directory already present", "INFO")
        print("[ok] Npcap already installed")
        return

    roots = []
    userprofile = os.environ.get("USERPROFILE", "")
    if userprofile:
        roots.append(os.path.join(userprofile, "scoop", "apps", "nmap", "current"))
    programdata = os.environ.get("ProgramData", r"C:\ProgramData")
    roots.append(os.path.join(programdata, "scoop", "apps", "nmap", "current"))

    installer = None
    for root in roots:
        if not os.path.isdir(root):
            continue
        for name in os.listdir(root):
            if name.lower().startswith("npcap") and name.lower().endswith(".exe"):
                installer = os.path.join(root, name)
                break
        if installer:
            break

    if not installer:
        debug_log("Npcap installer was not found next to Scoop's Nmap", "WARNING")
        print("[warn] Npcap installer not found. Packet capture needs Npcap installed by hand.")
        return

    debug_log(f"Installing Npcap from {installer}", "INFO")
    print(f"  - Npcap from {installer}...", end=" ")
    try:
        result = subprocess.run(
            [installer, "/S", "/winpcap_mode=yes"],
            capture_output=True,
            text=True,
            timeout=WINGET_TIMEOUT_SECONDS,
        )
        if result.returncode in (0, 3010):
            debug_log("Npcap installed", "INFO")
            print("[ok] Installed")
        else:
            debug_log(f"Npcap install exited {result.returncode}: {result.stderr}", "WARNING")
            print("[warn] Installation failed")
    except subprocess.TimeoutExpired:
        debug_log("Timeout installing Npcap", "WARNING")
        print("[warn] Timeout")
    except Exception as e:
        debug_log(f"Error installing Npcap: {e}", "ERROR")
        print(f"[fail] Error: {e}")


def install_scoop_packages():
    """Install tools from Scoop's main and extras buckets."""
    debug_log("Starting Scoop package installation", "INFO")
    print("\nScoop packages")
    print("=" * 60)

    if not install_scoop():
        return 0, len(SCOOP_PACKAGES)

    try:
        bucket = subprocess.run(
            "scoop bucket add extras",
            shell=True,
            capture_output=True,
            text=True,
            timeout=180,
        )
        debug_log(f"scoop bucket add extras exited {bucket.returncode}", "DEBUG")
        if bucket.stdout:
            debug_log(bucket.stdout, "DEBUG")
        if bucket.stderr:
            debug_log(bucket.stderr, "DEBUG")
    except subprocess.TimeoutExpired:
        debug_log("Timeout adding the Scoop extras bucket", "WARNING")
        print("[warn] Timed out adding the Scoop extras bucket")
    except Exception as e:
        debug_log(f"Error adding the Scoop extras bucket: {e}", "ERROR")
        print(f"[warn] Could not add the Scoop extras bucket: {e}")

    installed_count = 0
    total_count = len(SCOOP_PACKAGES)
    nmap_installed = False

    for package, tool_name, command_name in SCOOP_PACKAGES:
        debug_log(f"Processing Scoop package: {tool_name} ({package})", "DEBUG")
        print(f"  - {tool_name}...", end=" ")
        if command_name and check_command_exists(command_name):
            debug_log(f"{tool_name} already installed", "INFO")
            print("[ok] Already installed")
            installed_count += 1
            if package == "nmap":
                nmap_installed = True
            continue

        try:
            result = subprocess.run(
                f"scoop install {package}",
                shell=True,
                capture_output=True,
                text=True,
                timeout=SCOOP_TIMEOUT_SECONDS,
            )
            if result.returncode == 0:
                debug_log(f"Successfully installed {tool_name}", "INFO")
                print("[ok] Installed")
                installed_count += 1
                if package == "nmap":
                    nmap_installed = True
            else:
                debug_log(f"Failed to install {tool_name}: {result.stderr}", "WARNING")
                print("[warn] Installation failed")
        except subprocess.TimeoutExpired:
            debug_log(f"Timeout installing {tool_name}", "WARNING")
            print("[warn] Timeout")
        except Exception as e:
            debug_log(f"Error installing {tool_name}: {e}", "ERROR")
            print("[fail] Error")

    if nmap_installed:
        refresh_process_path()
        install_npcap_from_scoop_nmap()

    debug_log(f"Scoop packages completed: {installed_count}/{total_count}", "INFO")
    print(f"\nScoop summary: {installed_count}/{total_count} packages installed")
    return installed_count, total_count


def add_directory_to_machine_path(directory):
    """Append a directory to the machine PATH when it is not already there."""
    if os.name != "nt" or not directory or not os.path.isdir(directory):
        return False
    import winreg

    subkey = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
    access = winreg.KEY_READ | winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey, 0, access) as key:
            current, regtype = winreg.QueryValueEx(key, "Path")
            parts = [part for part in current.split(";") if part]
            if any(part.lower() == directory.lower() for part in parts):
                debug_log(f"Machine PATH already contains {directory}", "DEBUG")
                return True
            updated = ";".join(parts + [directory])
            winreg.SetValueEx(key, "Path", 0, regtype, updated)
    except OSError as e:
        debug_log(f"Could not update machine PATH: {e}", "ERROR")
        return False
    debug_log(f"Added to machine PATH: {directory}", "INFO")
    return True


def find_named_file(root, filename):
    """Return the first path under root whose file name matches, case-insensitive."""
    if not root or not os.path.isdir(root):
        return None
    target = filename.lower()
    for dirpath, _, files in os.walk(root):
        for name in files:
            if name.lower() == target:
                return os.path.join(dirpath, name)
    return None


def metasploit_console_path():
    """Path to msfconsole.bat when the framework is installed but not yet on PATH."""
    for directory in METASPLOIT_BIN_CANDIDATES:
        candidate = os.path.join(directory, "msfconsole.bat")
        if os.path.isfile(candidate):
            return candidate
    return None


def install_metasploit():
    """Install Metasploit Framework from Rapid7's official Windows MSI."""
    debug_log("Starting Metasploit Framework install", "INFO")
    print("\nMetasploit Framework")
    print("=" * 60)
    print(f"Source: {METASPLOIT_MSI_URL}")
    print("The MSI is about 400 MB. Antivirus often quarantines the install.")
    print(r"If it disappears, exclude C:\Tools\metasploit-framework and C:\metasploit-framework.")

    if check_command_exists("msfconsole") or metasploit_console_path():
        debug_log("Metasploit is already installed", "INFO")
        print("[ok] Already installed")
        console = metasploit_console_path()
        if console:
            add_directory_to_machine_path(os.path.dirname(console))
        return 1, 1

    script = r"""
$ErrorActionPreference = 'Stop'
$DownloadURL = 'https://windows.metasploit.com/metasploitframework-latest.msi'
$DownloadLocation = Join-Path $env:APPDATA 'Metasploit'
$LogLocation = Join-Path $DownloadLocation 'install.log'
New-Item -Path $DownloadLocation -ItemType Directory -Force | Out-Null
New-Item -Path 'C:\Tools' -ItemType Directory -Force | Out-Null
$Installer = Join-Path $DownloadLocation 'metasploit.msi'
Write-Output "Downloading $DownloadURL"
Invoke-WebRequest -UseBasicParsing -Uri $DownloadURL -OutFile $Installer
Write-Output "Installing $Installer"
$proc = Start-Process -FilePath "$env:SystemRoot\System32\msiexec.exe" -ArgumentList @(
    '/i', $Installer,
    '/qn',
    '/norestart',
    '/log', $LogLocation,
    'INSTALLLOCATION=C:\Tools'
) -Wait -PassThru
Write-Output "msiexec exit $($proc.ExitCode). Log: $LogLocation"
exit $proc.ExitCode
"""
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script],
            capture_output=True,
            text=True,
            timeout=METASPLOIT_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        debug_log("Timeout installing Metasploit", "ERROR")
        print("[warn] Timeout")
        return 0, 1
    except Exception as e:
        debug_log(f"Error installing Metasploit: {e}", "ERROR")
        print(f"[fail] Error: {e}")
        return 0, 1

    if result.stdout:
        debug_log(result.stdout, "DEBUG")
    if result.stderr:
        debug_log(result.stderr, "DEBUG")

    # 0 is success. 3010 is success with a reboot requested.
    if result.returncode in (0, 3010) or metasploit_console_path():
        console = metasploit_console_path()
        if console:
            add_directory_to_machine_path(os.path.dirname(console))
        refresh_process_path()
        debug_log("Metasploit installed", "INFO")
        print("[ok] Installed")
        return 1, 1

    debug_log(f"Metasploit install failed with exit code {result.returncode}", "ERROR")
    print(f"[warn] Installation failed (exit {result.returncode})")
    print(r"See %APPDATA%\Metasploit\install.log")
    return 0, 1


def install_john():
    """Install the official Openwall Windows build of John the Ripper."""
    debug_log("Starting John the Ripper install", "INFO")
    print("\nJohn the Ripper")
    print("=" * 60)
    print(f"Source: {JOHN_ZIP_URL}")

    if check_command_exists("john"):
        debug_log("John the Ripper is already installed", "INFO")
        print("[ok] Already installed")
        return 1, 1

    john_exe = find_named_file(JOHN_ROOT, "john.exe")
    if not john_exe:
        script = r"""
$ErrorActionPreference = 'Stop'
$Dest = 'C:\Tools\john'
$Zip = Join-Path $env:TEMP 'winX64_1_JtR.zip'
New-Item -Path 'C:\Tools' -ItemType Directory -Force | Out-Null
if (Test-Path $Dest) { Remove-Item -Path $Dest -Recurse -Force }
New-Item -Path $Dest -ItemType Directory -Force | Out-Null
Write-Output 'Downloading John the Ripper'
Invoke-WebRequest -UseBasicParsing -Uri 'https://github.com/openwall/john-packages/releases/latest/download/winX64_1_JtR.zip' -OutFile $Zip
Write-Output 'Extracting John the Ripper'
Expand-Archive -Path $Zip -DestinationPath $Dest -Force
"""
        try:
            result = subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script],
                capture_output=True,
                text=True,
                timeout=JOHN_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired:
            debug_log("Timeout installing John the Ripper", "ERROR")
            print("[warn] Timeout")
            return 0, 1
        except Exception as e:
            debug_log(f"Error installing John the Ripper: {e}", "ERROR")
            print(f"[fail] Error: {e}")
            return 0, 1

        if result.stdout:
            debug_log(result.stdout, "DEBUG")
        if result.stderr:
            debug_log(result.stderr, "DEBUG")
        if result.returncode != 0:
            debug_log(f"John download failed with exit code {result.returncode}", "ERROR")
            print(f"[warn] Installation failed (exit {result.returncode})")
            return 0, 1
        john_exe = find_named_file(JOHN_ROOT, "john.exe")

    if not john_exe:
        debug_log("john.exe was not found after extraction", "ERROR")
        print("[warn] john.exe was not in the archive")
        return 0, 1

    add_directory_to_machine_path(os.path.dirname(john_exe))
    refresh_process_path()
    debug_log(f"John the Ripper installed at {john_exe}", "INFO")
    print("[ok] Installed")
    return 1, 1


def install_python_packages():
    """Install Python packages for development and security"""
    debug_log("Starting Python package installation", "INFO")
    print("\nInstalling Python packages")
    print("=" * 60)

    if not check_command_exists("python"):
        debug_log("Python not found, skipping package installation", "WARNING")
        print("[warn] Python not found, skipping package installation")
        return 0, len(PYTHON_PACKAGES)

    installed_count = 0
    total_count = len(PYTHON_PACKAGES)

    batch_size = 5
    for i in range(0, len(PYTHON_PACKAGES), batch_size):
        batch = PYTHON_PACKAGES[i:i + batch_size]
        debug_log(f"Installing Python package batch: {batch}", "DEBUG")

        try:
            install_command = f"python -m pip install {' '.join(batch)} --upgrade"
            debug_log(f"Installing batch with command: {install_command}", "DEBUG")

            result = subprocess.run(
                install_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=WINGET_TIMEOUT_SECONDS,
            )
            if result.returncode == 0:
                installed_count += len(batch)
                debug_log(f"Successfully installed batch: {batch}", "INFO")
                print(f"[ok] Installed batch: {', '.join(batch)}")
            else:
                debug_log(f"Failed to install batch: {result.stderr}", "WARNING")
                print(f"[warn] Failed batch: {', '.join(batch)}")
        except subprocess.TimeoutExpired:
            debug_log(f"Timeout installing batch: {batch}", "WARNING")
            print(f"[warn] Timeout batch: {', '.join(batch)}")
        except Exception as e:
            debug_log(f"Error installing batch: {e}", "ERROR")
            print(f"[fail] Error batch: {', '.join(batch)}")

    debug_log(f"Python packages installation completed: {installed_count}/{total_count}", "INFO")
    print(f"\nPython packages summary: {installed_count}/{total_count} packages installed")
    return installed_count, total_count


def install_node_packages():
    """Install Node.js packages globally"""
    debug_log("Starting Node.js package installation", "INFO")
    print("\nInstalling Node.js packages")
    print("=" * 60)

    if not check_command_exists("npm"):
        debug_log("npm not found, skipping package installation", "WARNING")
        print("[warn] npm not found, skipping package installation")
        return 0, len(NODE_PACKAGES)

    installed_count = 0
    total_count = len(NODE_PACKAGES)

    for package in NODE_PACKAGES:
        debug_log(f"Installing Node.js package: {package}", "DEBUG")
        print(f"  - {package}...", end=" ")

        try:
            install_command = f"npm install -g {package}"
            debug_log(f"Installing with command: {install_command}", "DEBUG")

            result = subprocess.run(
                install_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=180,
            )
            if result.returncode == 0:
                installed_count += 1
                debug_log(f"Successfully installed {package}", "INFO")
                print("[ok] Installed")
            else:
                debug_log(f"Failed to install {package}: {result.stderr}", "WARNING")
                print("[warn] Failed")
        except subprocess.TimeoutExpired:
            debug_log(f"Timeout installing {package}", "WARNING")
            print("[warn] Timeout")
        except Exception as e:
            debug_log(f"Error installing {package}: {e}", "ERROR")
            print("[fail] Error")

    debug_log(f"Node.js packages installation completed: {installed_count}/{total_count}", "INFO")
    print(f"\nNode.js packages summary: {installed_count}/{total_count} packages installed")
    return installed_count, total_count


def install_editor_extensions():
    """Install the same extension list into every editor CLI that is present."""
    debug_log("Starting editor extension installation", "INFO")
    print("\nInstalling editor extensions")
    print("=" * 60)

    extensions = CODING_EXTENSIONS["vscode"]
    present = [editor for editor in EDITORS if check_command_exists(editor)]
    if not present:
        debug_log("No editor CLI found, skipping extension installation", "WARNING")
        print("[warn] Neither VS Code nor the Cursor CLI was found, skipping extensions")
        return 0, len(extensions)

    installed_count = 0
    total_count = len(extensions) * len(present)

    for editor in present:
        print(f"\n{editor}:")
        for extension in extensions:
            debug_log(f"Installing {editor} extension: {extension}", "DEBUG")
            print(f"  - {extension}...", end=" ")
            try:
                install_command = f"{editor} --install-extension {extension}"
                result = subprocess.run(
                    install_command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=90,
                )
                if result.returncode == 0:
                    installed_count += 1
                    debug_log(f"Successfully installed {extension} for {editor}", "INFO")
                    print("[ok] Installed")
                else:
                    debug_log(f"Failed to install {extension}: {result.stderr}", "WARNING")
                    print("[warn] Failed")
            except subprocess.TimeoutExpired:
                debug_log(f"Timeout installing {extension}", "WARNING")
                print("[warn] Timeout")
            except Exception as e:
                debug_log(f"Error installing {extension}: {e}", "ERROR")
                print("[fail] Error")

    debug_log(f"Editor extensions completed: {installed_count}/{total_count}", "INFO")
    print(f"\nEditor extensions summary: {installed_count}/{total_count} extensions installed")
    return installed_count, total_count


def discover_cloudflare_resources():
    """List common Cloudflare resources when Wrangler is installed and logged in."""
    debug_log("Starting Cloudflare resource discovery", "INFO")
    print("\nCloudflare resource discovery")
    print("=" * 60)

    if not check_command_exists("wrangler"):
        debug_log("Wrangler not found, skipping Cloudflare resource discovery", "WARNING")
        print("[warn] Wrangler not found, skipping Cloudflare resource discovery")
        return

    queries = [
        ("wrangler kv namespace list", "Listing KV namespaces"),
        ("wrangler d1 list", "Listing D1 databases"),
        ("wrangler r2 bucket list", "Listing R2 buckets"),
        ("wrangler hyperdrive list", "Listing Hyperdrive configs"),
        ("wrangler queues list", "Listing Queues"),
        ("wrangler pages project list", "Listing Pages projects"),
    ]
    for command, description in queries:
        run_command(command, description, allow_failure=True, timeout=120)


def main():
    """Main installation process - comprehensive toolkit setup"""
    log_filename = setup_logging()
    debug_log("Starting comprehensive toolkit installer", "INFO")
    debug_log(f"Debug log file: {log_filename}", "INFO")
    debug_log(f"Python version: {sys.version}", "DEBUG")
    debug_log(f"Script arguments: {sys.argv}", "DEBUG")
    debug_log(f"Current working directory: {os.getcwd()}", "DEBUG")

    print("Comprehensive toolkit installer")
    print("=" * 80)
    print("Installs a coding, cybersecurity, and pentesting toolkit.")
    print("Sources: winget, Scoop main/extras, pip, and npm.")
    print("=" * 80)

    debug_log("Checking administrator privileges", "INFO")
    if not is_admin():
        debug_log("Not running as admin, attempting to restart", "WARNING")
        if not run_as_admin():
            debug_log("Failed to restart as administrator", "ERROR")
            print("[fail] Cannot proceed without administrator privileges.")
            input("Press Enter to exit...")
            return
        return

    debug_log("Confirmed running as administrator", "INFO")
    print("[ok] Running as administrator")
    refresh_process_path()

    total_installed = 0
    total_available = 0

    debug_log("Starting core development tools", "INFO")
    installed, available = install_tool_category(
        "core",
        {"core": DEVELOPMENT_TOOLS["core"]},
        "Core development tools",
    )
    total_installed += installed
    total_available += available
    refresh_process_path()
    ensure_rust_toolchain()

    debug_log("Starting CLI tools", "INFO")
    installed, available = install_tool_category(
        "cli",
        {"cli": DEVELOPMENT_TOOLS["cli"]},
        "CLI tools",
    )
    total_installed += installed
    total_available += available

    debug_log("Starting containers", "INFO")
    installed, available = install_tool_category(
        "containers",
        {"containers": DEVELOPMENT_TOOLS["containers"]},
        "Container tools",
    )
    total_installed += installed
    total_available += available

    debug_log("Starting databases", "INFO")
    installed, available = install_tool_category(
        "databases",
        {"databases": DEVELOPMENT_TOOLS["databases"]},
        "Database tools",
    )
    total_installed += installed
    total_available += available

    debug_log("Starting cloud CLIs", "INFO")
    installed, available = install_tool_category(
        "cloud",
        {"cloud": DEVELOPMENT_TOOLS["cloud"]},
        "Cloud CLI tools",
    )
    total_installed += installed
    total_available += available

    debug_log("Starting security tools", "INFO")
    installed, available = install_tool_category(
        "security",
        SECURITY_TOOLS,
        "Security and pentesting tools",
    )
    total_installed += installed
    total_available += available

    debug_log("Starting system utilities", "INFO")
    installed, available = install_tool_category(
        "utilities",
        {"utilities": SYSTEM_UTILITIES},
        "System utilities",
    )
    total_installed += installed
    total_available += available

    refresh_process_path()

    debug_log("Starting Scoop packages", "INFO")
    installed, available = install_scoop_packages()
    total_installed += installed
    total_available += available
    refresh_process_path()

    debug_log("Starting Metasploit Framework", "INFO")
    installed, available = install_metasploit()
    total_installed += installed
    total_available += available

    debug_log("Starting John the Ripper", "INFO")
    installed, available = install_john()
    total_installed += installed
    total_available += available
    refresh_process_path()

    debug_log("Starting Python packages", "INFO")
    installed, available = install_python_packages()
    total_installed += installed
    total_available += available

    debug_log("Starting Node.js packages", "INFO")
    installed, available = install_node_packages()
    total_installed += installed
    total_available += available

    debug_log("Starting editor extensions", "INFO")
    installed, available = install_editor_extensions()
    total_installed += installed
    total_available += available

    discover_cloudflare_resources()

    debug_log("Installation process completed", "INFO")
    print("\nInstallation complete")
    print("=" * 80)
    print(f"Overall summary: {total_installed}/{total_available} tools installed")
    print("=" * 80)
    print("The machine now has installers for:")
    print("  - Languages and editors (Node.js LTS, Python 3.12, Go, Rust, JDK 21, VS Code)")
    print("  - Containers (Docker Desktop, WSL)")
    print("  - Databases (PostgreSQL 17, MongoDB tools, Redis, SQLite, DBeaver)")
    print("  - Cloud CLIs (AWS, Azure, Google Cloud, Terraform, cloudflared)")
    print("  - Network and web tools (Nmap, Wireshark, Burp Suite, ZAP, mitmproxy, ffuf, Maltego)")
    print("  - Frameworks (Metasploit Framework, John the Ripper, hashcat)")
    print("  - Forensics (Autopsy, OSFMount, Volatility Workbench, TestDisk, PhotoRec, YARA)")
    print("  - Reversing (Ghidra, x64dbg, ImHex, HxD, PE-bear, Resource Hacker, WinDbg)")
    print("  - Scoop CLIs (gobuster, feroxbuster, amass, jadx, gitleaks, grype)")
    print("  - Python, Node.js, and editor extensions")
    print("=" * 80)
    print("WinPcap is not installed. It is obsolete; Npcap comes from the Nmap Scoop bundle.")
    print("=" * 80)
    print("Next steps:")
    print("1. Restart so every installer can finish updating PATH")
    print("2. Open VS Code, or Cursor if its CLI is installed, and check the extensions")
    print("3. Check languages: node --version, python --version, go version, rustc --version, java -version")
    print("4. Check security tools: nmap --version, tshark --version, hashcat --version, john, msfconsole")
    print(f"5. Read the debug log: {log_filename}")
    print("=" * 80)

    debug_log("Installation completed, waiting for user input", "DEBUG")
    input("\nPress Enter to exit...")
    debug_log("Script execution finished", "INFO")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        debug_log("Installation cancelled by user (Ctrl+C)", "WARNING")
        print("\n\n[fail] Installation cancelled by user.")
        input("Press Enter to exit...")
    except Exception as e:
        debug_log(f"Unexpected error in main execution: {e}", "ERROR")
        print(f"\n[fail] Unexpected error: {e}")
        input("Press Enter to exit...")
