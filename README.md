# iseg-hv-controller
(Note: this file is written by users, not by the software author.)

> A python package giving command-line access to the `iseg_libs` provided by the manufacturer.
> Configuration of the High-Voltage crate can be provided in toml files.

## Installation
Install the requirements listed in `requirements.txt` with:
```bash
cd iseg-hv-controller
pip install -r requirements.txt
```

### Using Poetry
(No idea... and no time to test it.)

## Usage

Start the command-line interpreter with
```bash
python -m isegcontroller
```
You can specify the following arguments:
- `-h`: Print help on usage of the program.
- `-f FILENAME`: Load the `toml` file `FILENAME` to configure the HV crate.
- `-c COMMAND`: Execute the command `COMMAND` and exit.
- `-i`: Start in interactive mode.

## Commands

The CLI provides the following commands (see `isegcontroller/interpreter.py`):
- `help` and `help <cmd>`: display general help or detailed help and syntax for the command `<cmd>`.
- `ch`: View or modify a channel.
- `rampspeed`: Set the crate ramp speed.
- `reset`: Re-apply the given configuration file (or isegcontroller default) to the crate.
- `config`: Load and apply the given configuration file.
- `info`: Print information on the HV crate.
- `defaults`: Apply the settings in the section "default" of the configuration file to all channel.
- `all`: Apply the given value to all channels.
- `quit`: Exit the programm.
