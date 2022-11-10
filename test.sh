#!/usr/bin/env bash
set -euo pipefail
function help(){
    echo "USAGE: test.sh -t, -f <arg>, -h"
}

#while getopts ":tf:h" ARG; do
#  case "$ARG" in
#    t) echo "Running -t flag" ;;
#    f) echo "Running -f flag"
#       echo "Argument passed is $OPTARG" ;;
#    h) help ;;
#    :) echo "argument missing" ;;
#    \?) echo "Something is wrong" ;;
#  esac
#done

while getopts ":a:" opt; do
  case $opt in
    a)
      echo "-a was triggered, Parameter: $OPTARG" >&2
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done
shift "$((OPTIND-1))"

