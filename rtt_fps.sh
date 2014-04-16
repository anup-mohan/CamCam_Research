#!/bin/bash

ip_addr=128.10.29.20

count=10

fps=`python get_fps_rtt.py`

fps=`echo $fps | cut -d" " -f1`

del=145
delay_val=$del"ms"

#rtt_avg=`ping -c $count $ip_addr | grep "rtt" | cut -d/ -f5`

#echo $delay_val $rtt_avg $fps >> rtt_fps.txt

#echo $delay_val $rtt_avg $fps

while [ $del -lt 255 ]; do

	del=$((del + 5))

	delay_val=$del"ms"

	sudo tc qdisc add dev eth0 root netem delay $delay_val

	rtt_avg=`ping -c $count $ip_addr | grep "rtt" | cut -d/ -f5`

	fps=`python get_fps_rtt.py`

	fps=`echo $fps | cut -d" " -f1`

	echo $delay_val $rtt_avg $fps >> rtt_fps.txt

	sudo tc qdisc del dev eth0 root
	
done



