#! /bin/bash
echo "Загрузка..."
cd ~/admConsole-tray && nohup ~/.pyenv/versions/3.9.10/bin/python ./main.py > run.log 2>&1 &
echo "Загрузилось!"
sleep 0.5
exit 0
