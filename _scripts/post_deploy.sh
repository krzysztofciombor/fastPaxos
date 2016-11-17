#!/bin/bash
./stop_all.sh

pip3 install -r ../requirements.txt

nohup ./start_coordinator.sh > /dev/null &

for i in `seq 5001 5006`;
do
  nohup ./start_instance.sh $i 6 > /dev/null &
done
exit 0
