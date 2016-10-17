This is a quick and dirty little Python script to help prevent theft of USB
devices, e.g. at exhibits. You could run it on a laptop that is well secured,
and connect any number of phones, tablets or other USB devices to it.

## Requirements

- Linux (because of udev use)
- Python 2 (in `/usr/bin/python2`)
- pygame (e.g. `pip install pygame`)
- pyudev (e.g. `pip install pyudev`)

## Usage

At startup, the program enumerates the connected devices, so make sure all
devices you want to secure are connected. (If not, use the 'reset' command
afterwards.)

The program sounds an alarm if a USB cable is unplugged, and flashes the screen
black and white. The alarm can be silenced only by plugging the device back in,
or by typing 'reset' (in the blind). Typing 'exit' (again in the blind) will
quit the program.

Of course there are a number of security flaws with this approach, but it's
better than nothing.

## License

This software is in the public domain.
