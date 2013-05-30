#!/usr/bin/env python

import uuid
import serial
import time
import urllib2
import urllib
import pprint

class BadgeInterface:

    conn = serial.Serial(port="/dev/ttyACM0",baudrate=115200,
                         timeout=3)

    def __init__(self):
        pass

    def getPing(self):
        conn = self.conn
        conn.open()
        conn.write("t")
        conn.write("i")
        pingId = conn.readlines()
        conn.write("t")
        conn.close()
        return pingId

    def getStat(self):
        conn = self.conn
        conn.open()
        conn.write('\x20')
        statline = conn.readlines()
        conn.close()
        return statline

    def getBase(self):
        baseId = uuid.uuid5(uuid.NAMESPACE_DNS,"RVASEC{HACKRVA}")
        return baseId        

class BaseAppUpdater:
    url = 'http://script.google.com/macros/s/AKfycbxATodeGFzqYNKfiXggEM1uaBVX1vd52hYcya43Y7qVGQmdTZS_/exec'

    def __init__(self):
        pass

    def logPing(self,baseId,pings):
        for ping in pings:
            if ping == '\r\x00':
                continue            
            url = self.url
            request_headers = urllib.urlencode({"baseId":str(baseId),"pingId":ping})
            full_url = url + '?' + request_headers
            response = urllib2.urlopen(full_url)
            print response.read()

badge = BadgeInterface()
baseId = badge.getBase()
pings = badge.getPing()

updater = BaseAppUpdater()
updater.logPing(baseId,pings)
