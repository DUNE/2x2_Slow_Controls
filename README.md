# 2x2_Slow_Controls
This repository contains the code used for setting up the slow controls monitoring system for 2x2.

## Technology Stack:

- Backend: FastAPI. Go to `https://localhost:8000/docs` for more detail on noVNC04.
- Frontend: React JS
- TimeStamp Database: InfluxDB version 1.8.10
- Monitoring: Grafana
- Working on a Docker container with all the required extra packages.

## The Architecture:

This is the architecture for the Slow Controls GUI:

<img width="668" alt="image" src="https://github.com/DUNE/2x2_Slow_Controls/assets/34606228/ed7319db-f185-44a1-8e65-71a036a768d8">

## How to Start this App?
Go to /home/acd/acdemo/SLOW-CONTROLS-GUI on srv04 and run (as admin):

```bash
docker compose up --build
```
Then just go to noVNC04:

```bash
ssh -L 11443:acd-srv04.fnal.gov:443 acdemo@acd-gw04.fnal.gov
```
In here, open a browser (if not open) and go to:

- localhost:3000 (Grafana)
- localhost:3006 (GUI)
