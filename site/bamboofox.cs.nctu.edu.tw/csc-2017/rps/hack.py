#!/usr/bin/env python

from pwn import *
import time

r = remote('bamboofox.cs.nctu.edu.tw', 22004)

rps = ['paper', 'scissors', 'rock']

r.recvuntil('game')
seed = r.recvline()[:-1]
print(seed)

if seed == ':':
    seed = 2
elif seed == '?':
    seed = 1
else:
    seed = 0

for i in range(100):
    sleep(0.1)
    r.recvuntil('): ')
    r.sendline(rps[seed])
    seed = (seed + 1) % 3
r.interactive()
