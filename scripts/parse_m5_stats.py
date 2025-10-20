#!/usr/bin/env python3
# scripts/parse_m5_stats.py
import sys
import re
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: parse_m5_stats.py /path/to/stats.txt")
    sys.exit(1)

p = Path(sys.argv[1])
if not p.exists():
    print("File not found:", p)
    sys.exit(1)

data = {}
with p.open() as f:
    for line in f:
        m = re.match(r"^\s*([\w\.\-/]+)\s+(\S+)\s*#?.*$", line)
        if m:
            key, val = m.group(1), m.group(2)
            data[key] = val

# keys we care about (best-effort)
candidates = [
    "sim_seconds", "sim_tick", "system.cpu.cpi", "system.cpu.ipc",
    "system.cpu.numCycles", "system.cpu.numInsts",
    "system.mem_ctrls[0].total_reads", "system.mem_ctrls[0].total_writes",
    "system.l2.overall_miss_rate"
]

print("=== Summary from", p)
for k in candidates:
    if k in data:
        print(f"{k:40s} : {data[k]}")
print("\n--- All matched keys (partial) ---")
for k in sorted(data.keys()):
    if any(s in k for s in ["sim_", "system.cpu", "system.mem", "l2", "cache", "ipc", "cpi"]):
        print(f"{k:45s} : {data[k]}")

