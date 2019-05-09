#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# LINKER
# (c) Oleg Plaxin 2019
# plaxoleg@gmail.com

# -*- coding: utf-8 -*-
from Utils.Log import Log
from VK.Vk import VK


def main():
    Log().debug(tag, 'Корректный запуск.')
    VK().long_poll()


if __name__ == '__main__':
    tag = 'MAIN'
    while True:
        try:
            main()
        except Exception as e:
            Log().error(tag, e)
