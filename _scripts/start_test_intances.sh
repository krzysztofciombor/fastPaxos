nohup ./start_coordinator.sh 6010 2 > /dev/null &

for i in `seq 6011 6012`;
do
  nohup ./start_instance.sh $i 2 > /dev/null &
done

nohup ./start_coordinator.sh 6020 6 > /dev/null &

for i in `seq 6021 6026`;
do
  nohup ./start_instance.sh $i 6 > /dev/null &
done

nohup ./start_coordinator.sh 6030 6 > /dev/null &

for i in `seq 6031 6036`;
do
  nohup ./start_instance.sh $i 6 > /dev/null &
done

nohup ./start_coordinator.sh 6040 6 > /dev/null &

for i in `seq 6041 6046`;
do
  nohup ./start_instance.sh $i 6 > /dev/null &
done

exit 1
