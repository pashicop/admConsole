#!/usr/bin/env bash
printf '##### Начинаем установку диспетчера ОМЕГА #####\n\n'
printf '##### Настраиваем NTP #####\n'
sudo systemctl start ntp > ~/install_disp_log.txt 2>&1
sudo systemctl enable ntp >> ~/install_disp_log.txt 2>&1
sudo systemctl status ntp >> ~/install_disp_log.txt 2>&1
date
sudo sed -i.bak 's/#deb https/deb https/' /etc/apt/sources.list
sudo sed -i.bak 's/deb cdrom/#deb cdrom/' /etc/apt/sources.list
printf '\n##### Устанавливаем необходимые пакеты! ######\n'
sudo apt-get update >> ~/install_disp_log.txt 2>&1
sudo apt-get -y install openssh-server >> ~/install_disp_log.txt 2>&1
sudo apt-get -y install xorgxrdp xrdp >> ~/install_disp_log.txt 2>&1
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
rm -rf ~/dispatcher >> ~/install_disp_log.txt 2>&1
cp ~/.OmegaRoot/config.properties ~/ >> ~/install_disp_log.txt 2>&1
rm -rf ~/.OmegaRoot/* >> ~/install_disp_log.txt 2>&1
cp ~/config.properties ~/.OmegaRoot >> ~/install_disp_log.txt 2>&1
rm ~/Desktop/shortcut.desktop >> ~/install_disp_log.txt 2>&1
printf '##### ---------------OK--------------- #####\n'
DIRECTORY=$PWD
printf '\n Текущая директория: '
printf "$DIRECTORY"
printf '\n'
printf '\n##### Копируем диспетчер ОМЕГА К400 ######\n'

mv dispatcher/ ~/dispatcher/
cd ~/dispatcher/
sed -i.bak "s/omega/$USER/" shortcut.desktop
mv shortcut.desktop ~/Desktop/
sudo chown ${USER}:${USER} ~/dispatcher/run.sh &&
sudo chmod +x ~/dispatcher/run.sh &&
ar x dispatcher-compose_1.0.0-1_amd64.deb
zstd -d data.tar.zst
tar -xf data.tar
mv logo.png ~/dispatcher/opt/dispatcher-compose
mv run.sh ~/dispatcher/opt/dispatcher-compose
if [[ $? == 0 ]]
  then printf '##### ---------------OK--------------- #####\n'
  else printf '##### Проблемы с копированием файлов #####\n'
  exit 112
fi
cd ~ && rm -R "$DIRECTORY"
printf '##### Диспетчер успешно установлен и готов к работе! #####\n'
exit 0