#!venv/bin/python
"""
Some utilities for working with Betaflight (and derivatives).
"""
import argparse
import logging
import os
import sys

import serial
from yamspy import MSPy

if os.name == 'nt':  # sys.platform == 'win32':
    from serial.tools.list_ports_windows import comports
elif os.name == 'posix':
    from serial.tools.list_ports_posix import comports


def main():
    """
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("dump",
                          help="Dump and diff the connected flight controller into <name>/BTFL_<version>_DUMP.txt (as well as -DIFF.txt)")
    parser_load = subparsers.add_parser("load", help="Load a new config")
    parser_load.add_argument("file", help="File to load")
    args = parser.parse_args()

    ports = list(comports())
    serial_port = ports.pop().device

    print(f"Opening serial port: {serial_port}")

    board_config = {}
    with MSPy(serial_port) as board:
        if isinstance(board, int):
            print("Error opening board, try disconnecting and reconnecting")
            sys.exit(1)

        # Most config is retrieved automatically but grab the craft name
        board.send_RAW_msg(MSPy.MSPCodes['MSP_NAME'], data=[])
        dataHandler = board.receive_msg()
        board.process_recv_data(dataHandler)
        board_config = board.CONFIG

    print(
        "Connected to board. Firmware: %s %s" %
        (board_config['flightControllerIdentifier'],
         board_config['flightControllerVersion']))
    print(f"Craft name: {board_config['name']}")

    with serial.Serial(serial_port) as ser:
        activate_cli(ser)

        if args.command == "dump":
            dump_path, diff_path = dump_board(ser, board_config)
            print(f"Written files: {dump_path}, {diff_path}")

        if args.command == "load":
            load_to_board(ser, args.file)
            print(f"Loaded configuration: {args.file}")


def dump_board(ser: serial.Serial, config: dict):
    ident = config['flightControllerIdentifier']
    version = config['flightControllerVersion']
    path = config['name']
    path = path.replace("'", "")  # Seen in Rotorflight

    output_path_dump = f"{path}/{ident}_{version}_DUMP.txt"
    output_path_diff = f"{path}/{ident}_{version}_DIFF.txt"

    dump = ""
    ser.write("dump all\r\n".encode())
    while True:
        line = ser.readline().decode()
        dump += line

        if line == "save\r\n":
            break

    diff = ""
    ser.write("diff all\r\n".encode())
    while True:
        line = ser.readline().decode()
        diff += line

        if line == "save\r\n":
            break

    reset_board(ser)

    # Write the contents out to the filesystem
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

    with open(output_path_dump, "w") as filep:
        filep.write(dump)
    with open(output_path_diff, "w") as filep:
        filep.write(diff)

    return output_path_dump, output_path_diff


def load_to_board(ser: serial.Serial, filename):
    with open(filename, "rb") as filep:
        for line in filep:
            ser.write(line)
            ser.flush()
            print(ser.read_all())
        try:
            ser.write(b"save\r\n")
        except serial.serialutil.SerialException:
            pass


def reset_board(ser: serial.Serial):
    ser.write(b"exit\r\n")
    ser.flush()


def activate_cli(ser: serial.Serial):
    ser.write(b"#\r\n")
    wait_for(ser, b"Entering CLI Mode")


def wait_for(ser: serial.Serial, message):
    while line := ser.readline():
        if message in line:
            return


if __name__ == "__main__":
    main()
