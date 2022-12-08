#!/usr/bin/env bash
printf '##### Start installing OMEGA #####\n'
printf '\n##### UPDATE packets #####'
printf '\n##### It may take a long time!! #####'
printf '\n##### Please wait! #####\n\n'
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
mv Omega/ ~/Omega
mv admConsole/ ~/admConsole
cd ~ && rm -R O
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
chmod +x first_run run Api
./first_run
printf '\n##### First run OK! #####\n'
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
    printf '\n##### Time '
    printf "$(date)"
    printf ' ######\n'
    unset ip_host
  else printf '\n##### Error while service OMEGA starting #####\n'
  exit 17
fi
sudo apt-get -y install xorgxrdp xrdp
sudo apt-get -y install curl git
sudo apt-get -y install make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
cd ~/admConsole
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
export PATH=/opt/python/3.9.10/bin/:$PATH
. ~/.bashrc
python3 --version
cd ~/admConsole/
pip3 install -r requirements.txt
cp run.sh ~/Desktop/
chmod +x ~/Desktop/run.sh
date
printf '\n##### Add rights to start/stop OMEGA #####\n'
echo 'omega ALL=(ALL) NOPASSWD: /bin/systemctl * omega' | sudo EDITOR='tee -a' visudo
printf '\n##### Rights added #####\n'
printf '\n##### Admin panel installed successfully #####\n'
exit 0

