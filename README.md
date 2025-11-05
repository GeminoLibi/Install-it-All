# Install-It-All

*For the Lazy and Negligent — and the impatient builder, hacker, or pentester*

Install-It-All is a comprehensive Windows installer script for rapid setup of a full coding, cybersecurity, and pentesting environment. Whether you're spinning up a fresh dev box or prepping a security lab, it saves hours, automating installations of:

- Major languages/runtimes (Node.js, Python, Git, VS Code, Docker, WSL2, PowerShell, etc.)
- Security and pentesting tools (Nmap, Wireshark, Metasploit, Burp Suite, OWASP ZAP, Autopsy, Volatility, etc.)
- Cloud CLIs (AWS, Azure, Google Cloud)
- Databases (PostgreSQL, MongoDB Tools, Redis)
- Dev productivity utilities (PowerToys, .NET 8 SDK, PyCharm, IntelliJ, Sublime, Notepad++, Figma, OBS Studio)
- Python packages for security, automation, and data analysis
- Node.js global packages for web dev and CLI work
- VS Code extensions for every imaginable task

---

## How It Works

This script will:

1. **Verify Administrative Privileges**
2. **Install Core Development Tools**
3. **Refresh Windows Environment Variables**
4. **Install Containers (Docker Desktop, WSL2)**
5. **Install Database Clients**
6. **Install Cloud Provider CLI Tools**
7. **Install Security and Pentesting Tools**
8. **Install Desktop Productivity Utilities**
9. **Batch install Python and Node.js packages globally**
10. **Install a hand-curated set of VS Code extensions**
11. **Run project-specific resource queries (Cloudflare Wrangler integration) if relevant directories are found**
12. **Summarize installation and give next steps (including what to test, restart reminders, and log file location)**

Everything is logged to a timestamped debug file, and failures prompt you interactively.

---

## Requirements

- **Windows 10/11**
- **Administrator rights**
- **`winget` installed and available in your PATH**
- **Internet access (for package downloads)**

---

## Usage

Download or clone:

```sh
git clone https://github.com/GeminoLibi/Install-it-All.git
cd Install-it-All
```

Run as admin (either from an elevated shell, or the script will prompt/relaunch itself with UAC):

```sh
python install-it-all.py
```

Just follow the prompts. Everything essential is automatic; optional errors (like a failed package install) give you the option to skip, retry, or cancel.

---

## What Gets Installed?

### Dev Tools

- Node.js (with npm/yarn/pnpm)
- Python 3.12 (with pip/setuptools/wheel and a long list of libraries)
- Git, VS Code, Windows Terminal, PowerShell 7

### Containers & Databases

- Docker Desktop
- Windows Subsystem for Linux (WSL2)
- PostgreSQL, MongoDB Tools, Redis

### Cloud Access

- AWS CLI
- Azure CLI
- Google Cloud SDK

### Security & Forensics

- Nmap, Wireshark, Metasploit, Burp Suite, OWASP ZAP, Autopsy, Volatility, 7-Zip, GnuPG, Vault

### Utilities

- PowerToys, .NET 8 SDK, IntelliJ IDEA Community, PyCharm Community, Sublime Text, Notepad++, Figma, OBS Studio

### Packages

- Python: Requests, BS4, Selenium, Pandas, Numpy, Matplotlib, Flask, Django, FastAPI, Cryptography, PyCryptodome, and many tools for security and automation
- Node.js: Typescript, ESLint, Prettier, Nodemon, Express, React, Vue, Angular, Jest, Mocha, Cypress, Wrangler, Vercel, Netlify CLI

### VS Code Extensions

See [install-it-all.py](https://github.com/GeminoLibi/Install-it-All/blob/main/install-it-all.py) for the full handpicked list or modify to suit your workflow.

---

## Customizations

- Edit the lists (`DEVELOPMENT_TOOLS`, `SECURITY_TOOLS`, `PYTHON_PACKAGES`, `NODE_PACKAGES`, `CODING_EXTENSIONS`, `SYSTEM_UTILITIES`) directly in the script to add, remove, or adjust tools.
- Project-specific resource scanning is tailored for "project-revelare-web": change `project_dir` or add new paths to integrate your own post-install logic.

---

## Troubleshooting

- **Can't run some commands?** Make sure you're administrator.
- **Winget or Python not available?** Install manually before running this script.
- **Cloudflare Wrangler errors?** Only runs if you have the project directory and Wrangler CLI installed.
- **Log files:** Every run generates a detailed debug log, check `install_debug_<timestamp>.log`.
- **Failed install?** Interactive error handling lets you skip, retry, or abort any step — it's designed to tolerate unreliable internet and installer quirks.

---

## Next Steps After Install

1. **Restart your PC** to refresh your PATH.
2. **Open VS Code** and explore extensions/features.
3. **Verify installs:** Try commands like `node --version`, `python --version`, `git --version`
4. **Test security tools:** e.g., `nmap --version`, `wireshark --version`
5. **Configure Cloudflare resources:** update `wrangler.json` with your actual project IDs
6. **Check log files** for any installation issues or errors.

---

## License

MIT

---

## Author

[@GeminoLibi](https://github.com/GeminoLibi)
