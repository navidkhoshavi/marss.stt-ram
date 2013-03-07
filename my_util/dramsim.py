#!/usr/bin/python -O

import sys
import re

EPOCH_COUNT = 100000
CYCLE_TIME = float(1) / 667000000

#workload = sys.argv[1]
#fout_name = sys.argv[2]

start_pattern = re.compile("(.*) Printing Statistics (.*)")
end_pattern = re.compile(" == Pending Transactions : ([0-9]+) \(([0-9]+)\)==")
average_power_pattern = re.compile("   Average Power \(watts\)     : ([0-9\.]+)")
background_pattern = re.compile("     -Background \(watts\)     : ([0-9\.]+)")
actpre_pattern = re.compile("     -Act/Pre    \(watts\)     : ([0-9\.]+)")
burst_pattern = re.compile("     -Burst      \(watts\)     : ([0-9\.]+)")
refresh_pattern = re.compile("     -Refresh    \(watts\)     : ([0-9\.]+)")

flag = 0
cycle = 0
average_power = 0
background = 0
actpre = 0
burst = 0
refresh = 0

fin = open('dramsim.log', 'r')
fout = open('dramsim.dat', 'w')
    
for line in fin:
    start = start_pattern.match(line)
    end = end_pattern.match(line)
    ap = average_power_pattern.match(line)
    bg = background_pattern.match(line)
    a = actpre_pattern.match(line)
    b = burst_pattern.match(line)
    r = refresh_pattern.match(line)

    if start is not None: flag = 1
    elif end is not None:
        cycle = end.group(2)
        # energy in mJ
        average_energy = average_power * EPOCH_COUNT * CYCLE_TIME * 1000
        background_energy = background * EPOCH_COUNT * CYCLE_TIME * 1000
        actpre_energy = actpre * EPOCH_COUNT * CYCLE_TIME * 1000
        burst_energy = burst * EPOCH_COUNT * CYCLE_TIME * 1000
        refresh_energy = refresh * EPOCH_COUNT * CYCLE_TIME * 1000

        print >>fout, "%s\t%s\t%s\t%s\t%s\t%s\t%f\t%f\t%f\t%f\t%f" %(cycle, average_power, background, actpre, burst, refresh, average_energy, background_energy, actpre_energy, burst_energy, refresh_energy)

        flag = 0

    if flag == 1:
        if ap is not None: average_power += float(ap.group(1))
        elif bg is not None: background += float(bg.group(1))
        elif a is not None: actpre += float(a.group(1))
        elif b is not None: burst += float(b.group(1))
        elif r is not None: refresh += float(r.group(1))
    else:
        average_power = 0
        background = 0
        actpre = 0
        burst = 0
        refresh = 0

fin.close()
fout.close()
