printf '\n##### Установка панели администратора #####\n'
    sleep 1
    DIRECTORY=$PWD
    printf '\n Текущая директория: '
    printf "$DIRECTORY"
    printf '\n'
    printf '\n##### Копируем ОМЕГА ######\n'
    mv admConsole/ ~/admConsole
    cd ~ && rm -R "$DIRECTORY"
    cd ~/admConsole/
    mv ~/admConsole/shortcut2.desktop ~/Desktop/
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
    echo '# omega end' >> ~/.bashrc
    export PYENV_ROOT="$HOME/.pyenv"
    command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
    printf '\n##### Перезапускаем оболочку #####\n'
    . ~/.bashrc
    printf '\n##### Устанавливаем дополнительные пакеты  #####\n'
    sudo apt-get -y install make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libedit-dev\
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev >> ~/install_log.txt
    printf '\n##### Все пакеты установлены #####\n'
    pyenv install 3.9.10
    pyenv global 3.9.10
    python --version
    cd ~
    cd ~/admConsole/
    pip install -r requirements.txt >> ~/install_log.txt
    cd ~