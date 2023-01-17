#!/usr/bin/env bash
printf '##### Установка сервиса ОМЕГА #####\n'
printf '\n##### Удаление старой версии #####\n'
. ~/.bashrc
#pyenv uninstall 3.9.10
#export PGPASSWORD=omega1q2w &&
#psql -d omega_db -U omega_user -f Omega/dropAllTables.sql &&
#unset PGPASSWORD
sudo systemctl stop omega > ~/install_log.txt 2>&1
PGPASSWORD=omega1q2w dropdb -U omega_user --if-exists -w omega_db >> ~/install_log.txt 2>&1
sudo rm /lib/systemd/system/omega.service >> ~/install_log.txt 2>&1
#sudo rm -rf ~/.pyenv >> ~/install_log.txt 2>&1
sudo rm ~/Desktop/run.sh >> ~/install_log.txt 2>&1
sudo rm ~/Desktop/shortcut.desktop >> ~/install_log.txt 2>&1
sudo rm -rf ~/Omega >> ~/install_log.txt 2>&1
sudo rm -rf ~/admConsole >> ~/install_log.txt 2>&1
sed -i.bak '/omega start/,/stop omega/d' ~/.bashrc
printf '##### ------------OK----------- #####\n'
printf '\n##### Включаем сервис NTP #####\n'
sudo systemctl start ntp >> ~/install_log.txt 2>&1
sudo systemctl enable ntp >> ~/install_log.txt 2>&1
sudo systemctl status ntp >> ~/install_log.txt 2>&1
printf '##### ------------OK----------- #####\n'
printf '\n##### Обновляем пакеты ASTRALINUX #####'
printf '\n##### Это может занять много времени!! #####'
printf '\n##### Пожалуйста, подождите! #####\n'
date
sudo apt-get update >> ~/install_log.txt 2>&1 &&
sudo apt-get -y install openssh-server >> ~/install_log.txt 2>&1 &&
sudo apt-get -y install postgresql >> ~/install_log.txt 2>&1
if [[ $? == 0 ]]
  then printf '##### ------------OK----------- #####\n'
  else printf '\n##### Ошибка при обновлении пакетов #####\n'
#  exit 1
fi
DIRECTORY=$PWD
printf '\n Текущая директория: '
printf "$DIRECTORY"
printf '\n'
printf '\n##### Копируем ОМЕГА ######\n'
mv Omega/ ~/Omega
mv admConsole/ ~/admConsole
cd ~ && rm -R "$DIRECTORY"
printf '##### ------------OK----------- #####\n'
printf '\n##### Меняем настройки parsec ######\n'
sudo sed -i.bak 's/zero_if_notfound: no/zero_if_notfound: yes/' /etc/parsec/mswitch.conf
printf '##### ------------OK----------- #####\n'
printf '\n##### Создаём БД #####'
printf '\n##### Копируем скрипт БД #####\n'
sudo cp ~/Omega/init_db /etc/postgresql

sudo chown postgres /etc/postgresql/init_db
sudo -u postgres psql -f /etc/postgresql/init_db >> ~/install_log.txt 2>&1
if [[ $? == 0 ]]
  then printf '##### ------------OK----------- #####\n'
  else printf '\n##### Ошибка создания БД #####\n'
  exit 10
fi
printf '\n##### Удаляем временные файлы! #####\n'
rm ~/Omega/init_db
sudo rm /etc/postgresql/init_db
printf '##### ------------OK----------- #####\n'
printf '\n##### Правим postgres config #####\n'
sudo sed -i.bak 's/^local\s*all\s*all\s*peer$/local all all md5/' /etc/postgresql/9.6/main/pg_hba.conf
printf '##### ------------OK----------- #####\n'
printf '\n##### Перезапускаем БД #####\n'
sudo systemctl restart postgresql
printf '##### ------------OK----------- #####\n'
printf '\n##### Добавляем данные в БД! #####\n'
cd ~/Omega &&
export PGPASSWORD=omega1q2w &&
psql -d omega_db -U omega_user -f create_script >> ~/install_log.txt &&
unset PGPASSWORD
printf '##### ------------OK----------- #####\n'
printf '\n##### Настройка ОМЕГИ #####\n'
chmod +x first_run run Api
./first_run
printf '##### ------------OK----------- #####\n'
printf '\n##### Устанавливаем сервис ОМЕГИ #####\n'
sudo cp ~/Omega/omega.service /lib/systemd/system/ &&
sudo systemctl enable omega
if [[ $? == 0 ]]
  then printf '##### ------------OK----------- #####\n'
  else printf '\n##### Ошибка при создании сервиса ОМЕГА #####\n'
  exit 11
fi
printf '\n##### Запускаем ОМЕГУ #####\n'
ip_host=127.0.0.1
sudo systemctl start omega >> ~/install_log.txt
if [[ $? == 0 ]]
  then export ip_host=$(hostname -I | awk '{print $1}')
    printf '\n##### Сервер успешно запущен на '
    printf "$ip_host"
    printf '! ######\n'
    printf '\n##### Время '
    printf "$(date)"
    printf ' ######\n'
    unset ip_host
  else printf '\n##### Ошибка при запуске сервера #####\n'
  exit 12
fi

printf '\n##### Устанавливаем панель администратора #####\n'
cd ~/admConsole/
mv ~/admConsole/run.sh ~/admConsole/shortcut.desktop ~/Desktop/
chmod +x ~/Desktop/run.sh
printf '##### ------------OK----------- #####\n'
printf '\n##### Добавляем необходимые права #####\n'
echo 'omega ALL=(ALL) NOPASSWD: /bin/systemctl * omega' | sudo EDITOR='tee -a' visudo
printf '##### ------------OK----------- #####\n'
#printf '\n##### Installing packets for admin panel #####\n'
#sudo apt-get -y install xorgxrdp xrdp >> ~/install_log.txt
#sudo apt-get -y install curl git >> ~/install_log.txt
#curl https://pyenv.run | bash >> ~/install_log.txt 1>&2
echo '# omega start' >> ~/.bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
echo '# omega end' >> ~/.bashrc
##tail -n 10 ~/.bashrc
#export PYENV_ROOT="$HOME/.pyenv"
##echo $PYENV_ROOT
#command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
#eval "$(pyenv init -)"
#eval "$(pyenv virtualenv-init -)"
#printf '\n##### Restart bash #####\n'
##exec "$SHELL"
#. ~/.bashrc
#printf '\n##### Installing packets for python #####\n'
#sudo apt-get -y install make build-essential libssl-dev zlib1g-dev \
#libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
#libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev >> ~/install_log.txt
#printf '\n##### All packets have been installed #####\n'
#printf '\n##### Installing python #####\n'
#pyenv install 3.9.10
#printf '\n##### Python have been installed #####\n'
#pyenv global 3.9.10
#python --version
##cd ~
##unzip ~/admConsole-tray.zip >> ~/install_log.txt
#cd ~/admConsole/
#pip install -r requirements.txt >> ~/install_log.txt
#cd ~
#mv ~/admConsole/run.sh ~/admConsole/shortcut.desktop ~/Desktop/
#chmod +x ~/Desktop/run.sh
#date
#printf '\n##### Add rights to start/stop OMEGA #####\n'
#echo 'omega ALL=(ALL) NOPASSWD: /bin/systemctl * omega' | sudo EDITOR='tee -a' visudo
#printf '\n##### Rights added #####\n'
#printf '\n##### Admin panel installed successfully #####\n'
exit 0