#!/usr/bin/env bash
printf '##### Start installing OMEGA dispatcher #####\n\n'
sudo systemctl start ntp > ~/install_disp_log.txt
sudo systemctl enable ntp >> ~/install_disp_log.txt
sudo systemctl status ntp >> ~/install_disp_log.txt
date
sudo apt-get update >> ~/install_disp_log.txt &&
sudo apt-get -y install openssh-server >> ~/install_disp_log.txt &&
sudo apt-get -y install xorgxrdp xrdp >> ~/install_disp_log.txt
if [[ $? == 0 ]]
  then printf '\n##### Update packets done! ######\n'
  else printf '\n##### Error with updating packets #####\n'
  exit 111
fi
printf '\n##### COPY zulu compiler #####'
sudo cp -R ./jdk11 ~/ &&
sudo chown -R omega:omega ~/jdk11/ &&
sudo chmod -R 777 ~/jdk11/
if [[ $? == 0 ]]
  then printf '\n##### zulu has copied to Desktop! ######\n'
  else printf '\n##### Error with copying zulu #####\n'
  exit 112
fi
printf '\n##### COPY dispatcher #####'
sudo cp './run.sh' ~/Desktop/ &&
sudo chown omega:omega ~/Desktop/run.sh &&
sudo chmod 777 ~/Desktop/run.sh
mv ./shortcut.desktop ~/Desktop/
if [[ $? == 0 ]]
  then printf '\n##### Dispatcher has copied to Desktop! ######\n'
  else printf '\n##### Error with copying dispatcher #####\n'
  exit 112
fi
exit 0