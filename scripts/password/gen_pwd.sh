#!/usr/bin/env bash
OMEGA_PWD_TMP=$(python2.7 -c "import sys, binascii, random, string; main_pwd = ''.join(random.choice(string.ascii_letters) for i in range(10)); sys.stdout.write(main_pwd)")
#echo $OMEGA_PWD_TMP
echo "export OMEGA_PWD=$OMEGA_PWD_TMP" >> ~/.bashrc
echo "export OMEGA_PWD_B=$(python2.7 -c "import sys, binascii, random, string; sys.stdout.write(binascii.hexlify(str('$OMEGA_PWD_TMP').encode('ascii')))")" >> ~/.bashrc
. ~/.bashrc