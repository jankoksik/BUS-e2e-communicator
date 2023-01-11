# BUS-e2e-communicator
## czyli projekt bamBUS :bamboo:




# Installation : 
1. go to main folder 
2. run `docker-compose up --build`

# How to use :

When you run app firstly you have to regiser user so make a get request to : 
* http://127.0.0.1:5001/register
* http://127.0.0.1:5002/register

When you have user registered you are free to go. 
Open http://127.0.0.1:5001/chat in your browser. This is client 1. Client 2 is on port 5002 by default.
To send a msg to a new person just simply add ?chch=*username* (you have to change # to - in a nickname)
when you send msg it should show after refresh in other guy window. 

Msgs are encrypted and server can't read em. 

HF using it.

some pics :

![](./test_bus_1.png)
![](./test_bus_2.png)






# Plan : 
<img width="459" alt="daigram1" src="https://user-images.githubusercontent.com/22011659/196692883-cd214401-f7bb-4fd2-b613-b7b5837960f1.png">
<img width="340" alt="daigram2" src="https://user-images.githubusercontent.com/22011659/196692899-66cb91e6-7aaf-4f57-a2f2-218fc5ed4416.png">
<img width="285" alt="daigram3" src="https://user-images.githubusercontent.com/22011659/196692908-abf61ca6-eb86-4467-81a6-f1ad5aeea518.png">
