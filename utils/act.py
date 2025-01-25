# Windows 10 Activation Script
# This script is used to activate Windows 10 using a KMS server. Part of the Win10Act project.

from threading import Thread
import subprocess as s
import __main__


def __run(commands):

    outputs = []

    for i in range(n:=len(commands)):

        c = s.Popen(
            commands[i],
            shell=True,
            stdout=s.PIPE,
            stderr=s.PIPE,
            universal_newlines=True
        )
        stdout, stderr = c.communicate()
        outputs.append(stdout if stdout else stderr)
    return outputs


def run():

    global t, outputs

    outputs = []
    kms_server = "kms8.msguides.com"

    commands = [
        "cscript //nologo C:\Windows\System32\slmgr.vbs /ipk W269N-WFGWX-YVC9B-4J6C9-T83GX",
        "cscript //nologo C:\Windows\System32\slmgr.vbs /skms %s" % kms_server,
        "cscript //nologo C:\Windows\System32\slmgr.vbs /ato"
    ]

    def store():
        global outputs
        outputs = __run(commands)

    t = Thread(target=store)
    t.start()
