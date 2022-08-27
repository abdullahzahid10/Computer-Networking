import socket
import threading
from gettext import find
import zlib
import json
import sys
import os
import pyDH

localIP = "127.0.0.1"
localPort = 57900
bufferSize = 1024
listOfAllOrders = []

Client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

Client.bind((localIP, localPort))
print("Server Listening to connections")

lineBreak = "******************************"

def CRC16(x):
    return zlib.adler32(x.encode())

def READY(tableID):
    return json.dumps({
        "cmd": "READY",
        "data": {
            "table_id": tableID
        },
        "status": 200
    })

while (True):

    Pair = Client.recvfrom(bufferSize)
    address = Pair[1]

    message = json.loads(Pair[0])

    if (message["cmd"] == "CREATE"):
        data_json = json.dumps(message["data"])
        CRC16REC = CRC16(data_json)

        if CRC16REC == message["checksum"]:
            message['status'] = "200"
            listOfAllOrders.append(message["data"])
            bytesToSend = str.encode(
                json.dumps({
                    "status": "200"
                })
            )
            print(lineBreak)
            print("Order Details")
            print(lineBreak)
            print(listOfAllOrders)
            print(lineBreak)
            Client.sendto(bytesToSend, address)

    elif (message["cmd"] == "CANCEL"):
        data_json = json.dumps(message["data"])
        CRC16REC = CRC16(data_json)

        if CRC16REC == message["checksum"]:
            for x in range(len(listOfAllOrders)):
                if (listOfAllOrders[x]["table_id"] == message["data"]["table_id"]):
                    del listOfAllOrders[x]
                break

            bytesToSend = str.encode(
                json.dumps({
                    "status": "200",
                    "table_id": message["data"]["table_id"]
                })
            )
            Client.sendto(bytesToSend, address)

            status = input("Status: ")

            if status == "200":
                status = "SUCCESS"
            elif status == "300":
                status = "TECHNICAL MALFUNTION"
            elif status == "400":
                status = "BAD REQUEST"

            print("Order successfully CANCELLED" + "\n" + "Status: " + status)
            print("\nOrders in flow: ")
            print(listOfAllOrders)
            print("\n")

    elif (message["cmd"] == "COMPLETE"):

        data_json = json.dumps(message["data"])
        CRC16REC = CRC16(data_json)

        if CRC16REC == message["checksum"]:
            for x in range(len(listOfAllOrders)):
                if (listOfAllOrders[x]["table_id"] == message["data"]["table_id"]):
                    del listOfAllOrders[x]
                break
            status = input("Status: ")

            if status == "200":
                status = "SUCCESS"
            elif status == "300":
                status = "TECHNICAL MALFUNTION"
            elif status == "400":
                status = "BAD REQUEST"


            print(lineBreak + "\nOrder for table " + message["data"]["table_id"] + " has been successful" + "\n" + "Status: " + status)
            print(lineBreak + "\nOrders in flow: " + "\n" + lineBreak)
            print(listOfAllOrders)
            print("Status: 200" + "\n" + lineBreak)

            bytesToSend = str.encode(
                json.dumps({
                    "status": "200"
                })
            )

            Client.sendto(bytesToSend, address)
