#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
# 
# Copyright (c) 2016 Yuma.M
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from __future__ import print_function

import sys
import time
import smbus
import unicodedata

from config import BUS_NUMBER, LCD_ADDR, SLEEP_TIME, DELAY_TIME
from character_table import INITIALIZE_CODES, LINEBREAK_CODE, CHAR_TABLE

COMMAND_ADDR = 0x00
DATA_ADDR = 0x80


class LCDController:
    def __init__(self):
        self.bus = smbus.SMBus(BUS_NUMBER)
        pass

    def send_command(self, command, is_data=True):
        if is_data:
            self.bus.write_i2c_block_data(LCD_ADDR, DATA_ADDR, [command])
        else:
            self.bus.write_i2c_block_data(LCD_ADDR, COMMAND_ADDR, [command])
        time.sleep(DELAY_TIME)

    def initialize_display(self):
        for code in INITIALIZE_CODES:
            self.send_command(code, is_data=False)

    def send_linebreak(self):
        for code in LINEBREAK_CODE:
            self.send_command(code, is_data=False)

    def normalize_message(self, message):
        if isinstance(message, str):
            message = message.decode('utf-8')
        return unicodedata.normalize('NFKC', message)

    def convert_message(self, message):
        char_code_list = []
        for char in message:
            if char not in CHAR_TABLE:
                error_message = 'undefined character: %s' % (char.encode('utf-8'))
                raise ValueError(error_message)
            char_code_list += CHAR_TABLE[char]
        if len(char_code_list) > 16:
            raise ValueError('Exceeds maximum length of characters for each line: 16')
        return char_code_list

    def display_one_line(self, line_no, message):
        message = self.normalize_message(message)
        char_code_list = self.convert_message(message)
        for code in char_code_list:
            self.send_command(code)

    def display_messages(self, message_list):
        self.initialize_display()
        time.sleep(SLEEP_TIME)
        for line_no, message in enumerate(message_list):
            if line_no == 1:
                self.send_linebreak()
            self.display_one_line(line_no, message)


def main():
    if not 2 <= len(sys.argv) <= 3:
        print('Usage: python raspi_lcd.py "message for line 1" ["message for line 2"]')
        return
    else:
        lcd_controller = LCDController()
        lcd_controller.display_messages(sys.argv[1:3])

if __name__ == '__main__':
    main()
