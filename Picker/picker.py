#!/usr/bin/env python3
import requests
import json
import curses
import Picker
import Config
import threading
import Modules
import time




def main():
    p = Picker.Picker()
    conf = Config.Config()
    
    github = Modules.Github(conf, p)
    jenkins = Modules.Jenkins(conf, p)
    jira = Modules.Jira(conf, p)

    time.sleep(2)
    print(p.pick())


if __name__ == '__main__':
    main()
