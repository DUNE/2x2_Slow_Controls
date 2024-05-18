# Run the MINERvA DQM Log Reader
This branch contains a script that extracts the most recent information pushed to the runcontrol.log and readout_dispatcher.log files. The source code of the podman image that creates the MINERvA DQM log reader script can be found here. The code lives locally on /home/nfs/minerva/Mx2_monitoring on acd-mnv01 as minerva user. This code provides a .txt file located at /home/nfs/minerva/Mx2_monitoring/last_log_entry.txt that server as input for the plot transfer code explained above. The content of this .txt is later pushed to InfluxDB by the plot transfer script.

First let's ssh to acd-mnv01 as minerva user:

```bash
ssh -J minerva@acd-gw06.fnal.gov minerva@acd-mnv01.fnal.gov
```
Go to /home/nfs/minerva/Mx2_monitoring.

To run the LogReader, you just need to execute the .sh script, it will create the container:

```bash
./run.sh
```

Now if we list all possible containers, you can see that the minerva_daq_logs container is up and running.

<img width="1170" alt="image" src="https://github.com/DUNE/2x2_Slow_Controls/assets/34606228/b94bb590-96f6-4237-827c-d8632e1dfa8f">
