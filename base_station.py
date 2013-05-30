#!/usr/bin/env python

import uuid
import serial
import time
import urllib2
import urllib

conn = serial.Serial(port="/dev/ttyACM0",baudrate=115200,
                     interCharTimeout=True)
baseId = uuid.uuid1()
print "Base is: " + str(baseId)
conn.open()
conn.write("t")
conn.write("i")
pingId = conn.read(8)
conn.write("t")
conn.close()


class BaseAppUpdater:
    url = 'https://script.google.com/macros/s/AKfycbxATodeGFzqYNKfiXggEM1uaBVX1vd52hYcya43Y7qVGQmdTZS_/exec'
    cookie = None

    def __init__(self):
        pass

    def authenticate(self):
        url = self.url
        req = urllib2.Request(url)
        response = urllib2.urlopen(url)
        self.cookie = response.headers.get('Set-Cookie')

    def logPing(self,baseId,pingId):
        url = self.url
        request_headers = urllib.urlencode({"baseId":baseId,"pingId":pingId})

        req = urllib2.Request(url + "?" + request_headers)
        print request_headers
        response = urllib2.urlopen(url)
        print response.read()

updater = BaseAppUpdater()
updater.authenticate()
updater.logPing(pingId,baseId)

