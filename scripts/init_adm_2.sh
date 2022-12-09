#!/usr/bin/env bash
printf '\n##### Installing packets for admin panel #####\n'
sudo apt-get -y install xorgxrdp xrdp >> ~/install_log.txt
sudo apt-get -y install curl git >> ~/install_log.txt
printf '\n##### Installing packets for python #####\n'
sudo apt-get -y install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
printf '\n##### All packets have been installed #####\n'
printf '\n##### Installing python #####\n'
tar -xvzf Python-3.9.10.tgz -C ~/
cd ~/Python-3.9.10/
./configure \
    --prefix=/opt/python/3.9.10 \
    --enable-shared \
    --enable-optimizations \
    --enable-ipv6 \
    LDFLAGS=-Wl,-rpath=/opt/python/3.9.10/lib,--disable-new-dtags
make
sudo make install
echo 'export PATH=/opt/python/3.9.10/bin/:$PATH' >> ~/.bashrc
#export PATH=/opt/python/3.9.10/bin/:$PATH >> ~/.bashrc
. ~/.bashrc
python3 --version
cd ~/admConsole/
pip3 install -r requirements.txt >> ~/install_log.txt
cp run.sh ~/Desktop/
chmod +x ~/Desktop/run.sh
date
printf '\n##### Add rights to start/stop OMEGA #####\n'
echo 'omega ALL=(ALL) NOPASSWD: /bin/systemctl * omega' | sudo EDITOR='tee -a' visudo
printf '\n##### Rights added #####\n'
printf '\n##### Admin panel installed successfully #####\n'
#lsof -i :5000
exit 0