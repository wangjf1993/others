import binascii
import struct

s = b'hello'
h = binascii.b2a_hex(s)
print(h)
print(binascii.a2b_hex(h))

data = b'\x00\x124V\x00x\x90\xab\x00\xcd\xef\x01\x00#\x004'
x1 = int.from_bytes(data, 'little')
x2 = int.from_bytes(data, 'big')
print(len(data), x1, x2)
print(x1.to_bytes(16, 'little'), x2.to_bytes(16, 'big'))


ss = struct.pack('<idd', 1, 3, 4)
print(ss)
print(struct.unpack('<idd', ss))

x = 10
a = lambda y:x +y
print(a(10))