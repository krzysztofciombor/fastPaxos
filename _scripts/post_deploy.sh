#!/bin/bash
./stop_all.sh

pip3 install -r ../requirements.txt

nohup ./start_coordinator.sh > /dev/null &

for i in `seq 5001 5005`;
do
  nohup ./start_instance.sh $i 5 > /dev/null &
done
exit 0
