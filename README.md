# Run the MINERvA DQM Plot Transfer
This branch contains the podman image that creates the MINERvA DQM plot transporter script. This script takes each of the DQM plots located on the shared NSF MINERvA area and adds a timestamp on top of it showing the last time the file content was modified. 

First let's ssh to acd-daq05 as acdcs user:

```bash
ssh -J acdcs@acd-gw06.fnal.gov acdcs@acd-daq05.fnal.gov
```
Go to /home/acd/acdcs/2x2/MINERvA_DQM_PlotTransfer.

To run the PlotTransporter, you just need to execute the .sh script, it will create the container:

```bash
./run.sh
```

Now if we list all possible containers, you can see that the minerva_dqm_plots container is up and running.

![image](https://github.com/DUNE/2x2_Slow_Controls/assets/34606228/64aac6e7-4306-4193-b8ac-c8ea800cdf9f)
