#!/usr/bin/env python

import uuid
import serial
import time
import urllib2
import urllib


class BadgeInterface:
    def __init__(self):
        pass

    def getPing(self):
        conn = serial.Serial(port="/dev/ttyACM0",baudrate=115200,
                             interCharTimeout=True)
        conn.open()
        conn.write("t")
        conn.write("i")
        pingId = conn.read(8)
        conn.write("t")
        conn.close()
        return pingId

    def getBase(self):
        baseId = uuid.uuid5(uuid.NAMESPACE_DNS,"RVASEC{HACKRVA}")
        return baseId        

class BaseAppUpdater:
    url = 'http://script.google.com/macros/s/AKfycbxATodeGFzqYNKfiXggEM1uaBVX1vd52hYcya43Y7qVGQmdTZS_/exec'
    cookie = None

    def __init__(self):
        pass

    def logPing(self,baseId,pingId):
        url = self.url
        request_headers = urllib.urlencode({"baseId":str(baseId),"pingId":pingId})
        full_url = url + '?' + request_headers
        response = urllib2.urlopen(full_url)
        print response.read()

badge = BadgeInterface()
baseId = badge.getBase()
pingId = badge.getPing()

updater = BaseAppUpdater()
updater.logPing(pingId,baseId)
