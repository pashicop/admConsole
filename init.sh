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
exit 0