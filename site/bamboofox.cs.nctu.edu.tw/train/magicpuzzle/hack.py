#!/usr/bin/env python

from pwn import *
import angr
import base64

r = remote('bamboofox.cs.nctu.edu.tw', 11015)

def exp():
    prog = r.recvuntil('0th')
    prog = base64.b64decode(prog[:-3].strip())
    with open('tmp', 'wb') as fd:
        fd.write(prog)
    proj = angr.Project('./tmp')
    state = proj.factory.entry_state()
    sm = proj.factory.simgr(state)
    sm.explore(find = 0x400a0c)
    r.send(sm.found[0].posix.dumps(0))

r.recvuntil('base64')
exp()
r.recvuntil('GJ!')
exp()

r.interactive()
