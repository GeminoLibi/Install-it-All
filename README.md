# Install-It-All

*For the Lazy and Negligent - and the impatient builder, hacker, or pentester*

Install-It-All is a Windows installer for a coding, cybersecurity, and pentesting toolkit. It is a general swiss army knife, not a setup script for one project. On a fresh box it installs:

- Languages and editors (Node.js LTS, Python 3.12, Go, Rust, JDK 21, Git, VS Code, PowerShell 7)
- Security and pentesting tools (Nmap, Wireshark, Burp Suite, ZAP, mitmproxy, ffuf, and more from Scoop)
- Forensics and reversing tools (Autopsy, ExifTool, Ghidra, x64dbg, ImHex, WinDbg, Sysinternals)
- Cloud CLIs (AWS, Azure, Google Cloud, Terraform, cloudflared)
- Databases (PostgreSQL 17, MongoDB tools, Redis, SQLite, DBeaver)
- Dev utilities (PowerToys, .NET 8 and .NET 10 SDKs, PyCharm, IntelliJ, Sublime, Notepad++, Figma, OBS, PuTTY, WinSCP)
- Python packages for security, automation, and development
- Node.js global packages for web development and CLI work
- Editor extensions for VS Code, and for Cursor when its `cursor` command is already on PATH

---

## How It Works

This script will:

1. **Request administrator permission** if the window is not already elevated, then continue in that elevated window
2. **Install core languages and editors with winget**
3. **Reload PATH from the registry** and install the stable Rust toolchain when rustup is new
4. **Install CLI, container, database, and cloud tools**
5. **Install security, forensics, and reversing tools**
6. **Install desktop utilities**
7. **Install Scoop, then tools that winget does not publish** (or only publishes as a stale build)
8. **Install Npcap from the Nmap Scoop bundle** when that installer is present and Npcap is missing
9. **Install Metasploit Framework** from Rapid7's official Windows MSI
10. **Install John the Ripper** from Openwall's official Windows build and add it to PATH
11. **Batch-install Python and Node.js packages**
12. **Install editor extensions**
13. **List Cloudflare resources** when the Wrangler CLI is on PATH and already logged in
14. **Print a summary** with restart notes and the log path

Everything is logged to a timestamped debug file. The file is written next to the script when that folder is writable. If the script is on a drive root such as `C:\`, the log goes to `%LOCALAPPDATA%\Install-It-All` instead. A failed interactive command asks whether to continue. Per-package winget and Scoop failures are logged and skipped.

---

## Requirements

- **Windows 10/11**
- **Administrator rights**
- **`winget` installed and available in your PATH**
- **Internet access (for package downloads)**

Scoop is installed by the script. It does not need to be present beforehand.

---

## Usage

Download or clone:

```sh
git clone https://github.com/GeminoLibi/Install-it-All.git
cd Install-it-All
```

Run it from a normal terminal. If the window is not already elevated, Windows asks for administrator permission and the script continues in a new window:

```sh
python install-it-all.py
```

Follow the prompts. Optional package failures are recorded in the log and the run continues.

---

## What Gets Installed?

### Dev tools

- Node.js LTS (with npm, yarn, and pnpm)
- Python 3.12 (with pip and the package list in the script)
- Go, Rustup (then the stable toolchain), Temurin JDK 21, uv, Ruff, CMake
- Git, GitHub CLI, VS Code, Windows Terminal, PowerShell 7
- ripgrep, fd, and jq

### Containers and databases

- Docker Desktop
- Windows Subsystem for Linux
- PostgreSQL 17, MongoDB Database Tools, Redis, SQLite, DBeaver Community, DB Browser for SQLite

The winget Redis package is the legacy Windows port (3.0.504). It is the Redis build winget still publishes.

### Cloud

- AWS CLI, Azure CLI, Google Cloud SDK
- Terraform, Vault, cloudflared

### Security, forensics, and reversing

From winget:

- Wireshark, Burp Suite, ZAP, mitmproxy, ffuf, Maltego
- Autopsy (includes The Sleuth Kit), OSFMount, Volatility Workbench, TestDisk, PhotoRec
- ExifTool, YARA, VirusTotal CLI, Tesseract OCR, FFmpeg, WinDbg
- x64dbg, ImHex, HxD, PE-bear, Resource Hacker, Detect It Easy, System Informer
- 7-Zip, Gpg4win, Sysinternals Suite, KeePassXC, VeraCrypt

From Scoop's official `main` and `extras` buckets:

- Nmap (current build; winget's Nmap package is still 7.80), plus the bundled Npcap driver when it is not already installed
- hashcat, gobuster, feroxbuster, amass, chisel
- apktool, jadx, Ghidra, Cutter, CyberChef
- gitleaks, Grype, cosign

### Official installers outside winget and Scoop

- **Metasploit Framework.** Rapid7's nightly MSI (`https://windows.metasploit.com/metasploitframework-latest.msi`), installed silently under `C:\Tools`. The download is about 400 MB. `msfconsole` is added to PATH. The MSI is kept in `%APPDATA%\Metasploit`.
- **John the Ripper.** Openwall's official Windows jumbo build, extracted to `C:\Tools\john`, with the `john.exe` directory added to the machine PATH.

### Not installed automatically

- **WinPcap.** It is obsolete. Npcap replaces it.

### Utilities

- PowerToys, .NET 8 SDK, .NET 10 SDK
- IntelliJ IDEA Community, PyCharm Community, Sublime Text, Notepad++
- Figma, OBS Studio, PuTTY, WinSCP, Everything

### Packages

- Python: requests, Beautiful Soup, Selenium, pandas, NumPy, Matplotlib, Flask, Django, FastAPI, cryptography, Scapy, Impacket, sqlmap, Volatility 3, oletools, LIEF, python-registry, theHarvester, and related libraries
- Node.js: TypeScript, ESLint, Prettier, Nodemon, Express, React, Vue, Angular, Jest, Mocha, Cypress, Wrangler, Vercel, Netlify CLI

### Editor extensions

See [install-it-all.py](https://github.com/GeminoLibi/Install-it-All/blob/main/install-it-all.py) for the list. The same set is installed for `code` and, when that command exists, for `cursor`.

---

## Customizations

Edit the lists in the script:

- `DEVELOPMENT_TOOLS`
- `SECURITY_TOOLS`
- `SCOOP_PACKAGES`
- `PYTHON_PACKAGES`
- `NODE_PACKAGES`
- `CODING_EXTENSIONS`
- `SYSTEM_UTILITIES`

Scoop packages must exist in the official `main` or `extras` bucket. The script does not add third-party buckets.

---

## Troubleshooting

- **Access denied as soon as it starts?** Approve the administrator prompt. The script relaunches itself with UAC; it does not keep running in the window that Windows refused to elevate. If the prompt never appears and the `python` command is the Microsoft Store alias, install Python from python.org or run `py -3 install-it-all.py`.
- **Can't run some commands later?** The installer has to stay in that administrator window. A second, non-elevated terminal will not see the same permissions.
- **Winget or Python not available?** Install those before running this script.
- **A package failed?** Check `install_debug_<timestamp>.log` next to the script, or under `%LOCALAPPDATA%\Install-It-All` when the script folder cannot accept new files. Winget ids are exact (`--id` and `-e`), so a renamed package fails instead of installing a different one.
- **Permission denied creating `C:\install_debug_....log`?** That was the log being opened before elevation. Run the current script; it asks for administrator permission first and does not write the log on the drive root.
- **Scoop failed?** The installer is the official `get.scoop.sh` script with `-RunAsAdmin`, which is required because this run is elevated.
- **Nmap capture does not work?** Npcap has to be installed. The script runs the Npcap installer shipped inside Scoop's Nmap app when `C:\Program Files\Npcap` is missing. If that file is not in the bundle, install Npcap by hand.
- **Ghidra does not start?** It needs JDK 21 on PATH. The script installs Temurin 21 before Scoop's Ghidra package. Restart the terminal after the run.
- **Metasploit or John disappeared after install?** Antivirus quarantines both. Exclude `C:\Tools\metasploit-framework`, `C:\metasploit-framework`, and `C:\Tools\john`, then run the script again. Metasploit's MSI log is `%APPDATA%\Metasploit\install.log`.
- **`john` or `msfconsole` is not found?** Restart the terminal. Both installers update the machine PATH, which already-open shells do not see.
- **Cloudflare commands failed?** Wrangler has to be installed and logged in (`wrangler login`). The listing commands are skipped when Wrangler is absent, and a failed query does not stop the run.
- **Redis is very old?** That is the package winget still ships for Windows.

---

## Next Steps After Install

1. **Restart** so PATH updates from every installer are picked up.
2. **Open VS Code** and look through the extensions.
3. **Check the languages:** `node --version`, `python --version`, `go version`, `rustc --version`, `java -version`
4. **Check a few security tools:** `nmap --version`, `tshark --version`, `hashcat --version`, `john`, `msfconsole`
5. **Read the log** if anything was skipped.

---

## License

MIT

---

## Author

[@GeminoLibi](https://github.com/GeminoLibi)
