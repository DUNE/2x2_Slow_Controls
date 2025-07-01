# RTDs

The process for running the RTD script is simple.

- First let's ssh to acd-daq05 as acdcs user:

```bash
ssh -J acdcs@acd-gw06.fnal.gov acdcs@acd-daq05.fnal.gov
```

- Then, SSH to the raspi you want to work on:

```
ssh pi@acd-rtd{#number}.fnal.gov
```

-  Go to the scripts location area:

```
   cd /home/pi/SlowControls2x2/RTDs/RTD
```

- Now just run:
```
./start_rtd_in_screen.sh
```

**Important:** If you are pulling this code for the first time to the raspberry pi, you MUST modify the config.ini file setting the variable "POS = mod{#module number}." For example, if we are working with the RTD for module 3, then we use "POS = mod3." In case of module 0 (which has two RTDs), we use 0tpc1 and 0tpc2 as module number. 
