#! /usr/bin/env python3

# Echo client program
import socket, sys, re,os
import params
from framedSock import FramedStreamSock
from threading import Thread, Lock
import threading
import time

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

tosSizeLineRem = 0
progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)
dirPath = os.path.dirname(os.path.realpath(__file__))
server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

mutex = Lock()


def processData(data, thread_safe):
    if thread_safe:
        mutex.acquire()
    try:
        thread_id = threading.get_ident()
        #print('\nProcessing data:', data, "ThreadId:", thread_id)
        fs = FramedStreamSock(s, debug=debug) 
        SendDet = "Processing data: = " + str(data) 
        fs.sendmsg(SendDet.encode('utf-8'))
        print("received:", fs.receivemsg())
        
        #framedSend(s, SendDet.encode('utf-8') , debug)
    finally:
        if thread_safe:
            mutex.release()


tryConnect = True 
while(tryConnect): #This portion will loop and try to repeatedly take server sockets if there is an issue with connecting. 
    
    serverParse1 = input("Please input server ip address you wish to connect to: ")

        
    serverParse = str(input("Please input server socket you wish to connect to: "))

    if(serverParse.strip() != ""): 
        server = serverParse1.strip() + ":" + str(serverParse).strip()

    if usage:
        params.usage()


    try:
        serverHost, serverPort = re.split(":", server)
        serverPort = int(serverPort)
    except:
        print("Can't parse server:port from '%s'" % server)
        sys.exit(1)

    s = None
    for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        
        try:
            print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            print(" error: %s" % msg)
            s = None
            continue
        try:
            print(" attempting to connect to %s" % repr(sa))
            s.connect(sa)
            tryConnect = False
        except socket.error as msg:
            print(" error: %s" % msg)
            s.close()
            s = None
            continue
        break

    if s is None:
        print('could not open socket')
        print("")
            



counter = 0
max_run = 100
thread_safe = False
while True:
    some_data = counter        
    t = Thread(target=processData, args=(some_data, thread_safe))
    t.start()
    counter = counter + 1
    if counter >= max_run:
        break
