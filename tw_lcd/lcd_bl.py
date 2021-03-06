#!/usr/bin/env python
# -*- coding: utf-8 -*-
# lcd_bl.py
# switch lcd's back light

import RPi.GPIO as GPIO
import sys

LCD_BL_PIN=7 # PIN7=GPIO4

def main():
    if len(sys.argv) < 2:
        print('Usage: python lcd_bl.py [ON|OFF]')
        return
    else:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(LCD_BL_PIN, GPIO.OUT)
        if sys.argv[1] == 'ON':
            GPIO.output(LCD_BL_PIN, True)
        else:
            GPIO.output(LCD_BL_PIN, False)



if __name__ == '__main__':
    main()
    
        

