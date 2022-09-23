#!/usr/bin/env bash
printf 'Add repo dev\n'
sudo touch /etc/apt/sources.list.d/dev.list
sudo chmod 777 /etc/apt/sources.list.d/dev.list
echo 'deb ftp://'"${1:-10.1.4.147}"'/AstraSE 1.7_x86-64 main contrib non-free' > /etc/apt/sources.list.d/dev.list
sudo chmod 644 /etc/apt/sources.list.d/dev.list
sudo apt-get update
printf 'update OK/n'
