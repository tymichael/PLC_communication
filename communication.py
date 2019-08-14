# Copyright (c) Michael.
"""
File    : communication.py
Brief   : Connect to PLC use ModbusTcp.
Author  : Michael
Date    : 2019/07/23
Modify  : MOD.19072515 by Michael 新增類別ModbusTcp
"""
import socket
import struct
import time

MODBUS_TCP_MAX_DATA=255

MODBUS_TCP_TRNSACTION_IDENTIFIER = 0x0001

MODBUS_TCP_PROTOCOL_IDENTIFIER=0x0000

MODBUS_TCP_DATA_LENGTH = 0x0006

READ_DIGITAL_OUTPUT_STATUS = 0x01
READ_DIGITAL_INPUT_STATUS = 0x02
READ_ANALOG_OUTPUT_STATUS = 0x03
READ_ANALOG_INPUT_STATUS = 0x04
WRITE_DIGITAL_OUTPUT_VALU = 0x05
WRITE_ANALOG_OUTPUT_VALUE = 0x06
WRITE_MULTI_DIGITAL_OUTPUT_VALUE = 0x15
WRITE_MULTI_ANALOG_OUTPUT_VALUE = 0x16

READ_DIGITAL_OUTPUT_STATUS_EXCEPTION_RESPONSE = 0x81
READ_DIGITAL_INPUT_STATUS_EXCEPTION_RESPONSE = 0x82
READ_ANALOG_OUTPUT_STATUS_EXCEPTION_RESPONSE = 0x83
READ_ANALOG_INPUT_STATUS_EXCEPTION_RESPONSE = 0x84
WRITE_DIGITAL_OUTPUT_VALUE_EXCEPTION_RESPONSE = 0x85
WRITE_ANALOG_OUTPUT_VALUE_EXCEPTION_RESPONSE = 0x86
WRITE_MULTI_DIGITAL_OUTPUT_VALUE_EXCEPTION_RESPONSE = 0x8F
WRITE_MULTI_ANALOG_OUTPUT_VALUE_EXCEPTION_RESPONSE = 0x90

# ---MOD.19072515 by Michael(S)---
class ModbusTcp:
    """
    Communicate with PLC using modbus tcp.
    Attributes:
        address: A set indicating PLC address.
        device_address = A int indicating PLC device address.
        conect(): A public function indicating connect to PLC.
        disconnect(): A public function indicating disconnect to PLC.
        __read_packet(): A private function indicating read received packet from PLC.
        __send_packet(): A private function indicating send packet from PLC.
        read_holding_registers(): A public function read holding registers from PLC.
    """

    def __init__(self, plc_ip, plc_port, device_address):
        self.address = (plc_ip, int(plc_port))
        self.device_address = int(device_address)
        self.connect()

    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = self.s.connect(self.address)
        if result:
            print ("CONNECT ERROR!")
            return -1
        else:
            return 0

    def disconnect(self):
        self.s.close()
        
    def __read_packet(self):
        return self.s.recv(MODBUS_TCP_MAX_DATA)
    
    def __send_packet(self, function_code, register_address, query_length):
        buffer = struct.pack('>3H2B2H', MODBUS_TCP_TRNSACTION_IDENTIFIER, MODBUS_TCP_PROTOCOL_IDENTIFIER
                                      , MODBUS_TCP_DATA_LENGTH,           self.device_address
                                      , function_code,                    register_address
                                      , query_length)
        self.s.send(buffer)

    def read_holding_registers(self, register_address, query_length):
        self.__send_packet(READ_ANALOG_OUTPUT_STATUS, int(register_address), query_length)
        result = self.__read_packet()
        cmd = struct.unpack('B', result[7:8])
        if cmd[0] == READ_ANALOG_OUTPUT_STATUS_EXCEPTION_RESPONSE:
            print ("Error")
            return -1
        else:
            byte_count = struct.unpack('B', result[8:9])
            fmt ='>'+str(int(byte_count[0]/2))+'H'
            data = struct.unpack(fmt , result[9:9+byte_count[0]])
            return data

# ---MOD.19072515 by Michael(E)---

# TEST
if __name__ == "__main__":
    test=ModbusTcp('127.0.0.1', 502, 1)
    data = test.read_holding_registers(0, 21)
    print (data)