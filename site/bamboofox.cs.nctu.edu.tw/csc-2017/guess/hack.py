#!/usr/bin/env python

from pwn import *

r = remote('bamboofox.cs.nctu.edu.tw', 22005)

p = 1
q = 500000000

while True:
    mid = (p + q) >> 1
    r.recvuntil('=')
    r.sendline(str(mid))
    res = r.recvline()
    if 'small' in res:
        p = mid
    elif 'big' in res:
        q = mid + 1
    else:
        print(res)
        break

r.interactive()
