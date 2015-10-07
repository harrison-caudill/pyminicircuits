# PyMiniCircuits

Provides a python interface for interacting with the MiniCircuits
programmable attenuators via USB.  This code may or may not be
extended to work with the Ethernet interface and it may or may not be
extended to incorporate other MiniCircuits devices.

# Installing

```bash
sudo python setup.py install
```

# Examples

```
kungfoo@sasha:~/hid/minicircuits$ sudo mini-attenuator get
125.0
kungfoo@sasha:~/hid/minicircuits$ sudo mini-attenuator set -v 50
50.0
kungfoo@sasha:~/hid/minicircuits$ sudo mini-attenuator get
50.0
```
