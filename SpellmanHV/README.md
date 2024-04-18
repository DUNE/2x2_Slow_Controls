# Spellman High Voltage

## How to start the remote monitoring?
Go to /home/acd/acdcs/SlowControls2x2/SpellmanHV on acd-daq05 logged as acdcs an run:

```bash
./monitor.sh
```

## How to activate the controls?

Go to /home/acd/acdcs/SlowControls2x2/SpellmanHV/SPELLMAN

To control the Spellman, the SpellmanEnv must be activated. 
```bash
source SpellmanEnv/bin/activate
```

The python script to control the Spellman is SpellmanCTL_py3.py. Do python SpellmanCTL_py3.py to see all of the commands you can use to control the Spellman.

There will be 12 commands to give:

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

To use any of these commands besides SetSP_V, SetSP_I, or RampTo, run:

```bash
python SpellmanCTL_py3.py <command>
```

For setting a voltage, setting a current, or ramping up/down the Spellman, you will have to enter two arguments after python SpellmanCTL_py3.py. The argument will have to be in the order command then value. The units for the value you enter will either be in kV or mA depending on whether you are setting the voltage, setting the current, or ramping the voltage.

To run the commands SetSP_V, SetSP_I, or RampTo:

```bash
python SpellmanCTL_py3.py <command> <value>
```

