# Windows 10 Activation Script
# This script is used to activate Windows 10 using a KMS server. Part of the Win10Act project.

from threading import Thread
import subprocess as s


def __run(commands):

    for i in range(n:=len(commands)):

        c = s.Popen(
            commands[i],
            shell=True
        )
        c.wait()


def run():

    global t

    kms_server = "kms8.msguides.com"

    commands = [
        "cscript //nologo C:\Windows\System32\slmgr.vbs /ipk W269N-WFGWX-YVC9B-4J6C9-T83GX",
        "cscript //nologo C:\Windows\System32\slmgr.vbs /skms %s" % kms_server,
        "cscript //nologo C:\Windows\System32\slmgr.vbs /ato"
    ]

    t = Thread(target=__run, args=(commands,))
    t.start()
