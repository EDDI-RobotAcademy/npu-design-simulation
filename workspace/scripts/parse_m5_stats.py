#!/usr/bin/env python3
import sys, re
if len(sys.argv)<1:
    print("Usage: parse_m5_stats.py /path/to/stats.txt")
    sys.exit(1)
p=sys.argv[1]
d={}
with open(p) as f:
    for L in f:
        m=re.match(r"^\s*([\w\.\-\[\]]+)\s+([0-9Ee\+\-\.]+)", L)
        if m: d[m.group(1)]=m.group(2)
print("Summary:")
for k in ["sim_seconds","system.cpu.ipc","system.cpu.cpi","system.cpu.numCycles","system.cpu.numInsts"]:
    if k in d: print(f"{k:25s}: {d[k]}")
print("\n(You can inspect the rest of the stats file in detail.)")

