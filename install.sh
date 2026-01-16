#!/data/data/com.termux/files/usr/bin/bash

echo -e "\033[1;36m"
echo "╔═══════════════════════════════════════════════════╗"
echo "║          RAX OSINT Tool Installer                ║"
echo "║               Version 2.0                        ║"
echo "║               by TEAM RAX                        ║"
echo "╚═══════════════════════════════════════════════════╝"
echo -e "\033[0m"

sleep 2

echo -e "\033[1;33m[+] Updating Termux packages...\033[0m"
pkg update -y && pkg upgrade -y

echo -e "\033[1;33m[+] Installing Python...\033[0m"
pkg install python -y

echo -e "\033[1;33m[+] Installing required packages...\033[0m"
pkg install git -y
pkg install nano -y

echo -e "\033[1;33m[+] Installing Python dependencies...\033[0m"
pip install rich requests pyfiglet colorama

echo -e "\033[1;33m[+] Creating directory...\033[0m"
mkdir -p ~/rax-osint-tool
cd ~/rax-osint-tool

echo -e "\033[1;33m[+] Downloading tool...\033[0m"
curl -s -o rax_osint.py https://raw.githubusercontent.com/teamrax/osint-tool/main/rax_osint.py

echo -e "\033[1;33m[+] Making it executable...\033[0m"
chmod +x rax_osint.py

echo -e "\033[1;33m[+] Creating launcher...\033[0m"
cat > ~/../usr/bin/rax-osint << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
cd ~/rax-osint-tool
python rax_osint.py
EOF

chmod +x ~/../usr/bin/rax-osint

echo -e "\033[1;32m"
echo "╔═══════════════════════════════════════════════════╗"
echo "║          INSTALLATION COMPLETE!                  ║"
echo "╠═══════════════════════════════════════════════════╣"
echo "║                                                   ║"
echo "║  To run the tool, type:                          ║"
echo "║  \033[1;36m$ rax-osint\033[1;32m                                 ║"
echo "║                                                   ║"
echo "║  Features:                                       ║"
echo "║  • Beautiful TUI interface                       ║"
echo "║  • 15+ OSINT search types                        ║"
echo "║  • Fast & efficient                              ║"
echo "║  • Free to use                                   ║"
echo "║                                                   ║"
echo "║  Need help? Contact: @TEAM_RAX                   ║"
echo "║                                                   ║"
echo "╚═══════════════════════════════════════════════════╝"
echo -e "\033[0m"