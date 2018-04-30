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

