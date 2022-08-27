import socket
import json
import zlib
import threading
import sys
import os
import binascii
import pyDH
import test1
import test2


d1 = test1.client["d1"]
d2 = test2.server["d2"]


d1_pubkey = d1.gen_public_key()
d2_pubkey = d2.gen_public_key()
d1_sharedkey = d1.gen_shared_key(d2_pubkey)
d2_sharedkey = d2.gen_shared_key(d1_pubkey)

sen1 = "DH Key matches: "
sen1Statement = d1_sharedkey == d2_sharedkey

if sen1Statement == True:
        sen1Statement = "True"
else:
        sen1Statement = "False"

    # print(d1_sharedkey == d2_sharedkey)
lineBreak = "**********"
# print(lineBreak)
# print(sen1 + sen1Statement)
# print(lineBreak)
# print("Public Keys")
# print(lineBreak)
# print("Client Public Key")
# print(d1_pubkey)
# print("Server Public Key")
# print(d2_pubkey)
# print("Shared Keys")
# print(lineBreak)
# print("Client Shared Key")
# print(d1_sharedkey)
# print("Server Shared Key")
# print(d2_sharedkey)

lineBreak = "******************************"

print(lineBreak)
print("Client-Server connection ESTABLISHED")
print(lineBreak)
waiterID = input("Enter waiter ID: ")
tableStatus = []

# d1 = pyDH.DiffieHellman()
# d1_pubkey = d1.gen_public_key()
# d1_sharedkey = d1.gen_shared_key(d2_pubkey)


def CRC16(x):
    return zlib.adler32(x.encode())

# def CS(bitstring: str) -> str:
#         print(bitstring)
#         return "{0:016b}".format(binascii.crc_hqx(__bitstring_to_bytes(bitstring), 0))
#
# def __bitstring_to_bytes(s: str):
#         return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')
#
# def __string_to_bitstring(s: str):
#         ords = (ord(c) for c in s)
#         shifts = (7, 6, 5, 4, 3, 2, 1, 0)
#         bitlist = [str((o >> shift) & 1) for o in ords for shift in shifts]
#         bitstring = ''.join(bitlist)
#         return bitstring
#
#
#
# def __map_payload_to_dict(payload: bytes):
#
#         bitstring = BitArray(bytes=payload).bin
#
#         __log(f"recieved {len(bitstring)} bits")
#
#         checksum = bitstring[0:16]
#         incrementer = 16
#         SYN = bitstring[incrementer]
#         incrementer = incrementer + 1
#         ACK = bitstring[incrementer]
#         incrementer = incrementer + 1
#         FIN = bitstring[incrementer]
#         incrementer = incrementer + 1
#         COR = bitstring[incrementer]
#         sequence_number = bitstring[20:32]
#         body = bitstring[32:]
#
#         expCS = __calculate_checksum(bitstring[16:])
#
#         crpt = not True
#         if checksum == expCS:
#             __log("CHECKSUM*MATCH*")
#         else:
#             __log("CHECKSUM*MISMATCH*")
#             crpt = True
#
#         bytesInBody = __bitstring_to_bytes(body)
#
#         sequence_number_int = int(sequence_number, 2)
#
#         payload_dict = {
#             "syn": int(syn),
#             "ack": int(ack),
#             "fin": int(fin),
#             "cor": int(cor),
#             "sequence_number": sequence_number_int,
#             "checksum": checksum,
#             "body": json.loads(bytesInBody),
#         }
#
#         return payload_dict, crpt

def CREATE(waiter_ID, table_id):
    order = []

    ItemsToOrder = input("What would you like to order: ")
    ItemsToOrder = ItemsToOrder.upper()
    order.append(ItemsToOrder)

    additionalItems = True
    while (additionalItems):
        ItemsToOrder = input(lineBreak + "\nWould you like to order something else, if not, hit [x]:  " + "\n" + lineBreak + "\n")
        ItemsToOrder = ItemsToOrder.upper()
        if (ItemsToOrder == 'X'):
            additionalItems = False
        else:
            order.append(ItemsToOrder)

    data = {
        "Waiter ID": waiter_ID,
        "table_id": table_id,
        "order": order
    }

    # bitstring = __string_to_bitstring(json.dumps(data))
    # checkSum = CS(bitstring)
    checkSum = CRC16(json.dumps(data))

    return json.dumps({
        "cmd": "CREATE",
        "checksum": checkSum,
        "data": {
            "Waiter ID": waiter_ID,
            "table_id": table_id,
            "order": order
        },
        "status": ""
    })

def CANCEL(table_id):
    data = {
        "table_id": table_id
    }

    # bitstring = __string_to_bitstring(json.dumps(data))
    #
    # checkSum = CS(bitstring)

    checkSum = CRC16(json.dumps(data))


    return json.dumps({
        "cmd": "CANCEL",
        "checksum": checkSum,
        "data": {
            "table_id": table_id
        },
        "status": "",
    })

def COMPLETE(table_id):
    data = {
        "table_id": table_id
    }

    # checkSum = CS(json.dumps(data))
    checkSum = CRC16(json.dumps(data))


    return json.dumps({
        "cmd": "COMPLETE",
        "checksum": checkSum,
        "data": {
            "table_id": table_id
        },
        "status": ""
    })

Port = ("127.0.0.1", 57900)
bufferSize = 1024

Client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

while (True):

    print(lineBreak + "\nChoose an option: \n-Enter Create to create order \n-Cancel to cancel order \n-Complete to complete order\n" + lineBreak)
    print("*** TO CHECK DIFFIE HELLMAN STATUS TYPE DH ***")
    choice = input("Enter CREATE to create an order, CANCEL to cancel an existing order and COMPLETE to complete an order ")
    choice = choice.upper()

    if "CREATE" in choice:
        table = input("table ID: ")
        tableStatus.append(table)

        commandsJS = CREATE(waiterID, table)
        Bytes = str.encode(commandsJS)
        Client.sendto(Bytes, Port)

        msg = Client.recvfrom(bufferSize)
        msgjson = json.loads(msg[0])

        print()
        print("Status: " + msgjson["status"])
        if msgjson["status"] == "200":
            print("Order Recieved")
        print()

    if "DH" in choice:
        print(lineBreak)
        print(sen1 + sen1Statement)
        print(lineBreak)
        print("Public Keys")
        print(lineBreak)
        print("Client Public Key")
        print(d1_pubkey)
        print("Server Public Key")
        print(d2_pubkey)
        print("Shared Keys")
        print(lineBreak)
        print("Client Shared Key")
        print(d1_sharedkey)
        print("Server Shared Key")
        print(d2_sharedkey)

    if "CANCEL" in choice:
        table = input("Enter table ID: ")
        commandsJS = CANCEL(table)
        Bytes = str.encode(commandsJS)
        Client.sendto(Bytes, Port)

        msg = Client.recvfrom(bufferSize)
        msgjson = json.loads(msg[0])

        print()
        print("Status: " + msgjson["status"])
        if msgjson["status"] == "200":
            print(lineBreak + "\nTable " + msgjson["table_id"] + " has now been cancelled" + "\n" + lineBreak)
        print()

    if "COMPLETE" in choice:
        table = input("Enter table ID: ")
        commandsJS = COMPLETE(table)
        Bytes = str.encode(commandsJS)
        Client.sendto(Bytes, Port)

        msg = Client.recvfrom(bufferSize)
        msgjson = json.loads(msg[0])

        print()
        if msgjson["status"] == '200':
            print("ORDER PROCESSED")
            print("Status: " + msgjson["status"])
            print()
