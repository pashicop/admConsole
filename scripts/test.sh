#!/usr/bin/env bash
set -euo pipefail
NTP=0
DB=0
function help(){
    echo
    echo "USAGE: update.sh -t, -d, -h"
    echo "This script updates OMEGA server "
    echo "-t - enable NTP if server has internet connection!"
    echo "-d - recreate database"
    echo "-h - help"
}

while getopts ":tdh" OPT; do
#  echo "BEFORE CASE: OPT=$OPT "
#  echo "OPTIND=$OPTIND"
  case $OPT in
    t)
      echo "-t выбрано"
      NTP=1
      ;;
    d)
      echo "-d выбрано"
      read -r -n 3 -p "Вы уверены, что хотите обновить БД? Все данные будут потеряны![Y/n|Д/н]:"$'\n' CONF
      CONF="${CONF:-Y}"
      echo "$CONF"
      case $CONF in
        y|Y|yes|Yes|"Д"|"д"|"Да"|"да")
          echo "БД будет обновлена"
          DB=1;;
        n|N|no|No|"Н"|"н"|"Нет"|"нет")
          echo "БД не будет обновлена. Перезапустите скрипт заново."
          exit 13;;
        *)
          echo "Ответ не распознан"
          exit 14;;
      esac
      ;;
    h)
      help
      ;;
    \?)
      echo "Неизвестный ключ: -$OPTARG"
      help
      exit 1
      ;;
    :)
      echo "Ключ -$OPTARG требует аргумент."
      help
      exit 1
      ;;
    *)
      echo "Некорректный аргумент"
      help
      ;;
  esac
done
shift "$((OPTIND-1))"
echo "NTP = $NTP"
echo "DB = $DB"
