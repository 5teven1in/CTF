#!/usr/bin/env python

import angr

proj = angr.Project('./angrman')
state = proj.factory.entry_state()
sm = proj.factory.simgr(state)
sm.explore(find = 0x400d9e)

print sm.found[0].posix.dumps(0).strip('\0\n')
