#!/usr/bin/python -O

import sys
import re
import os

infile1 = sys.argv[1] # ex. blackscholes.log
infile2 = sys.argv[2] # ex. blackscholes.txt


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
    
    num_access = 0
    num_access_per_kins = 0.0
    num_access_per_kcyc = 0.0

    fin2 = open(infile2, 'r')

    for line in fin2:
        s = start.match(line)
        r = read_hit.match(line)
        w = write_hit.match(line)
        m = miss.match(line)
        
        if s is not None: flag = 1
        if flag == 1:
            if r is not None: num_read_hit = int(r.group(2))
            if w is not None: num_write_hit = int(w.group(2))
            if m is not None:
                num_read_miss = int(m.group(1))
                num_write_miss = int(m.group(2))
                flag = 0
    fin2.close()

    num_read = num_read_hit
    num_write = num_write_hit
    num_update = num_read_miss + num_write_miss
    miss_ratio = float(num_read_miss + num_write_miss) / (num_read + num_write + num_update)
    mpki = 10E3 * float(num_read_miss + num_write_miss) / num_ins
    apkc = 10E3 * float(num_read + num_write + num_update) / num_cycle # num access per k cycle

    return num_read, num_write, num_update, miss_ratio, mpki, apkc


# === main ===
fout = open('perf.dat', 'w')

# system performance
(ipc, 
 num_ins, 
 num_cycle, 
 num_refresh) = system_perf()

# L1_D performance
L1_D = []
L1_D += ["L1_D_0"]
L1_D += ["L1_D_1"]
L1_D += ["L1_D_2"]
L1_D += ["L1_D_3"]
L1_D += ["L1_D_4"]
L1_D += ["L1_D_5"]
L1_D += ["L1_D_6"]
L1_D += ["L1_D_7"]

l1_d_num_read = 0
l1_d_num_write = 0
l1_d_num_update = 0
for l1_d in L1_D:
    (num_read,
     num_write,
     num_update,
     miss_ratio,
     mpki,
     apkc) = cache_perf(l1_d, num_cycle, num_ins)

    l1_d_num_read += num_read
    l1_d_num_write += num_write
    l1_d_num_update += num_update

# L1_I performance
L1_I = []
L1_I += ["L1_I_0"]
L1_I += ["L1_I_1"]
L1_I += ["L1_I_2"]
L1_I += ["L1_I_3"]
L1_I += ["L1_I_4"]
L1_I += ["L1_I_5"]
L1_I += ["L1_I_6"]
L1_I += ["L1_I_7"]

l1_i_num_read = 0
l1_i_num_write = 0
l1_i_num_update = 0
for l1_i in L1_I:
    (num_read,
     num_write,
     num_update,
     miss_ratio,
     mpki,
     apkc) = cache_perf(l1_i, num_cycle, num_ins)

    l1_i_num_read += num_read
    l1_i_num_write += num_write
    l1_i_num_update += num_update

# L2 performance
L2 = []
L2 += ["L2_0"]
L2 += ["L2_1"]
L2 += ["L2_2"]
L2 += ["L2_3"]
L2 += ["L2_4"]
L2 += ["L2_5"]
L2 += ["L2_6"]
L2 += ["L2_7"]

l2_num_read = 0
l2_num_write = 0
l2_num_update = 0
for l2 in L2:
    (num_read,
     num_write,
     num_update,
     miss_ratio,
     mpki,
     apkc) = cache_perf(l2, num_cycle, num_ins)

    l2_num_read += num_read
    l2_num_write += num_write
    l2_num_update += num_update

# L3 performance
(L3_0_num_read,
 L3_0_num_write,
 L3_0_num_update,
 L3_0_miss_ratio,
 L3_0_mpki,
 L3_0_apkc) = cache_perf('L3_0', num_cycle, num_ins)

l3_num_read = L3_0_num_read
l3_num_write = L3_0_num_write
l3_num_update = L3_0_num_update
l3_miss_ratio = L3_0_miss_ratio
l3_mpki = L3_0_mpki
l3_apkc = L3_0_apkc

# print results
print "IPC=%f MISS_RATIO=%f MPKI=%f APKC=%f" %(ipc,
                                               l3_miss_ratio,
                                               l3_mpki,
                                               l3_apkc)

print >>fout, "%f %d %f %f %f %d %d %d %d %d %d %d %d %d %d %d %d %d" %(ipc,
                                                                        num_cycle,
                                                                        l3_miss_ratio,
                                                                        l3_mpki,
                                                                        l3_apkc,
                                                                        l1_d_num_read,
                                                                        l1_d_num_write,
                                                                        l1_d_num_update,
                                                                        l1_i_num_read,
                                                                        l1_i_num_write,
                                                                        l1_i_num_update,
                                                                        l2_num_read,
                                                                        l2_num_write,
                                                                        l2_num_update,
                                                                        l3_num_read,
                                                                        l3_num_write,
                                                                        l3_num_update,
                                                                        num_refresh)

fout.close()
