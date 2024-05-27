# About this GUI
This repository contains the code used for setting up the 2x2 slow controls monitoring and controls. The goal of this GUI is to provide a graphical interface that allows shifters and run coordinators to power different power supplies as well as monitoring their respective outcomes.

## Technology Stack:

- Backend: FastAPI. Go to `192.168.197.46:8000/docs` for more details on the noVNC.
- Frontend: React JS.
- TimeStamp Database: InfluxDB version 1.8.10
- Monitoring: Grafana
- Working on a Podman container with all the required extra packages.

## The Architecture:

This is the architecture for the Slow Controls GUI:

<img width="668" alt="image" src="https://github.com/DUNE/2x2_Slow_Controls/assets/34606228/ed7319db-f185-44a1-8e65-71a036a768d8">

## How to Start the GUI?
First let's ssh to acd-daq05 as acdcs user:

```bash
ssh -J acdcs@acd-gw06.fnal.gov acdcs@acd-daq05.fnal.gov
```
Go to /home/acd/acdcs/2x2/SlowControls2x2/GUI.

Here you have two options:

1. Run GUI in production mode: This is the official GUI that we use for controls and monitoring. To run it just do:

```bash
./run-production.sh
```   
2. Run GUI in development mode: This is the GUI we use for software development. To run it just do:
```bash
./run-dev.sh
```

We won't cover the details on development mode, just notice that this dev container does not run on detached mode so we can easily see errors in real time on our terminal. Production mode runs on detached mode so it keeps running even after user logging out.

To list all running containers you can do:

```bash
podman ps
```

To stop a container you just need to do:

```bash
podman stop {CONTAINER ID}
```

![image](https://github.com/DUNE/2x2_Slow_Controls/assets/34606228/67161b77-7e86-4f93-b030-04d19161daea)

From the screenshot above you can see the following containers running:

- gui_fastapi-app-prod: Container that contains our production backend.
- gui_react-app-prod: Container that contains our production frontend.

Now that these are running, we just need to open a noVNC session. To do this we need to do a tunnel forward from acd-ops01 to a port on our local computer, let's say port 11445:

```bash
ssh -J acdcs@acd-gw06.fnal.gov acdcs@acd-ops01.fnal.gov -L 11445:localhost:443
```

Now you just need to go to your local browser (i.e. Chrome) and open localhost:11445. The password for the noVNC session is argoncube. Once you are there you open Firefox (on the remote vnc) and go to 192.168.197.46:3006, which is the official address of the GUI frontend.

![image](https://github.com/DUNE/2x2_Slow_Controls/assets/34606228/71b02bae-99d2-48f9-aad6-66f4051c9a88)


