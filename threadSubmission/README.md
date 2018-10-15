<h1>THREAD LAB SUBMISSION FOLDER</h1>


This folder contains all the files pertaining to my server and client solution. 
The 2 python programs that implement the client and server are threadClientSub.py and threadServer.py. 


<h3>Running Information: </h3>
To run these programs you must in the proper directory input: 
    <h4>'Python3 threadServerSub.py'</h4> 
and 
    <h4>'Python3 threadClientSub.py'</h4>

The server's default listening port is 50007. You must specify the proper connection path and port to link the client and 
server together. 

<h3>Client Program Information:</h3>

The program for the client works by using a thread to behave as the client. I embedded a race condition test within my code to
generate lots of threads writing to the same file to ensure that the locking mechanism used works. This program works by 
displaying a menu allowing the user to input file names the user wishes to transfer. After specifying the file to transfer, the 
cmd prompt will display exactly what the server receives to ensure that it properly transfers data. It is important to note that 
my program will store any file it is told to even if it doesn't exist on the client side. This program also sometimes after writing 
doesn't redisplay the menu, when this happens if you press enter again it will actually bring up the display and can be used. Furthermore, 
even if the server states some bad reads it will still properly store the files, so it is safe to ignore those. I left 
all feedback and debugging prints to ensure that the user can see what the program is doing. 

<h3>Server Program Information:</h3>

The program for the server works by creating new threads for each new client that joins. This server program will overwrite files 
if the user tries to send a file that they already have stored in the server. Furthermore, this program works by having some triggers that 
it recognizes to do certain commands. This program will work with a proxy inbetween as well due to the fact that all of the messages are 
framed.

<h3>Final Notes:</h3>

Lastly, it is important to note that there are minimal exception catches in both programs. Thus, these two programs aren't the most robust
solutions out there for a client and server. That said they will work as intended even if there are some exceptions that display during 
running. Furthermore, I believe that it is fair to overwrite files when written by multiple clients. This is no different then what 
github would do, except that my server does not keep track of versions and changes. 
