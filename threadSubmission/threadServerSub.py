#! /usr/bin/env python3
import sys, os, socket, params, time
from threading import Thread
from framedSock import FramedStreamSock

#start by creating a file for writing all transfered files. This will just reset for every different server. Essentially you lose them
#once you start a new server. 

curDir =os.path.dirname(os.path.abspath(__file__))
strPath = curDir + r'/serverStorage'
strNum = 0
notUnique = True
while(notUnique):
    if not os.path.exists(strPath):
        os.makedirs(strPath) 
        notUnique = False 
    else: 
        strPath = strPath + str(strNum)
        strNum = strNum + 1 
#should have storage folder now. 

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50002),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

class ServerThread(Thread):
    requestCount = 0            # one instance / class
    def __init__(self, sock, debug):
        Thread.__init__(self)
        self.fsock, self.debug = FramedStreamSock(sock, debug), debug
        self.start()
    def run(self):
        from os import listdir #these three lines implement a method get all file names in a folder efficiently. I took this from: https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory#3207973
        from os.path import isfile, join
        while True:
            fileDict = [f for f in listdir(strPath) if isfile(join(strPath, f))] #line three referenced above. 

            payload = self.fsock.receivemsg()
            
            if not payload:
                if self.debug: print(self.fsock, "server thread done")
                return    


            print("read: " + payload)
            
            cmds = payload.split()
            
 
            msg = ("%s (%s)" % ("Wrote", payload)).encode()
            self.fsock.sendmsg(msg)






while True:
    sock, addr = lsock.accept()
    ServerThread(sock, debug)
