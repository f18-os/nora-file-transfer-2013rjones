#! /usr/bin/env python3
#This code initially started as a mix of how to use mutex taken from: https://stackoverflow.com/questions/3310049/proper-use-of-mutexes-in-python#3311157 for a general implementation and outline on how to use mutex then a combo of the framedThreadedClient provided by Dr.Freudenthal.

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


def processData(data, thread_safe, fileNameProvided):
    if thread_safe:
        mutex.acquire()
    try:
        thread_id = threading.get_ident()
        #print('\nProcessing data:', data, "ThreadId:", thread_id)
        fs = FramedStreamSock(s, debug=debug) 
        #so we know that we have a file to process. 
        
        
        #modified logic for processing files here. 
        
        SendDet = "-StrFl "+ fileNameProvided.strip()
        fs.sendmsg(SendDet.encode('utf-8'))
        print("received:", fs.receivemsg())

        
        cnt = 0
                                
        try:
            with open(fileNameProvided) as f:
                for line in f:#loop through all lines if they are small enough send else split in two and tack detail to end. 
                    if(sys.getsizeof(line) <= 100): 
                    #send
                        if(line.strip() != ""):
                            print("Sending line. " + line)
                            fs.sendmsg(line.encode('utf-8'))
                            print("received:", fs.receivemsg())
                            
                            
                        else: 
                            print("Sending line. EMPTYLINE" )
                            
                            fs.sendmsg("EMPTYLINE".encode('utf-8'))
                            print("received:", fs.receivemsg())
                        
                    else:
                        totSizeLine = sys.getsizeof(line)
                        #print("Total line size: "+ str(totSizeLine))
                        notDone = True
                        cnt = 0
                        while(notDone):#this loop sends lines that are too big by breaking them up. 
                            totSizeLineRem = totSizeLine - (98*cnt)
                            if(totSizeLineRem > 98): 
                                cnt = cnt + 1 
                                valLoop = totSizeLineRem / 98 
                                looping = True
                                totLoop = 0 
                                while(looping): 
                                    if(valLoop <= totLoop):
                                        looping = False
                                        
                                        fs.sendmsg("NEWLINE".encode('utf-8'))
                                        print("received:", fs.receivemsg())
                                        
                                        fs.sendmsg("DONELINE".encode('utf-8'))
                                        print("received:", fs.receivemsg())
                                        notDone = False 
                                    else:    
                                        lineSending = "PL "+ line[(0+(98*totLoop)):(98 + (98*totLoop))]
                                        print("LineSending: "+ lineSending)
                                        
                                        fs.sendmsg(lineSending.encode('utf-8'))
                                        print("received:", fs.receivemsg())
                                        totLoop = totLoop + 1 


        except Exception as e:
            print(e)
            print("Error during byte writing.")
    
        f.close()
        #tell server we are done writing 
        SendDet = "-cmd CloseFileWritingChunks"
        framedSend(s, SendDet.encode('utf-8') , debug)
        print("received:", framedReceive(s, debug))
        
        #SendDet = "Processing data: = " + str(data) 
        #fs.sendmsg(SendDet.encode('utf-8'))
        #print("received:", fs.receivemsg())
        
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
            

test = False  #sends file repeatedly on different threads.  
counter = 0
max_run = 100
thread_safe = True
cmd = 0; 
totSizeLineRem = 0
cont = True 
try: #this is to catch any errors with connection to server
    while(cont): #coninuous loop for menu. 
        print(" ")
        print("Please enter:")
        print("             0 to send a file to a server")
        #print("             1 to display files on server")  Not including this feature. 
        print("             2 to exit")
        try:
            cmd = input("Please input number corresponding to command.")
            if((cmd == 0 or 2 )):
                try: 
                    if((cmd == "0")):
                        print("Sending a file to a server.")
                        fileNameProvided = input('Please input file and or file path to transfer: ')
                        
                        print("File Name: "+ fileNameProvided)
                
                        while True:
                            some_data = counter        
                            t = Thread(target=processData, args=(some_data, thread_safe, fileNameProvided))
                            t.start()
                            counter = counter + 1
                            if counter >= max_run:
                                break
                                
                    if((cmd == "2")):
                        cont = False 
                        exit()
                except: 
                    print("Exiting")  
        
        except: 
            print("Error in taking input")            
except: 
    print("Error in processing")