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

#prep wordlists
sudo gunzip /usr/share/wordlists/rockyou.txt.gz
sudo apt install -y seclists

#upload and enumeration scripts
cd /opt
sudo git clone https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite.git
sudo git clone https://github.com/rebootuser/LinEnum.git
sudo mkdir pspy
cd pspy
sudo wget https://github.com/DominicBreuker/pspy/releases/download/v1.2.0/pspy32
sudo wget https://github.com/DominicBreuker/pspy/releases/download/v1.2.0/pspy64
sudo wget https://github.com/DominicBreuker/pspy/releases/download/v1.2.0/pspy32s
sudo wget https://github.com/DominicBreuker/pspy/releases/download/v1.2.0/pspy64s
cd ~/

#rustscan
wget https://github.com/RustScan/RustScan/releases/download/2.0.1/rustscan_2.0.1_amd64.deb
sudo apt install -y ./rustscan_2.0.1_amd64.deb 
rm rustscan_2.0.1_amd64.deb
