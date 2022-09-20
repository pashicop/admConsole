#!/usr/bin/env bash
printf '##### Start installing OMEGA #####\n'
printf '\n##### UPDATE packets #####'
printf '\n##### It may take a long time!! #####'
printf '\n##### Please wait! \n\n#####'
sudo systemctl start ntp > ~/install_log.txt
sudo systemctl enable ntp >> ~/install_log.txt
sudo systemctl status ntp >> ~/install_log.txt
date
sudo apt-get update >> ~/install_log.txt &&
sudo apt-get -y install openssh-server >> ~/install_log.txt &&
sudo apt-get -y install postgresql >> ~/install_log.txt
if [[ $? == 0 ]]
  then printf '\n##### Update packets done! ######\n'
  else printf '\n##### Error with updating packets #####\n'
  exit 1
fi
printf '\n##### CREATE DB #####'
printf '\n##### COPY init script #####'
sudo cp ~/Omega/init_db /etc/postgresql
printf '\n##### OK! #####\n'
printf "\n##### Changing script's owner #####"
sudo chown postgres /etc/postgresql/init_db
printf '\n##### OK! #####\n'
printf '\n##### Running script! #####'
sudo -u postgres psql -f /etc/postgresql/init_db >> ~/install_log.txt 2>&1
if [[ $? == 0 ]]
  then printf '\n##### DB CREATED! ######\n'
  else printf '\n##### Error with creating DB #####\n'
  exit 2
fi
printf '\n##### Deleting tmp files! #####'
rm ~/Omega/init_db
sudo rm /etc/postgresql/init_db
printf '\n##### OK! #####\n'
printf '\n##### EDITING postgres config #####'
sudo sed -i.bak 's/^local\s*all\s*all\s*peer$/local all all md5/' /etc/postgresql/9.6/main/pg_hba.conf
printf '\n##### OK! #####\n'
printf '\n##### Restarting postgresql #####'
sudo systemctl restart postgresql
printf '\n##### OK! #####\n'
printf '\n##### CREATE DB SCHEME! #####'
cd ~/Omega &&
export PGPASSWORD=omega1q2w &&
psql -d omega_db -U omega_user -f create_script >> ~/install_log.txt &&
unset PGPASSWORD
printf '\n##### OK! #####\n'
printf '\n##### First run #####'
chmod +x first_run run Api TimeoutManager
./first_run
printf '\n##### First run OK! #####\n'
#./run
#if [[ $? == 0 ]]
#  then export ip_host=$(hostname -I | awk '{print $1}')
#    printf '\n##### Server started successfully on '
#    printf "$ip_host"
#    printf '! ######\n'
#    unset ip_host
#  else printf '\n##### Error while starting #####\n'
#  exit 15
#fi
printf '\n##### Install OMEGA service #####\n'
sudo cp ~/Omega/omega.service /lib/systemd/system/ &&
sudo systemctl enable omega
if [[ $? == 0 ]]
  then printf '\n##### Service OMEGA installed successfully #####\n'
  else printf '\n##### Error while installing service #####\n'
  exit 16
fi
printf '\n##### Starting OMEGA #####\n'
sudo systemctl start omega >> ~/install_log.txt
if [[ $? == 0 ]]
  then export ip_host=$(hostname -I | awk '{print $1}')
    printf '\n##### Server started successfully on '
    printf "$ip_host"
    printf '! ######\n'
    unset ip_host
  else printf '\n##### Error while service OMEGA starting #####\n'
  exit 17
fi
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