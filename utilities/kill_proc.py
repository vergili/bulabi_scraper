#!/usr/bin/env python
import psutil
from datetime import datetime
from datetime import timedelta


for pid in psutil.pids():
    try:
        p = psutil.Process(pid)

        if p.name() == 'chrome' or p.name() == 'chromedriver':

            create_time = datetime.fromtimestamp(p.create_time())
            print create_time, pid,  p.name()

            c10 = create_time + timedelta(minutes=10)
            print p.name()

            if c10 < datetime.now():
                print 'process...:' + str(pid) + ' ' + str(p.name) + ' killing.....'
                p.kill()
    except:
        pass



"""
for process in psutil.process_iter():
    pid = process.pid
    cmdline = process.cmdline
    if what_im_looking_for in cmdline:
        p = psutil.Process(pid)
        p.create_time
        pidcreated = datetime.datetime.fromtimestamp(p.create_time)
        allowed_time = pidcreated + datetime.timedelta( 0, 5400 )
        now = datetime.datetime.now()
        if now > allowed_time:
            print "Killing process {} Start time: {} Current time: {}".format( pid, pidcreated, now)
            p.kill()
"""
