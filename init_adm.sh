#!/usr/bin/env bash
printf '\n##### Installing packets for admin panel #####\n'
sudo apt-get -y install xorgxrdp xrdp >> ~/install_log.txt
sudo apt-get -y install curl git >> ~/install_log.txt
curl https://pyenv.run | bash >> ~/install_log.txt 1>&2
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
#tail -n 10 ~/.bashrc
export PYENV_ROOT="$HOME/.pyenv"
#echo $PYENV_ROOT
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
printf '\n##### Restart bash #####\n'
#exec "$SHELL"
. ~/.bashrc
printf '\n##### Installing packets for python #####\n'
sudo apt-get -y install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev >> ~/install_log.txt
printf '\n##### All packets have been installed #####\n'
printf '\n##### Installing python #####\n'
pyenv install 3.9.10
printf '\n##### Python have been installed #####\n'
pyenv global 3.9.10
python --version
cd ~
unzip ~/admConsole-tray.zip >> ~/install_log.txt
cd ~/admConsole-tray/
pip install -r requirements.txt >> ~/install_log.txt
cd ~
cp adm.sh ~/Desktop/
chmod +x ~/Desktop/adm.sh
date
#lsof -i :5000
exit 0