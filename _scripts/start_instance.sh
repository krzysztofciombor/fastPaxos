#!/bin/bash
cd ..
nohup python3 Instance.py $1 $2 > "${1}-instance.log" &
exit 0
