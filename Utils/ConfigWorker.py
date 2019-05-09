#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ConfigWorker.py
# (c) Oleg Plaxin 2018
# plaxoleg@gmail.com

# -*- coding: utf-8 -*-
import configparser
import os
CONFIG_PATH = "./Utils/Config/main.ini"


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()

    def save(self):
        with open(CONFIG_PATH, "w") as config_file:
            self.config.write(config_file)

    def read(self, conf, param):
        if not os.path.exists(CONFIG_PATH):
            self.save()

        self.config.read(CONFIG_PATH)
        return self.config.get(conf, param)

    def add(self, conf, param, value):
        if not self.config.has_section(conf):
            self.config.add_section(conf)
        self.config.set(conf, param, value)
        self.save()

