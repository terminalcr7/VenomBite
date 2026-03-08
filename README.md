#  MSFVenom Payload Generator - Enterprise Edition

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-red.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Kali%20Linux-black.svg)](https://kali.org)
[![Version](https://img.shields.io/badge/version-2.0-green.svg)]()

A professional, enterprise-grade automation tool for generating Metasploit payloads with advanced evasion techniques, session management, and comprehensive logging capabilities.

## Table of Contents
- [Features](#-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Advanced Features](#-advanced-features)
- [Configuration](#-configuration)
- [Examples](#-examples)
- [Troubleshooting](#-troubleshooting)
- [Security & Compliance](#-security--compliance)
- [Contributing](#-contributing)
- [License](#-license)
- [Disclaimer](#-disclaimer)

##  Features

### Core Capabilities
- **Multi-Platform Support**: Windows, Linux, Android, macOS, and Web payloads
- **Multiple Payload Types**: Reverse TCP, Reverse HTTP, Reverse HTTPS, Bind TCP
- **Staged/Stageless Options**: Choose between staged (smaller) or stageless (standalone) payloads
- **Format Variety**: EXE, DLL, PowerShell, Python, Bash, APK, and more
- **Encoder Support**: x86/shikata_ga_nai, x86/polymorphic, x64/xor with configurable iterations

### Advanced Features
- ** Custom Crypter**: AES-256 encryption with XOR fallback
- ** Multi-Encoder Chain**: Multiple encoding layers for better evasion
- ** Advanced Listener Management**: Auto-reconnect, multi-port listeners
- ** Parallel Generation**: Generate multiple payloads simultaneously
- ** Session Analytics**: Track and analyze payload sessions
- ** Payload Signing**: Cryptographic verification with HMAC-SHA256
- ** Smart Organization**: Session-based directory structure
- ** Comprehensive Logging**: Detailed audit trails
- ** Professional UI**: Colored output with intuitive menus

##  Architecture

```
MSFVENOM/
├── core/                      # Core modules
│   ├── generator.py           # Main payload generation engine
│   ├── validator.py           # Input validation
│   ├── executor.py            # Command execution
│   └── config_manager.py      # Configuration management
├── utils/                      # Utilities
│   ├── colors.py              # Terminal coloring
│   ├── ip_detector.py         # IP detection
│   ├── logger.py              # Logging system
│   └── file_organizer.py      # File management
├── obfuscators/                # Evasion techniques
│   ├── custom_crypter.py      # AES encryption
│   └── multi_encoder.py       # Encoder chains
├── listeners/                  # Listener management
│   └── rc_generator.py        # RC script generation
├── optimization/               # Performance
│   └── parallel_generator.py  # Parallel processing
├── payloads/                   # Generated payloads
│   └── session_*              # Session-specific directories
├── logs/                       # Application logs
├── main.py                     # Main application
└── requirements.txt            # Dependencies
```

## 💻 Installation

### Prerequisites
- Kali Linux (recommended) or any Debian-based Linux
- Python 3.6+
- Metasploit Framework
- Nmap (optional, for target profiling)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/msfvenom-payload-generator.git
cd msfvenom-payload-generator
```

### Step 2: Set Up Virtual Environment (Recommended for Kali)
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
# Install required Python packages
pip install -r requirements.txt

# Or install individually
pip install colorama requests netifaces python-dateutil pycryptodome
```

### Step 4: Install System Dependencies
```bash
sudo apt update
sudo apt install metasploit-framework nmap
```

### Step 5: Verify Installation
```bash
python3 main.py --test
```

##  Quick Start

### Interactive Mode (Recommended)
```bash
python3 main.py
```
Simply follow the interactive prompts to generate your payload.

### One-Line Generation
```bash
# Quick Windows reverse TCP payload
python3 main.py --quick --lhost 192.168.1.100 --lport 4444 --platform 1
```

## 📖 Usage Guide

### Main Menu Options

```
1.  Generate Payload     - Create new payloads interactively
2.  Check Dependencies   - Verify all required tools are installed
3.  Show Available       - List all supported payloads
4.  Exit                 - Exit the application
```

### Payload Generation Workflow

1. **IP Configuration**
   - Auto-detects local IP
   - Option to use WAN IP or custom IP
   - Validates IP format

2. **Port Selection**
   - Default: 4444
   - Range: 1-65535
   - Automatic validation

3. **Platform Selection**
   - 1: Windows
   - 2: Linux
   - 3: Android
   - 4: macOS
   - 5: Web

4. **Connection Type**
   - Reverse TCP (most common)
   - Reverse HTTP (firewall evasion)
   - Reverse HTTPS (encrypted)
   - Bind TCP (for restricted networks)

5. **Payload Type**
   - Staged (smaller, requires handler)
   - Stageless (larger, standalone)

6. **Output Format**
   - Platform-specific formats (exe, elf, apk, etc.)
   - Script formats (ps1, py, rb, etc.)

7. **Encoder Options**
   - No encoder
   - x86/shikata_ga_nai (polymorphic)
   - x86/polymorphic
   - x64/xor

8. **Advanced Options**
   - Encryption (if available)
   - Listener generation
   - Custom output filename

## 🔧 Advanced Features

### Custom Encryption
```python
# Automatically encrypts generated payloads
Apply encryption? (y/n): y
✓ Encrypted payload saved to payload.exe.encrypted
```

### Listener Generation
```python
# Creates Metasploit RC script
Generate listener script? (y/n): y
✓ Listener script saved to listeners/windows_tcp_4444.rc
# Run with: msfconsole -q -r listeners/windows_tcp_4444.rc
```

### Session Organization
```
payloads/
└── session_20260216_172753/
    ├── windows/
    │   └── payload.exe
    ├── listeners/
    │   └── windows_tcp_4444.rc
    └── encrypted/
        └── payload.exe.encrypted
```

### Parallel Generation (Batch Mode)
Create a JSON configuration file:
```json
[
    {
        "platform_key": "1",
        "payload_type_key": "1",
        "staged_key": "1",
        "lhost": "192.168.1.100",
        "lport": 4444,
        "format_type": "exe"
    },
    {
        "platform_key": "2",
        "payload_type_key": "1",
        "staged_key": "2",
        "lhost": "192.168.1.100",
        "lport": 4445,
        "format_type": "elf"
    }
]
```
Then run:
```bash
python3 main.py --batch config.json
```

## 📝 Configuration

### Requirements.txt
```txt
colorama>=0.4.6          # Colored terminal output
requests>=2.31.0         # HTTP requests for WAN IP detection
netifaces>=0.11.0        # Network interface detection
python-dateutil>=2.8.2   # Date handling
pycryptodome>=3.9.0      # AES encryption (optional)
```

### Environment Variables
```bash
# Optional: Set default values
export MSFVENOM_DEFAULT_LHOST="192.168.1.100"
export MSFVENOM_DEFAULT_LPORT="4444"
export MSFVENOM_OUTPUT_DIR="/path/to/payloads"
```

##  Examples

### Generate Windows Reverse HTTPS Payload
```bash
# Interactive selection:
# Platform: 1 (Windows)
# Type: 3 (reverse_https)
# Staged: 1 (Staged)
# Format: 1 (exe)
# Encoder: 2 (x86/shikata_ga_nai)
```

### Generate Linux Stageless Payload
```bash
# Interactive selection:
# Platform: 2 (Linux)
# Type: 1 (reverse_tcp)
# Staged: 2 (Stageless)
# Format: elf
# Encoder: None
```

### Generate Android APK with Evasion
```bash
# Interactive selection:
# Platform: 3 (Android)
# Type: 1 (reverse_tcp)
# Staged: 2 (Stageless)
# Format: apk
# Encoder: 2 (x86/shikata_ga_nai)
# Apply encryption: y
```

##  Troubleshooting

### Common Issues

#### 1. "msfvenom not found"
```bash
sudo apt update
sudo apt install metasploit-framework
```

#### 2. "externally-managed-environment" (Kali Linux)
```bash
# Use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3. "No module named 'Crypto'"
```bash
pip install pycryptodome
# or
sudo apt install python3-pycryptodome
```

#### 4. Permission Denied
```bash
chmod +x main.py
chmod +x set.sh
```

#### 5. Colors Not Displaying Properly
```bash
# Ensure colorama is installed
pip install colorama

# For Windows terminals, enable ANSI support
```

### Debug Mode
```bash
python3 main.py --debug
```

##  Security & Compliance

### Legal Requirements
- **Always obtain written authorization** before testing any system
- Use only on systems you own or have explicit permission to test
- Maintain proper documentation of all tests
- Follow responsible disclosure practices

### Audit Trail
All actions are logged:
```
logs/
├── payload_generator.log    # Main application log
├── sessions.db              # Session analytics database
└── audit/                   # Compliance logs
    └── YYYY-MM-DD/
        └── actions.log
```

### Best Practices
1. **Use VPN/Proxy** for anonymity during testing
2. **Encrypt sensitive payloads** before transmission
3. **Delete test artifacts** after assessment completion
4. **Regularly update** Metasploit and dependencies
5. **Use strong passwords** for listener services

##  Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add comments for complex logic
- Update documentation for new features
- Include unit tests where possible
- Test on Kali Linux before submitting

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Disclaimer

**IMPORTANT: READ CAREFULLY BEFORE USE**

This tool is designed **SOLELY** for:
- Authorized penetration testing
- Security research and education
- System administration and defense testing

**By using this software, you agree to:**

1. **Only test systems you own** or have explicit written permission to test
2. **Comply with all applicable laws** and regulations in your jurisdiction
3. **Take full responsibility** for your actions and any consequences
4. **Not use this tool** for any illegal or unauthorized purposes
5. **Maintain proper documentation** of all testing activities

**The developers and contributors:**
- Are NOT responsible for misuse or illegal activities
- Provide NO warranty, express or implied
- Assume NO liability for damages or legal consequences
- Reserve the right to deny support to anyone

**Unauthorized use may violate:**
- Computer Fraud and Abuse Act (CFAA)
- GDPR and data protection laws
- Local and international cybercrime laws
- Terms of service of cloud providers
- Network acceptable use policies

**If you do not have authorization, STOP immediately.**

## Support

- **Documentation**: See this README
- **Issues**:Talk to the team

##  Acknowledgments

- Metasploit Framework Team
- Rapid7
- Kali Linux Team
- Open Source Community

##  Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | 2026-02-16 | Enterprise release with encryption, parallel generation, analytics |
| 1.5 | 2026-01-15 | Added listener management, improved UI |
| 1.0 | 2025-12-01 | Initial release with core functionality |

---

**Made with  for security professionals**
