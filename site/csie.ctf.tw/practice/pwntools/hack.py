#!/usr/bin/env python

from pwn import *
import time

# r = remote("localhost", 10123)
r = remote("csie.ctf.tw", 10124)

x = 1
y = 50000000

r.recvuntil('= ')

while True:
    mid = (x + y) / 2
    r.sendline(str(mid))
    res = r.recvuntil('= ')
    if 'small' in res:
        x = mid + 1
    elif 'big' in res:
        y = mid
    else:
        print res
        break

r.interactive()
