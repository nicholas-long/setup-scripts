#!/bin/bash

#install nvidia drivers
sudo apt install nvidia-opencl-dev nvidia-opencl-common
sudo apt install -y nvidia-driver nvidia-cuda-toolkit\n

#install sublime
wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
sudo apt-get install apt-transport-https
echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
sudo apt-get update
sudo apt-get install sublime-text

#install vs code
cd ~/
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt install apt-transport-https
sudo apt update
sudo apt install code # or code-insiders


#prep wordlists
sudo gunzip /usr/share/wordlists/rockyou.txt.gz
sudo apt install -y seclists

#upload and enumeration scripts
cd /opt
sudo git clone https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite.git
sudo git clone https://github.com/rebootuser/LinEnum.git
sudo git clone https://github.com/pentestmonkey/php-reverse-shell.git
sudo mkdir pspy
cd pspy
sudo wget https://github.com/DominicBreuker/pspy/releases/download/v1.2.0/pspy32
sudo wget https://github.com/DominicBreuker/pspy/releases/download/v1.2.0/pspy64
sudo wget https://github.com/DominicBreuker/pspy/releases/download/v1.2.0/pspy32s
sudo wget https://github.com/DominicBreuker/pspy/releases/download/v1.2.0/pspy64s
cd ~/

#install necessary tools
sudo apt install -y python3-pip

#install useful tools that should be here
sudo apt install -y gobuster 
sudo apt install -y ffuf
#need this for some CTFs that hide stuff in images
sudo apt install -y steghide
sudo apt install -y libimage-exiftool-perl


#rustscan
wget https://github.com/RustScan/RustScan/releases/download/2.0.1/rustscan_2.0.1_amd64.deb
sudo apt install -y ./rustscan_2.0.1_amd64.deb 
rm rustscan_2.0.1_amd64.deb

#set up aliases
cd ~/
echo '' >> .zshrc
echo 'if [ -f ~/.bash_aliases ]; then' >> .zshrc
echo '    . ~/.bash_aliases' >> .zshrc
echo 'fi' >> .zshrc
