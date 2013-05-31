#!/usr/bin/env python

import uuid
import serial
import time
import urllib2
import urllib
import pprint
import datetime

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
        if pingId == None:
            return None
        else:
            return pingId

    def getStat(self):
        conn = self.conn
        conn.open()
        conn.write('\x20')
        statline = conn.readlines()
        conn.close()
        if statline == None:
            return None
        else:
            return statline

    def getBase(self):
        baseId = uuid.uuid3(uuid.NAMESPACE_DNS,str(uuid.getnode()))
        return baseId

class BaseAppUpdater:
    updateFile = open('./updateFile.csv','a')
    url = 'http://script.google.com/macros/' + \
        's/AKfycbxATodeGFzqYNKfiXggEM1uaBVX1vd52hYcya43Y7qVGQmdTZS_/exec'

    def __init__(self):
        pass

    def inetCheck(self):
        try:
            response = urllib2.urlopen("http://www.google.com")
            return True
        except urllib2.URLError as err:
            pass
        return false

    def logPingToWeb(self,baseId,pings):
        for ping in pings:
            if ping == '\r\x00':
                continue
            url = self.url
            request_headers = urllib.urlencode({"baseId":str(baseId).strip(),
                                                "pingId":str(ping).strip().replace("Ping:","")})
            full_url = url + '?' + request_headers
            response = urllib2.urlopen(full_url)
            print response.read()

    def logPingToFile(self,baseId,pings):
        for ping in pings:
            if ping == '\r\x00':
                continue
            updateFile = self.updateFile
            now = datetime.datetime.now().isoformat()
            updateFile.write("%s,%s,%s\n" % (str(now).strip(),
                                             str(baseId).strip(),
                                             str(ping).strip().replace('Ping:','')))


if __name__ == '__main__':
    badge = BadgeInterface()
    baseId = badge.getBase()
    pings = badge.getPing()

    updater = BaseAppUpdater()
    updater.logPingToFile(baseId,pings)
    updater.updateFile.close()
    if updater.inetCheck():
        updater.logPingToWeb(baseId,pings)

