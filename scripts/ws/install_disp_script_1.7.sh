#!/usr/bin/env bash
CR=0
CONF_D="Y"
printf '##### Начинаем установку диспетчера ОМЕГА #####\n\n'
printf '##### Настраиваем NTP #####\n'
sudo systemctl start ntp > ~/install_disp_log.txt 2>&1
sudo systemctl enable ntp >> ~/install_disp_log.txt 2>&1
sudo systemctl status ntp >> ~/install_disp_log.txt 2>&1
date
echo -e "\033[31mВы хотите обновить репозитории? Y/n|Д/н]:\033[0m"
while true
  do
  read -n 1 CONF_D
  case $CONF_D in
    y|Y|yes|Yes|"Д"|"д"|"Да"|"да")
      printf "\nРепозитории будут обновлены\n"
      CR=1
      break;;
    n|N|no|No|"Н"|"н"|"Нет"|"нет")
      printf "\nРепозитории не будут обновлены\n"
      break;;
    *)
      printf "\nСимвол $CONF_D не распознан - повторите!\n";;
  esac
done
if [[ $CR -eq 1 ]]
  then
  sudo sed -i.bak 's/#deb https/deb https/' /etc/apt/sources.list
  sudo sed -i.bak 's/^deb cdrom/#deb cdrom/' /etc/apt/sources.list
  printf '#------------------------------------------------#\n'
  printf '#Репозитории обновлены---------------------------#\n'
fi
printf '\n##### Устанавливаем необходимые пакеты! ######\n'
sudo apt-get update >> ~/install_disp_log.txt 2>&1
sudo apt-get -y install openssh-server >> ~/install_disp_log.txt 2>&1
sudo apt-get -y install xorgxrdp xrdp >> ~/install_disp_log.txt 2>&1
sudo apt-get -y install mtp-tools aft-mtp-mount >> ~/install_disp_log.txt 2>&1
if [[ $? == 0 ]]
  then printf '\n##### Пакеты установлены! ######\n'
  else printf '\n##### Проблемы с установкой пакетов #####\n'
  exit 111
fi
sudo systemctl start ssh >> ~/install_disp_log.txt 2>&1
sudo systemctl enable ssh >> ~/install_disp_log.txt 2>&1
sudo systemctl status ssh >> ~/install_disp_log.txt 2>&1
printf '##### ---------------OK--------------- #####\n'
printf '\n##### Удаляем старые файлы #####\n'
cp ~/dispatcher/opt/omega-dispatcher/.OmegaRoot/config.properties ~/ >> ~/install_disp_log.txt 2>&1
rm -rf ~/dispatcher >> ~/install_disp_log.txt 2>&1
rm -rf ~/.OmegaRoot/* >> ~/install_disp_log.txt 2>&1

rm ~/Desktop/disp_shortcut.desktop >> ~/install_disp_log.txt 2>&1
printf '##### ---------------OK--------------- #####\n'
DIRECTORY=$PWD
printf '\n Текущая директория: '
printf "$DIRECTORY"
printf '\n'
printf '\n##### Копируем диспетчер ОМЕГА К400 ######\n'
sleep 3
mv dispatcher/ ~/dispatcher/
cd ~/dispatcher/
sed -i.bak "s/omega/$USER/" disp_shortcut.desktop
mv disp_shortcut.desktop ~/Desktop/
#printf '\n##### Обновляем ярлыки ######\n'
##fly-wmfunc FLYWM_FORCE_UPDATE_SHORTCUT
#~/update.sh
#sleep 3
#printf '\n##### Ярлыки обновлены ######\n'
sudo chown ${USER}:${USER} ~/dispatcher/run.sh
sudo chmod +x ~/dispatcher/run.sh
ar x `find . -name "omega_dispatcher_*" `
#ar x dispatcher-compose_1.0.0-1_amd64.deb
zstd -d data.tar.xz
tar -xf data.tar
mv logo.png ~/dispatcher/opt/omega-dispatcher
mv run.sh ~/dispatcher/opt/omega-dispatcher
if [[ $? == 0 ]]
  then printf '##### ---------------OK--------------- #####\n'
  else printf '##### Проблемы с копированием файлов #####\n'
  exit 112
fi
mkdir ~/dispatcher/opt/omega-dispatcher/.OmegaRoot
cp ~/config.properties ~/dispatcher/opt/omega-dispatcher/.OmegaRoot >> ~/install_disp_log.txt 2>&1
cd ~ && rm -R "$DIRECTORY"
printf '##### Диспетчер успешно установлен и готов к работе! #####\n'
exit 0