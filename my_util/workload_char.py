#!/usr/bin/python -O

import sys
import re

benchmark = sys.argv[1] # e.g. canneal

# get number of lines (depends on cache size)
tech = sys.argv[2] # e.g. sram_32nm_32MB)mix

NUM_LINES = 0

if tech == 'sram_32nm_32MB_mix': NUM_LINES = 524288
elif tech == 'sram_32nm_32MB_mix_3GHz': NUM_LINES = 524288
elif tech == 'sram_32nm_32MB_mix_4GHz': NUM_LINES = 524288
elif tech == 'sram_32nm_16MB_mix': NUM_LINES = 262144
elif tech == 'sram_32nm_64MB_mix': NUM_LINES = 1048576
elif tech == 'sram_32nm_32MB_HP': NUM_LINES = 524288
elif tech == 'sram_32nm_32MB_LP': NUM_LINES = 524288
elif tech == 'sram_32nm_32MB_mix_95C': NUM_LINES = 524288
elif tech == 'sram_45nm_32MB_mix': NUM_LINES = 524288
elif tech == 'sram_22nm_32MB_mix': NUM_LINES = 524288
elif tech == 'edram_32nm_16MB_mix': NUM_LINES = 262144
elif tech == 'edram_32nm_32MB_mix': NUM_LINES = 524288
elif tech == 'edram_32nm_32MB_mix_3GHz': NUM_LINES = 524288
elif tech == 'edram_32nm_32MB_mix_4GHz': NUM_LINES = 524288
elif tech == 'edram_32nm_64MB_mix': NUM_LINES = 1048576
elif tech == 'edram_32nm_32MB_mix_95C': NUM_LINES = 524288
elif tech == 'edram_45nm_32MB_mix': NUM_LINES = 524288
elif tech == 'edram_22nm_32MB_mix': NUM_LINES = 524288
elif tech == 'sttram_32nm_32MB': NUM_LINES = 524288
elif tech == 'sttram_32nm_32MB_LP': NUM_LINES = 524288
elif tech == 'sttram_32nm_32MB_LP_3GHz': NUM_LINES = 524288
elif tech == 'sttram_32nm_32MB_LP_4GHz': NUM_LINES = 524288
elif tech == 'sttram_32nm_32MB_LP_95C': NUM_LINES = 524288
elif tech == 'sttram_45nm_32MB_LP': NUM_LINES = 524288
elif tech == 'sttram_22nm_32MB_LP': NUM_LINES = 524288
elif tech == 'sttram_32nm_16MB_LP': NUM_LINES = 262144
elif tech == 'sttram_32nm_64MB_LP': NUM_LINES = 1048576


flog = open(benchmark + '_' + tech + '/' + benchmark + '.log', 'r')
ftrace = open(benchmark + '_' + tech + '/llc_access_trace.log', 'r')

# === get total cycle ===
time = re.compile("Stopped after ([0-9]+) cycles, ([0-9]+) instructions(.*)")
exe_time = 0

for line in flog:
    t = time.match(line)
    if t is not None:
        exe_time = int(t.group(1))


# TODO (uncomment this code block after line_stats is coded in marss)
# calculate avg dead time and avg access interval for the entire cache
# this is only an estimation
# fin = open(benchmark + '_' + tech + '/line_stats.log', 'r')

# dead_start = re.compile("# === avg dead time ===")
# access_start = re.compile("# === avg access interval ===")

# flag = 0
# totalDeadTime = 0
# avgDeadTime = 0
# totalAccessInterval = 0
# avgAccessInterval = 0

# for line in fin:
#     dead = dead_start.match(line)
#     access = access_start.match(line)

#     if dead is not None: 
#         flag = 1
#         continue
#     if access is not None: 
#         flag = 2
#         continue

#     if flag == 1:
#         s = line.strip().split(" ")
#         for l in range(0, len(s)):
#             totalDeadTime += int(s[l])
#     elif flag == 2:
#         s = line.strip().split(" ")
#         for l in range(0, len(s)):
#             if int(s[l]) == 0: totalAccessInterval += exe_time
#             else: totalAccessInterval += int(s[l])

# avgDeadTime = float(totalDeadTime) / NUM_LINES
# avgAccessInterval = float(totalAccessInterval) / NUM_LINES

fout = open('workload_char.dat', 'a')

# print >>fout, "# Avg dead time = %f cycles" %avgDeadTime
# print >>fout, "# Avg access interval = %f cycles" %avgAccessInterval

# fin.close()


# lazy coding... should've make defs instead of appending code
# this part of the code is for getting working set size

# === load trafe file ===
trace = []
i = 0

for line in ftrace:
    trace += [0]
    trace[i] = int(line.split()[1])
    i += 1

trace.sort()

# === ref distance ===
def ref_distance(trace):
    addr = 0
    num_unique_line = 0
    flag = 0
    i = 0

    for t in trace:
        if t != addr:
            num_unique_line += 1
                
        addr = t
        i += 1

    print >>fout, "# Working set size: %f MB" %(float(num_unique_line)*64/1000000)

ref_distance(trace)

fout.close()
