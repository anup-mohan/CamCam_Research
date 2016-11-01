#!/bin/bash

fname1="LRM_rtt_test_"
fname2=$1
fname3=".txt"
filename=$fname1$fname2$fname3

inputfile=$2

count=10

for ip_addr in `cat $inputfile`
do
	
	rtt_avg=`ping -c $count $ip_addr | grep "rtt" | cut -d/ -f5`

	echo $ip_addr $rtt_avg >> $filename
done
