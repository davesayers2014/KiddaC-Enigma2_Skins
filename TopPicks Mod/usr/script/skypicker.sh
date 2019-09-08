#!/bin/sh
#

# Slyk Universal toppicks V5 (C) kiddac. 2019

echo 1 > /proc/sys/vm/drop_caches
echo 2 > /proc/sys/vm/drop_caches
echo 3 > /proc/sys/vm/drop_caches

python /etc/enigma2/slyk/picker.py

exit 0