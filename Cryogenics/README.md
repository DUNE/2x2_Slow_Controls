# Run the Cryogenics Monitoring
This branch contains the podman image that reads the cryo data from their PostgreSQL database.

First let's ssh to acd-daq05 as acdcs user:

```bash
ssh -J acdcs@acd-gw06.fnal.gov acdcs@acd-daq05.fnal.gov
```
Go to /home/acd/acdcs/2x2/Cryogenics.

To run the continous monitoring, you just need to execute the .sh script, it will create the container:

```bash
./run.sh
```

Now if we list all possible containers, you can see that the cryogenics_monitor container is up and running.

![image](https://github.com/DUNE/2x2_Slow_Controls/assets/34606228/64aac6e7-4306-4193-b8ac-c8ea800cdf9f)
