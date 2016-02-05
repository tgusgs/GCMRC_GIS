#Runs goostats in loop. Edited 02/05/2016,  @ 9:21am.
for datafile in [!stats]*[AB].txt
do
echo ${datafile}
bash goostats ${datafile} stats-${datafile}
done

