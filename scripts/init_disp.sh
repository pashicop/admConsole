#!/usr/bin/env bash
printf '##### Начинаем установку диспетчера ОМЕГА #####\n\n'
printf '##### Настраиваем NTP #####\n'
sudo systemctl start ntp > ~/install_disp_log.txt 2>&1
sudo systemctl enable ntp >> ~/install_disp_log.txt 2>&1
sudo systemctl status ntp >> ~/install_disp_log.txt 2>&1
date
#sudo apt-get update >> ~/install_disp_log.txt &&
#sudo apt-get -y install openssh-server >> ~/install_disp_log.txt &&
#sudo apt-get -y install xorgxrdp xrdp >> ~/install_disp_log.txt
#if [[ $? == 0 ]]
#  then printf '\n##### Update packets done! ######\n'
#  else printf '\n##### Error with updating packets #####\n'
#  exit 111
#fi
printf '##### ---------------OK---------------#####\n'
printf '\n##### Удаляем старые файлы #####\n'
rm -rf ~/jdk11 >> ~/install_disp_log.txt 2>&1
rm -rf ~/dispatcher >> ~/install_disp_log.txt 2>&1
rm ~/Desktop/shortcut.desktop >> ~/install_disp_log.txt 2>&1
rm ~/Desktop/run.sh >> ~/install_disp_log.txt 2>&1
printf '##### ---------------OK---------------#####\n'
mv jdk11/ ~/jdk11 &&
sudo chown -R omega:omega ~/jdk11/ &&
sudo chmod -R 777 ~/jdk11/
DIRECTORY=$PWD
printf '\n Текущая директория: '
printf "$DIRECTORY"
printf '\n'
printf '\n##### Копируем ОМЕГА ######\n'
mv dispatcher ~/dispatcher
cd ~/dispatcher
#cd ~ && rm -R "$DIRECTORY"
sudo cp run.sh ~/Desktop/ &&
sudo chown omega:omega ~/Desktop/run.sh &&
sudo chmod 777 ~/Desktop/run.sh &&
mv shortcut.desktop ~/Desktop/
#printf '##### ------------OK----------- #####\n'
#if [[ $? == 0 ]]
#  then printf '\n##### zulu has copied to Desktop! ######\n'
#  else printf '\n##### Error with copying zulu #####\n'
#  exit 112
#fi
#printf '\n##### COPY dispatcher #####'
#sudo cp run.sh ~/Desktop/ &&
#sudo chown omega:omega ~/Desktop/run.sh &&
#sudo chmod 777 ~/Desktop/run.sh &&
#mv ./shortcut.desktop ~/Desktop/
if [[ $? == 0 ]]
  then printf '##### ---------------OK---------------#####\n'
  else printf '##### Проблемы с копированием файлов #####\n'
  exit 112
fi
cd ~ && rm -R "$DIRECTORY"
exit 0