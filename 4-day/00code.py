import struct
# 长度概念
# 8 Bit  相当于 二进制长度 00000000 11111111
# 1 Byte 相当于 字节长度   00       ff
# 常用两大长度对照
# 32 Bit   4 Bytes 0x00000000         0 (Def)
# 64 Bit   8 Bytes 0x0000000000000000 0
# pack单位
# 常用类型  长度  单位
# b 8  Bit
# h 16 Bit
# i 32 Bit
# Q 64 Bit
BYTES =  b"\x04\x00\x00\x00"
DWORD = struct.unpack("i",BYTES)[0]
print("i  = ",DWORD)
DWORD = struct.unpack("<i",BYTES)[0]
print("<i = ",DWORD)
DWORD = struct.unpack(">i",BYTES)[0]
print(">i = ",DWORD)

DWORD = 1024
BYTES = struct.pack("i",DWORD)
print("i  = ",BYTES)
BYTES = struct.pack("<i",DWORD)
print("<i = ",BYTES)
BYTES = struct.pack(">i",DWORD)
print(">i = ",BYTES)



FileText = b"\xffSMB\x00\x00\x00"
FileObject = open("shell.txt","wb+") # 关键第二个参数的b
FileObject.write(b"SMB HEAD") # 8 Byte
FileObject.write(struct.pack("Q",len(FileText))) # 8 Byte
FileObject.write(FileText)












