#!/usr/bin/env python3
import requests
import argparse
import subprocess
import os
import configparser
import json
import curses
from . import Picker
import threading
from . import Modules
import time
import logging


def create_log_dir():
    try:
        os.makedirs(os.path.expanduser('~/.cache/picker/'))
    except FileExistsError:
        pass


def main():
    parser = argparse.ArgumentParser(description='Picker')
    parser.add_argument('-d', '--debug', action='store_true', default=False, help='Set log level to debug')
    parser.add_argument('-e', '--error-stdout', action='store_true', default=False,
                        help='Do not start curses interface and output logs to stdout')
    args = parser.parse_args()
    start(args)


def start(args):
    create_log_dir()
    args.debug = True
    args.error_stdout = True
    # init log
    logger = logging.getLogger('picker')
    filehandler = logging.FileHandler(os.path.expanduser('~/.cache/picker/picker.log'))

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    filehandler.setFormatter(formatter)
    if args.debug:
        lvl = logging.DEBUG
    else:
        lvl = logging.WARNING

    logger.setLevel(lvl)
    filehandler.setLevel(lvl)
    logger.addHandler(filehandler)
    if args.error_stdout:
        consolehandler = logging.StreamHandler()
        consolehandler.setLevel(lvl)
        consolehandler.setFormatter(formatter)
        logger.addHandler(consolehandler)

    conf_file = os.path.expanduser('~/.config/picker/picker.conf')
    config = configparser.ConfigParser()
    config.read(conf_file)

    modules_lst = []

    general_config = {}
    for section in config.sections():
        if section.lower() == 'general':
            general_config = config[section]

    p = Picker(general_config)

    for section in config.sections():
        if section.lower() == 'general':
            pass
        else:
            if 'type' not in config[section]:
                raise Exception('Section does not specify type [%s]' % section)
            elif config[section]['type'] == 'github':
                modules_lst.append(Modules.Github(config[section], p))
            elif config[section]['type'] == 'jenkins':
                modules_lst.append(Modules.Jenkins(config[section], p))
            elif config[section]['type'] == 'jira':
                modules_lst.append(Modules.Jira(config[section], p))
            else:
                raise Exception('Unhandled type [%s] for section [%s]' % (config[section]['type'], section))

    if not args.error_stdout:
        res = p.pick()
        if res:
            subprocess.check_output(['xdg-open', res[2]])
    else:
        try:
            time.sleep(100)
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()
