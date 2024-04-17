# Spellman High Voltage

## How to start the remote monitoring?
Go to /home/acd/acdcs/SlowControls2x2/SpellmanHV on acd-daq05 logged as acdcs an run:

```bash
./monitor.sh
```

## How to activate the controls?

Go to /home/acd/acdcs/SlowControls2x2/SpellmanHV/SPELLMAN

To control the Spellman, the SpellmanEnv must be activated. Do source SpellmanEnv/bin/activate.

The python script to control the Spellman is SpellmanCTL_py3.py. Do python SpellmanCTL_py3.py to see all of the commands you can use to control the Spellman.

There will be 12 commands.

  1. Clear - disables HV.
  2. IsON - returns 1 if HV is on, 0 if off.
  3. Enable - Remotely turns on HV.
  4. Disable - Remotely turns off HV.
  5. GetSP_V - prints voltage set point.
  6. GetSP_I - print current set point.
  7. GetVI - print actual voltage [kV] and current [mA].
  8. SetSP_V - set the setpoint for the voltage [kV].
  9. SetSP_I - set current limit [mA].
  10. OpMode - print operation mode (voltage/current limit).
  11. Status - print status flags.
  12. RampTo - Ramps HV up/down to given voltage [kV].

To use any of these commands, python SpellmanCTL_py3.py <command>. If you are setting a voltage, setting a current, or ramping up/down the Spellman, you must enter a voltage/current after the command. For example, python SpellmanCTL_py3.py RampTo 1. This will ramp the Spellman to 1 kV.
