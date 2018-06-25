hw6
===

## break

### concept

- just reverse

![](https://i.imgur.com/PLDKIrW.png)

sub_40066D 中將一些 global variable 做運算，不過並不影響是否成功 Pass 並輸出 flag，所以可以忽略這個 function

off_6010C8 的內容為 "Temporal Reverse Engineering"

將輸入每 2 bytes 切為一組做以下操作

- 前面的 byte xor 1
- 後面的 byte xor (off_6010C8[該 byte 在輸入 string 中的位置 mod len(off_6010C8)] + 1)

結果若與 byte_601080 相同則印出 flag

![](https://i.imgur.com/N414Wu1.png)

- pintool

利用 ```obj-intel64/inscount0.so``` 可以計算程式執行的 instruction count

如此可以暴力猜測每一 byte 若比對成功則該次 instruction count 會較多即可獲得 flag

- angr

找出最後成功並輸出 flag 的 address

![](https://i.imgur.com/p4LsZ7V.png)

使用 angr 做 symbolic execution 並限制輸入必須是可視字元即可得到 flag

### exploit

- just reverse

```python
#!/usr/bin/python3

enc = '4201471551196f2345794008480875117347600c640c6e144206721b6e38681460126d07454463136601681a6656681b692e7808601e680c483b721a73056c076f55601268096f09'
string = 'Temporal Reverse Engineering'

by = [ enc[i: i + 2] for i in range(0, len(enc), 2) ]

for i in range(0, len(by), 2):
    print(chr(int(by[i], 16) ^ 1), end = "")
    print(chr(int(by[i + 1], 16) ^ (ord(string[i % len(string)]) + 1)), end = "")
```

- pintool

```python
#!/usr/bin/env python

import os
import string

def try_one(ans, c):
    os.system('echo \'{}\' | ../../../pin -t obj-intel64/inscount0.so -- ./break > /dev/null 2>&1'.format(ans + c))
    with open('inscount.out') as fd:
        f = fd.read()
    return int(f.split()[1])

ans = ''

for i in xrange(75):
    cnt = 0
    ch = ''
    for c in string.printable:
        tmp = try_one(ans, c)
        if tmp > cnt:
            cnt = tmp
            ch = c
    ans += ch
    print ans
```

- angr

```python
#!/usr/bin/env python

import angr

proj = angr.Project("./break")
state = proj.factory.entry_state()

for _ in xrange(72):
        c = state.posix.files[0].read_from(1)
        state.se.add(c >= ' ')
        state.se.add(c <= '~')
state.posix.files[0].seek(0)

sm = proj.factory.simgr(state)
sm.explore(find = 0x00000000040091F)

print sm.found[0].posix.dumps(0).strip('\0\n')
```

### flag

```CTF{PinADXAnInterfaceforCustomizableDebuggingwithDynamicInstrumentation}```
