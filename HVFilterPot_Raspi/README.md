PFD4

ssh into any server of your pleasing, this tutorial will use daq05 as an example,

```bash
ssh -J <user>@acd-gw05.fnal.gov <user>@acd-daq05.fnal.gov
```

From here, you must ssh into the filter pot raspi,

```bash
ssh pi@<IP>
```
The ip address can be found here, https://cdcvs.fnal.gov/redmine/projects/argoncube-2x2-demonstrator/wiki/Ac2x2-network-configurations_ , under the HV section.

You will be prompted to enter a password.

After you are in the raspi enter:

```bash
cd Dune2x2_SlowControl/PFD4/
```

After you are in this directory using

```bash
./start_PFD4_in_screen.sh
```
to start the monitor in screen, and using

```bash
./start_PFD4.sh
```
will allow you to monitor the values in the terminal.
