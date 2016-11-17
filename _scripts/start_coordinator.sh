#!/bin/bash
cd ..
nohup python3 fast_paxos.py > "$coordinator.log" &
exit 0
