#Runs goostats in loop
for datafile in [!stats]*[AB].txt
do
echo $datafile
bash goostats $datafile stats-$datafile
done

