#!/usr/bin/env bash
CR=0
TP=0
PA=0
CONF_D="Y"
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
  sudo sed -i.bak 's/deb cdrom/#deb cdrom/' /etc/apt/sources.list
fi

printf '\n##### Включаем сервис NTP #####\n'
sudo systemctl start ntp >> ~/install_log.txt 2>&1
sudo systemctl enable ntp >> ~/install_log.txt 2>&1
sudo systemctl status ntp >> ~/install_log.txt 2>&1
printf '##### ------------OK----------- #####\n'
printf '\n##### Обновляем пакеты ASTRALINUX #####'
printf '\n##### Это может занять много времени!! #####'
printf '\n##### Пожалуйста, подождите! #####\n'
date
sleep 10
date
sudo apt-get update >> ~/install_log.txt 2>&1 &&
sudo apt-get -y install openssh-server xorgxrdp xrdp >> ~/install_log.txt 2>&1 &&
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
PG_HOME=`sudo -u postgres psql -c "SHOW hba_file;" | grep pg_hba` &&
echo $PG_HOME &&
sudo sed -i.bak 's/^local\s*all\s*all\s*peer$/local all all md5/' $PG_HOME
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
chmod +x first_run run Api Licensing/ValidateCli Licensing
echo -e "\033[31mВы хотите заполнить сервер тестовыми данными? Y/n|Д/н]:\033[0m"
while true
  do
  read -n 1 CONF_D
  case $CONF_D in
    y|Y|yes|Yes|"Д"|"д"|"Да"|"да")
      printf "\nДанные будут добавлены\n"
      TP=1
      break;;
    n|N|no|No|"Н"|"н"|"Нет"|"нет")
      printf "\nТестовые данные не будут добавлены\n"
      break;;
    *)
      printf "\nСимвол $CONF_D не распознан - повторите!\n";;
  esac
done
if [[ $TP -eq 1 ]]
  then
    ./first_run true
  else
    ./first_run
fi
#. ~/.bashrc
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
ADM=$(cat "$HOME"/Omega/admPass.txt)
#echo $ADM
sudo systemctl start omega >> ~/install_log.txt
if [[ $? == 0 ]]
  then export ip_host=$(hostname -I | awk '{print $1}')
    printf '\n##### Сервер успешно запущен на '
    printf "$ip_host"
    printf '! ######\n'
    printf '\n##### Время '
    printf "$(date)"
    printf ' ######\n'
#    printf '\n##### Пароль для admin - '
##    printf "$adminPass"
#    printf "$(<./admPass.txt)"
#    printf ' ######\n'
    unset ip_host
  else printf '\n##### Ошибка при запуске сервера #####\n'
  exit 12
fi

FILE="$HOME/Omega/admPass.txt"
#echo "$FILE"
#if [[ -f "$FILE" ]]
#  then
##    OMEGA_PWD_B=$(python2.7 -c "import sys, binascii, random, string; sys.stdout.write(binascii.hexlify(str('$(<./admPass.txt)').encode('ascii')))")
#    OMEGA_PWD_B=$(python2.7 -c "import sys, binascii, hashlib;  sys.stdout.write(binascii.hexlify(hashlib.pbkdf2_hmac('sha256', bytes('$(<./admPass.txt)'), b'omega', 10000)))")
##    echo $OMEGA_PWD_B
#    sed -i.bak "s/04533cc2be3af54c7f5c827f07417a14ea8f1ba5ec2b6a2756b101c5446cd0ae/${OMEGA_PWD_B}/" ~/admConsole/main.py
#    rm ~/Omega/admPass.txt
#fi

echo -e "\033[31mВы хотите установить панель администратора? Y/n|Д/н]:\033[0m"
while true
  do
  read -n 1 CONF_D
  case $CONF_D in
    y|Y|yes|Yes|"Д"|"д"|"Да"|"да")
      printf "\nПанель будет установлена\n"
      PA=1
      break;;
    n|N|no|No|"Н"|"н"|"Нет"|"нет")
      printf "\nПанель НЕ будет установлена\n"
      break;;
    *)
      printf "\nСимвол $CONF_D не распознан - повторите!\n";;
  esac
done
if [[ $PA -eq 1 ]]
  then
    printf '\n##### Установка панели администратора #####\n'
    sleep 1
    cd ~/admConsole/
    mv ~/admConsole/shortcut.desktop ~/Desktop/
    chmod +x ~/admConsole/run.sh
    printf '##### ------------OK----------- #####\n'
    printf '\n##### Добавляем необходимые права #####\n'
    echo 'omega ALL=(ALL) NOPASSWD: /bin/systemctl * omega' | sudo EDITOR='tee -a' visudo
    echo 'omega ALL=(ALL) NOPASSWD: /usr/bin/crontab *' | sudo EDITOR='tee -a' visudo
    printf '##### ------------OK----------- #####\n'
    printf '\n##### Устанавливаем необходимые пакеты #####\n'
    sudo apt-get -y install xorgxrdp xrdp >> ~/install_log.txt
    sudo apt-get -y install curl git >> ~/install_log.txt
    curl https://pyenv.run | bash >> ~/install_log.txt 1>&2
    echo '# omega start' >> ~/.bashrc
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
#    echo 'export OMEGA=0' >> ~/.bashrc
    echo '# omega end' >> ~/.bashrc
    #tail -n 10 ~/.bashrc
    export PYENV_ROOT="$HOME/.pyenv"
    #echo $PYENV_ROOT
    command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
    printf '\n##### Перезапускаем оболочку #####\n'
    #exec "$SHELL"
    . ~/.bashrc
    printf '\n##### Устанавливаем дополнительные пакеты  #####\n'
    sudo apt-get -y install make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libedit-dev\
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev >> ~/install_log.txt
    printf '\n##### Все пакеты установлены #####\n'
#    printf '\n##### Installing python #####\n'
    pyenv install 3.9.10
#    printf '\n##### Python have been installed #####\n'
    pyenv global 3.9.10
    python --version
    #cd ~
    #unzip ~/admConsole-tray.zip >> ~/install_log.txt
    cd ~/admConsole/
    pip install -r requirements.txt >> ~/install_log.txt
    cd ~
fi
printf '\n##### Установка завершена #####\n'
    printf '\n##### Логин по умолчанию - admin, Пароль - '
    printf "$ADM"
    printf ' #####\n'
    printf '\n##### Сохраните пароль в надёжном месте! #####\n'
exit 0