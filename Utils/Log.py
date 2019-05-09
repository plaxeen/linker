#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Log.py
# (c) Oleg Plaxin 2018
# plaxoleg@gmail.com

# -*- coding: utf-8 -*-
import os
import time


class Log:
    def __init__(self):
        self.log_text = '{time} /{level}:{tag}: {message}'

    def info(self, tag, message):
        worker = LogWorker()
        log = self.log_text.format(time=worker.get_sys_time(), tag=tag, level='I', message=message)
        worker.print_log(log)
        worker.save_to_file(log)

    def debug(self, tag, message):
        worker = LogWorker()
        log = self.log_text.format(time=worker.get_sys_time(), tag=tag, level='D', message=message)
        worker.print_log(log)
        worker.send_to_vk(message)
        worker.save_to_file(log)

    def warning(self, tag, message):
        worker = LogWorker()
        log = self.log_text.format(time=worker.get_sys_time(), tag=tag, level='W', message=message)
        worker.print_log(log)
        worker.send_to_vk(message)
        worker.save_to_file(log)

    def error(self, tag, e):
        worker = LogWorker()
        message = f'An error occurred. {e.__class__.__name__}: {str(e)}'
        log = self.log_text.format(time=worker.get_sys_time(), tag=tag, level='E', message=message)
        worker.print_log(log)
        worker.send_to_vk(message)
        worker.save_to_file(log)


class LogWorker:
    def __init__(self):
        self.LOG_PATH = "./Logs/"
        if not os.path.exists(self.LOG_PATH):
            os.makedirs(self.LOG_PATH)

    def get_sys_time(self):
        now = time.localtime()
        nt = time.strftime("%d %b %Y %H:%M:%S", now)
        return nt

    def print_log(self, text):
        print(text.replace("\n", "\n\t\t\t\t\t\t"))

    def send_to_vk(self, text):
        from VK.Vk import VK
        project_admin_vk_id = 140830142
        VK().send_message(project_admin_vk_id, text.replace("\n", "\n\t\t\t\t\t\t"))

    def save_to_file(self, text):
        now = time.localtime()
        log_to_file = open(
            self.LOG_PATH + str(now.tm_year) + str(now.tm_mon) + str(now.tm_mday) + ".log",
            "a",
            encoding="utf-8")
        log_to_file.write(text.replace("\n", "\n\t\t\t\t\t\t") + "\n")
