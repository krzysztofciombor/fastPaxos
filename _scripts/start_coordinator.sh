#!/bin/bash
cd ..
nohup python3 fast_paxos.py $1 $2 > "${1}-coordinator.log" &
exit 0
