#!/usr/bin/env bash
set -euo pipefail
printf '##### Start updating OMEGA #####\n' | tee update_log.txt
printf '\n##### Please wait! #####\n' | tee -a update_log.txt
sleep 1
date | tee -a update_log.txt
NTP=0
DB=0
STATUS=0

echo -e "\033[31mВы хотите обновить БД? Все данные будут потеряны![Y/n|Д/н]:\033[0m"
read -n 3 CONF_D
#      read -r -n 3 -p "\033[31mВы уверены, что хотите обновить БД? Все данные будут потеряны![Y/n|Д/н]:\033[0m"$'\n' CONF
CONF_D="${CONF_D:-Y}"
echo "$CONF_D"
case $CONF_D in
  y|Y|yes|Yes|"Д"|"д"|"Да"|"да")
    echo "БД будет обновлена"
    DB=1;;
  n|N|no|No|"Н"|"н"|"Нет"|"нет")
    echo "БД не будет обновлена";;
esac
echo -e "\033[31mВы хотите обновить время?[Y/n|Д/н]:\033[0m"
read -n 3 CONF_T
#      read -r -n 3 -p "\033[31mВы уверены, что хотите обновить БД? Все данные будут потеряны![Y/n|Д/н]:\033[0m"$'\n' CONF
CONF_T="${CONF_T:-Y}"
echo "$CONF_T"
case $CONF_T in
  y|Y|yes|Yes|"Д"|"д"|"Да"|"да")
    echo "Время будет обновлено"
    NTP=1;;
  n|N|no|No|"Н"|"н"|"Нет"|"нет")
    echo "Время не будет обновлено";;
esac
echo "NTP = $NTP" | tee -a update_log.txt
echo "DB = $DB" | tee -a update_log.txt
if [[ $NTP -eq 1 ]]
  then sudo systemctl restart ntp | tee -a update_log.txt
  else printf ''
fi
sleep 1
date | tee -a update_log.txt
if [[ $DB -eq 1 ]]
  then
    printf '\n##### deleting and creating DB #####\n'
    sleep 1
    export PGPASSWORD=omega1q2w &&
    psql -U omega_user -d omega_db -f dropAllTables.sql >> update_log.txt 2>&1 &&
    psql -d omega_db -U omega_user -f create_script >> update_log.txt 2>&1 &&
    unset PGPASSWORD
    STATUS=$?
  else
    echo
fi
if [[ $STATUS == 0 ]]
  then printf '\n##### DB dropped and created ######\n'
  else printf '\n##### Smth wrong with recreating DB  #####\n'
  exit 113
fi
sleep 1
printf '\n##### Stopping service #####\n'
# shellcheck disable=SC2046
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
sudo systemctl start omega | tee -a update_log.txt
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