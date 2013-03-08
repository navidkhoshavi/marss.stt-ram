#!/usr/bin/python -O

import sys
import re

EPOCH = 1000000

benchmark = sys.argv[1] # e.g., canneal
tech = sys.argv[2] # e.g., sram_32nm_32MB_mix

flog = open(benchmark + '_' + tech + '/' + benchmark + '.log', 'r')
ftrace = open(benchmark + '_' + tech + '/llc_access_trace.log', 'r')
fout = open('workload_char.dat', 'w')

time = re.compile("Stopped after ([0-9]+) cycles, ([0-9]+) instructions(.*)")

for line in flog:
    t = time.match(line)
    if t is not None:
        exe_time = int(t.group(1))

num_access = [0] * (exe_time/EPOCH + 1)

cycle = 0
i = 0
print >>fout, "# Access density (for plotting)"
for line in ftrace:
    cycle = int(line.split()[0])

    while cycle/EPOCH != i:
        i += 1

    num_access[i] += 1

for x in num_access:
    print >>fout, x

flog.close()
ftrace.close()
fout.close()
