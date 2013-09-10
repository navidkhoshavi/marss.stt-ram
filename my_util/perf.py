#!/usr/bin/python -O

import sys
import re
import os

infile1 = sys.argv[1] # ex. blackscholes.log
infile2 = sys.argv[2] # ex. blackscholes.txt
num_core = sys.argv[3] # ex. 8
machine = sys.argv[4] # ex. ooo_l3

def system_perf():
    cycle = re.compile("Stopped after ([0-9]+) cycles, ([0-9]+) instructions(.*)")
    refresh = re.compile("Total number of refreshes = ([0-9]+)")

    ipc = 0.0
    num_ins = 0
    num_cycle = 0
    num_refresh = 0

    fin1 = open(infile1, 'r')

    for line in fin1:
        c = cycle.match(line)
        r = refresh.match(line)

        if c is not None: 
            num_cycle = int(c.group(1))
            num_ins = int(c.group(2))
        if r is not None: 
            num_refresh = int(r.group(1))

    fin1.close()

    ipc = float(num_ins) / num_cycle

    return ipc, num_ins, num_cycle, num_refresh


def cache_perf(cache_object, num_cycle, num_ins):
    start = re.compile("  %s:" %cache_object)
    read_hit = re.compile("          read: {forward: ([0-9]+), hit: ([0-9]+)}")
    write_hit = re.compile("          write: {forward: ([0-9]+), hit: ([0-9]+)}")
    miss = re.compile("        miss: {read: ([0-9]+), write: ([0-9]+)}")
    update = re.compile("      update: ([0-9]+)")

    flag = 0

    num_read = 0
    num_read_hit = 0
    num_read_miss = 0
    read_miss_ratio = 0.0

    num_write = 0
    num_write_hit = 0
    num_write_miss = 0
    write_miss_ratio = 0.0
    
    miss_ratio = 0.0

    num_update = 0 # number of updates from upper caches
    
    num_access = 0
    num_access_per_kins = 0.0
    num_access_per_kcyc = 0.0

    fin2 = open(infile2, 'r')

    for line in fin2:
        s = start.match(line)
        r = read_hit.match(line)
        w = write_hit.match(line)
        m = miss.match(line)
        u = update.match(line)

        if s is not None: flag = 1
        if flag == 1:
            if r is not None: num_read_hit = int(r.group(2))
            if w is not None: num_write_hit = int(w.group(2))
            if m is not None:
                num_read_miss = int(m.group(1))
                num_write_miss = int(m.group(2))
            if u is not None: 
                num_update = int(u.group(1))
                flag = 0

    fin2.close()

    num_read = num_read_hit + num_read_miss
    num_write = num_write_hit + num_write_miss
    num_insert = num_read_miss + num_write_miss
    miss_ratio = float(num_read_miss + num_write_miss) / (num_read + num_write)
    mpki = 1E3 * float(num_read_miss + num_write_miss) / num_ins

    return num_read, num_read_hit, num_read_miss, num_write, num_write_hit, num_write_miss, num_update, num_insert, miss_ratio, mpki


# === main ===
fout = open('perf.dat', 'w')

# system performance
(ipc, 
 num_ins, 
 num_cycle, 
 num_refresh) = system_perf()

# L1_D performance
L1_D = []
for i in range(int(num_core)):
    L1_D += ['L1_D_%d' %i]

l1_d_num_read = 0
l1_d_num_read_hit = 0
l1_d_num_read_miss = 0
l1_d_num_write = 0
l1_d_num_write_hit = 0
l1_d_num_write_miss = 0
l1_d_num_update = 0
l1_d_num_insert = 0

for l1_d in L1_D:
    (num_read,
     num_read_hit,
     num_read_miss,
     num_write,
     num_write_hit,
     num_write_miss,
     num_update,
     num_insert,
     miss_ratio,
     mpki) = cache_perf(l1_d, num_cycle, num_ins)

    l1_d_num_read += num_read
    l1_d_num_read_hit += num_read_hit
    l1_d_num_read_miss += num_read_miss
    l1_d_num_write += num_write
    l1_d_num_write_hit += num_write_hit
    l1_d_num_write_miss += num_write_miss
    l1_d_num_update += num_update
    l1_d_num_insert += num_insert

# L1_I performance
L1_I = []
for i in range(int(num_core)):
    L1_I += ['L1_I_%d' %i]

l1_i_num_read = 0
l1_i_num_read_hit = 0
l1_i_num_read_miss = 0
l1_i_num_write = 0
l1_i_num_write_hit = 0
l1_i_num_write_miss = 0
l1_i_num_update = 0
l1_i_num_insert = 0

for l1_i in L1_I:
    (num_read,
     num_read_hit,
     num_read_miss,
     num_write,
     num_write_hit,
     num_write_miss,
     num_update,
     num_insert,
     miss_ratio,
     mpki) = cache_perf(l1_i, num_cycle, num_ins)

    l1_i_num_read += num_read
    l1_i_num_read_hit += num_read_hit
    l1_i_num_read_miss += num_read_miss
    l1_i_num_write += num_write
    l1_i_num_write_hit += num_write_hit
    l1_i_num_write_miss += num_write_miss
    l1_i_num_update += num_update
    l1_i_num_insert += num_insert

# L2 performance
L2 = []
for i in range(int(num_core)):
    L2 += ['L2_%d' %i]

l2_num_read = 0
l2_num_read_hit = 0
l2_num_read_miss = 0
l2_num_write = 0
l2_num_write_hit = 0
l2_num_write_miss = 0
l2_num_update = 0
l2_num_insert = 0

for l2 in L2:
    (num_read,
     num_read_hit,
     num_read_miss,
     num_write,
     num_write_hit,
     num_write_miss,
     num_update,
     num_insert,
     miss_ratio,
     mpki) = cache_perf(l2, num_cycle, num_ins)

    l2_num_read += num_read
    l2_num_read_hit += num_read_hit
    l2_num_read_miss += num_read_miss
    l2_num_write += num_write
    l2_num_write_hit += num_write_hit
    l2_num_write_miss += num_write_miss
    l2_num_update += num_update
    l2_num_insert += num_insert

# L3 performance
l3_num_read = 0
l3_num_read_hit = 0
l3_num_read_miss = 0
l3_num_write = 0
l3_num_write_hit = 0
l3_num_write_miss = 0
l3_num_update = 0

if machine == 'ooo_l3' or machine == 'atom_l3':
    (num_read,
     num_read_hit,
     num_read_miss,
     num_write,
     num_write_hit,
     num_write_miss,
     num_update,
     num_insert,
     miss_ratio,
     mpki) = cache_perf('L3_0', num_cycle, num_ins)

    l3_num_read = num_read
    l3_num_read_hit = num_read_hit
    l3_num_read_miss = num_read_miss
    l3_num_write = num_write
    l3_num_write_hit = num_write_hit
    l3_num_write_miss = num_write_miss
    l3_num_update = num_update
    l3_num_insert = num_insert
    l3_miss_ratio = miss_ratio
    l3_mpki = mpki

else:
    l3_num_read = 0
    l3_num_read_hit = 0
    l3_num_read_miss = 0
    l3_num_write = 0
    l3_num_write_hit = 0
    l3_num_write_miss = 0
    l3_num_update = 0
    l3_num_insert = 0
    l3_miss_ratio = 0
    l3_mpki = 0

# print results
print "IPC=%f MISS_RATIO=%f MPKI=%f" %(ipc, l3_miss_ratio, l3_mpki)

print >>fout, "%f %d %f %f " %(ipc, num_cycle, l3_miss_ratio, l3_mpki),
print >>fout, "%d %d %d %d %d %d %d %d " %(l1_d_num_read,
                                           l1_d_num_read_hit,
                                           l1_d_num_read_miss,
                                           l1_d_num_write,
                                           l1_d_num_write_hit,
                                           l1_d_num_write_miss,
                                           l1_d_num_update,
                                           l1_d_num_insert),
print >>fout, "%d %d %d %d %d %d %d %d " %(l1_i_num_read,
                                           l1_i_num_read_hit,
                                           l1_i_num_read_miss,
                                           l1_i_num_write,
                                           l1_i_num_write_hit,
                                           l1_i_num_write_miss,
                                           l1_i_num_update,
                                           l1_i_num_insert),
print >>fout, "%d %d %d %d %d %d %d %d " %(l2_num_read,
                                           l2_num_read_hit,
                                           l2_num_read_miss,
                                           l2_num_write,
                                           l2_num_write_hit,
                                           l2_num_write_miss,
                                           l2_num_update,
                                           l2_num_insert),
print >>fout, "%d %d %d %d %d %d %d %d %d " %(l3_num_read,
                                           l3_num_read_hit,
                                           l3_num_read_miss,
                                           l3_num_write,
                                           l3_num_write_hit,
                                           l3_num_write_miss,
                                           l3_num_update,
                                           l3_num_insert,
                                           num_refresh),

fout.close()
