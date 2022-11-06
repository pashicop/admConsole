#!/usr/bin/env bash
printf '##### Start updating OMEGA #####\n'
printf '\n##### Please wait! #####\n'
sleep 1
sudo systemctl restart ntp > ~/update_log.txt
date >> ~/update_log.txt
printf '\n##### Stopping service #####\n'
sudo systemctl stop omega || kill -9 $(pidof Api)
if [[ $? == 0 ]]
  then printf '\n##### Service stopped ######\n'
  else printf '\n##### Service cant stop!! #####\n'
  exit 111
fi
printf '\n##### Delete src #####\n'
sleep 1
rm -rf ~/Omega
if [[ $? == 0 ]]
  then printf '\n##### Source deleted ######\n'
  else printf '\n##### Cant delete source #####\n'
  exit 112
fi
printf '\n##### deleting and creating DB #####\n'
sleep 1
export PGPASSWORD=omega1q2w &&
psql -U omega_user -d omega_db -f dropAllTables.sql >> ~/update_log.txt 2>&1 &&
psql -d omega_db -U omega_user -f create_script &>> ~/update_log.txt 2>&1 &&
unset PGPASSWORD
if [[ $? == 0 ]]
  then printf '\n##### DB dropped and created ######\n'
  else printf '\n##### Smth wrong with recreating DB  #####\n'
  exit 113
fi
sleep 1
printf '\n##### Copy new src #####\n'
cp -r . ~/Omega
if [[ $? == 0 ]]
  then printf '\n##### New src installed #####\n'
  else printf '\n##### Smth wrong with new src installing #####\n'
  exit 114
fi
sleep 1
printf '\n##### First run #####\n'
cd ~/Omega && chmod +x first_run run Api &&
./first_run
printf '\n##### First run OK! #####\n'
sleep 1
printf '\n##### Starting OMEGA #####\n'
sudo systemctl start omega >> ~/update_log.txt
if [[ $? == 0 ]]
  then export ip_host=$(hostname -I | awk '{print $1}')
    printf '\n##### Server started successfully on '
    printf "$ip_host"
    printf '! ######\n'
    printf '\n##### Time '
    printf "$(date)"
    printf ' ######\n\n'
    unset ip_host
  else printf '\n##### Error while service OMEGA starting #####\n'
  exit 17
fi
sleep 1
exit 0