#!/usr/bin/env python3
import requests
import os
import configparser
import json
import curses
import Picker
import threading
import Modules
import time


def main():
    conf_file = os.path.expanduser('~/.config/picker/picker.conf')
    config = configparser.ConfigParser()
    config.read(conf_file)

    modules_lst = []

    general_config = {}
    for section in config.sections():
        if section.lower() == 'general':
            general_config = config[section]

    p = Picker.Picker(general_config)

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

    print(p.pick())


if __name__ == '__main__':
    main()
