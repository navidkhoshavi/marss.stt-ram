#!/usr/bin/python -O

import sys
import re
import os

tech = sys.argv[1] 
# tech = 
# sram_32nm_32MB_mix
# sram_32nm_32MB_mix_3GHz
# sram_32nm_32MB_mix_4GHz
# sram_32nm_16MB_mix
# sram_32nm_64MB_mix
# sram_32nm_32MB_HP
# sram_32nm_32MB_LP
# sram_32nm_32MB_mix_95C
# sram_45nm_32MB_mix
# sram_22nm_32MB_mix
# edram_32nm_16MB_mix
# edram_32nm_32MB_mix
# edram_32nm_32MB_mix_3GHz
# edram_32nm_32MB_mix_4GHz
# edram_32nm_64MB_mix
# edram_32nm_32MB_mix_95C
# edram_45nm_32MB_mix
# edram_22nm_32MB_mix
# sttram_32nm_32MB
# sttram_32nm_32MB_LP
# sttram_32nm_32MB_LP_3GHz
# sttram_32nm_32MB_LP_4GHz
# sttram_32nm_32MB_LP_95C
# sttram_45nm_32MB_LP
# sttram_22nm_32MB_LP
# sttram_32nm_16MB_LP
# sttram_32nm_64MB_LP


# === get key parameters ===
def get_perf_dat():
    num_cycle = 0
    l1_d_num_read = 0
    l1_d_num_write = 0
    l1_d_num_update = 0
    l1_i_num_read = 0
    l1_i_num_write = 0
    l1_i_num_update = 0
    l2_num_read = 0
    l2_num_write = 0
    l2_num_update = 0
    l3_num_read = 0
    l3_num_write = 0
    l3_num_update = 0
    num_refresh = 0

    fin = open('perf.dat', 'r')

    for line in fin: 
        key = line.split()

    fin.close()

    num_cycle = float(key[1])
    l1_d_num_read = float(key[5])
    l1_d_num_write = float(key[6])
    l1_d_num_update = float(key[7])
    l1_i_num_read = float(key[8])
    l1_i_num_write = float(key[9])
    l1_i_num_update = float(key[10])
    l2_num_read = float(key[11])
    l2_num_write = float(key[12])
    l2_num_update = float(key[13])
    l3_num_read = float(key[14])
    l3_num_write = float(key[15])
    l3_num_update = float(key[16])
    num_refresh = float(key[17])

    return (num_cycle,
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


# === cache power characteristics ===
def cache_power_map(tech):
    l1_d_leakage_power = 0 # mW (per bank)
    l1_d_read_energy = 0 # nJ (per read)
    l1_d_write_energy = 0 # nJ (per write)

    l1_i_leakage_power = 0 # mW (per bank)
    l1_i_read_energy = 0 # nJ (per read)
    l1_i_write_energy = 0 # nJ (per write)

    l2_leakage_power = 0 # mW (per bank)
    l2_read_energy = 0 # nJ (per read)
    l2_write_energy = 0 # nJ (per write)

    l3_leakage_power = 0 # mW (per bank)
    l3_read_energy = 0 # nJ (per read)
    l3_write_energy = 0 # nJ (per write)
    l3_tag_energy = 0 # nJ (per tag access)
    l3_refresh_energy = 0 # nJ (per refresh)
    l3_overhead_power = 0 # nW (all)

    if tech == 'sram_32nm_32MB_mix':
        l1_d_leakage_power = 32.85
        l1_d_read_energy = 0.68
        l1_d_write_energy = 0.69

        l1_i_leakage_power = 32.85
        l1_i_read_energy = 0.68
        l1_i_write_energy = 0.69

        l2_leakage_power = 75.91
        l2_read_energy = 0.32
        l2_write_energy = 0.40

        l3_leakage_power = 131.58 * 0.95
        l3_read_energy = 2.10
        l3_write_energy = 2.21
        l3_tag_energy = 0.02
        l3_refresh_energy = 0
        l3_overhead_power = 0

    elif tech == 'sram_32nm_32MB_mix_3GHz':
        l1_d_leakage_power = 32.85
        l1_d_read_energy = 0.68
        l1_d_write_energy = 0.69

        l1_i_leakage_power = 32.85
        l1_i_read_energy = 0.68
        l1_i_write_energy = 0.69

        l2_leakage_power = 75.91
        l2_read_energy = 0.32
        l2_write_energy = 0.40

        l3_leakage_power = 131.58 * 0.95
        l3_read_energy = 2.10
        l3_write_energy = 2.21
        l3_tag_energy = 0.02
        l3_refresh_energy = 0
        l3_overhead_power = 0

    elif tech == 'sram_32nm_32MB_mix_4GHz':
        l1_d_leakage_power = 32.85
        l1_d_read_energy = 0.68
        l1_d_write_energy = 0.69

        l1_i_leakage_power = 32.85
        l1_i_read_energy = 0.68
        l1_i_write_energy = 0.69

        l2_leakage_power = 75.91
        l2_read_energy = 0.32
        l2_write_energy = 0.40

        l3_leakage_power = 131.58 * 0.95
        l3_read_energy = 2.10
        l3_write_energy = 2.21
        l3_tag_energy = 0.02
        l3_refresh_energy = 0
        l3_overhead_power = 0

    elif tech == 'sram_32nm_16MB_mix':
        l1_d_leakage_power = 32.85
        l1_d_read_energy = 0.68
        l1_d_write_energy = 0.69

        l1_i_leakage_power = 32.85
        l1_i_read_energy = 0.68
        l1_i_write_energy = 0.69

        l2_leakage_power = 75.91
        l2_read_energy = 0.32
        l2_write_energy = 0.40

        l3_leakage_power = 77.69 * 0.95
        l3_read_energy = 1.76
        l3_write_energy = 1.93
        l3_tag_energy = 0.02
        l3_refresh_energy = 0
        l3_overhead_power = 0

    elif tech == 'sram_32nm_64MB_mix':
        l1_d_leakage_power = 32.85
        l1_d_read_energy = 0.68
        l1_d_write_energy = 0.69

        l1_i_leakage_power = 32.85
        l1_i_read_energy = 0.68
        l1_i_write_energy = 0.69

        l2_leakage_power = 75.91
        l2_read_energy = 0.32
        l2_write_energy = 0.40

        l3_leakage_power = 185.95 * 0.95
        l3_read_energy = 3.32
        l3_write_energy = 3.67
        l3_tag_energy = 0.04
        l3_refresh_energy = 0
        l3_overhead_power = 0

    elif tech == 'sram_32nm_32MB_HP':
        l1_d_leakage_power = 32.85
        l1_d_read_energy = 0.68
        l1_d_write_energy = 0.69

        l1_i_leakage_power = 32.85
        l1_i_read_energy = 0.68
        l1_i_write_energy = 0.69

        l2_leakage_power = 75.91
        l2_read_energy = 0.32
        l2_write_energy = 0.40

        l3_leakage_power = 690.963
        l3_read_energy = 2.31
        l3_write_energy = 2.42
        l3_tag_energy = 0.01
        l3_refresh_energy = 0
        l3_overhead_power = 0

    elif tech == 'sram_32nm_32MB_LP':
        l1_d_leakage_power = 32.85
        l1_d_read_energy = 0.68
        l1_d_write_energy = 0.69

        l1_i_leakage_power = 32.85
        l1_i_read_energy = 0.68
        l1_i_write_energy = 0.69

        l2_leakage_power = 75.91
        l2_read_energy = 0.32
        l2_write_energy = 0.40

        l3_leakage_power = 3.79
        l3_read_energy = 3.50
        l3_write_energy = 3.65
        l3_tag_energy = 0.02
        l3_refresh_energy = 0
        l3_overhead_power = 0

    elif tech == 'sram_32nm_32MB_mix_95C':
        l1_d_leakage_power = 40.00
        l1_d_read_energy = 0.53
        l1_d_write_energy = 0.53

        l1_i_leakage_power = 40.00
        l1_i_read_energy = 0.53
        l1_i_write_energy = 0.53

        l2_leakage_power = 99.28
        l2_read_energy = 0.22
        l2_write_energy = 0.27

        l3_leakage_power = 182.31 * 0.95
        l3_read_energy = 2.12
        l3_write_energy = 2.29
        l3_tag_energy = 0.02
        l3_refresh_energy = 0
        l3_overhead_power = 0

    elif tech == 'sram_45nm_32MB_mix':
        l1_d_leakage_power = 19.10
        l1_d_read_energy = 0.97
        l1_d_write_energy = 0.99

        l1_i_leakage_power = 19.10
        l1_i_read_energy = 0.97
        l1_i_write_energy = 0.99

        l2_leakage_power = 51.57
        l2_read_energy = 0.56
        l2_write_energy = 0.70

        l3_leakage_power = 91.62 * 0.95
        l3_read_energy = 3.69
        l3_write_energy = 4.00
        l3_tag_energy = 0.04
        l3_refresh_energy = 0
        l3_overhead_power = 0

    elif tech == 'sram_22nm_32MB_mix':
        l1_d_leakage_power = 50.99
        l1_d_read_energy = 0.37
        l1_d_write_energy = 0.38

        l1_i_leakage_power = 50.99
        l1_i_read_energy = 0.37
        l1_i_write_energy = 0.38

        l2_leakage_power = 118.87
        l2_read_energy = 0.18
        l2_write_energy = 0.22

        l3_leakage_power = 201.95 * 0.95
        l3_read_energy = 1.15
        l3_write_energy = 1.25
        l3_tag_energy = 0.01
        l3_refresh_energy = 0
        l3_overhead_power = 0

    elif tech == 'edram_32nm_16MB_mix':
        l1_d_leakage_power = 32.85
        l1_d_read_energy = 0.68
        l1_d_write_energy = 0.69

        l1_i_leakage_power = 32.85
        l1_i_read_energy = 0.68
        l1_i_write_energy = 0.69

        l2_leakage_power = 75.91
        l2_read_energy = 0.32
        l2_write_energy = 0.40

        l3_leakage_power = 31.03
        l3_read_energy = 1.02
        l3_write_energy = 1.03
        l3_tag_energy = 0.01
        l3_refresh_energy = 0.02
        l3_overhead_power = 0

    elif tech == 'edram_32nm_32MB_mix':
        l1_d_leakage_power = 32.85
        l1_d_read_energy = 0.68
        l1_d_write_energy = 0.69

        l1_i_leakage_power = 32.85
        l1_i_read_energy = 0.68
        l1_i_write_energy = 0.69

        l2_leakage_power = 75.91
        l2_read_energy = 0.32
        l2_write_energy = 0.40

        l3_leakage_power = 49.00
        l3_read_energy = 1.74
        l3_write_energy = 1.79
        l3_tag_energy = 0.02
        l3_refresh_energy = 0.03
        l3_overhead_power = 0

    elif tech == 'edram_32nm_32MB_mix_3GHz':
        l1_d_leakage_power = 32.85
        l1_d_read_energy = 0.68
        l1_d_write_energy = 0.69

        l1_i_leakage_power = 32.85
        l1_i_read_energy = 0.68
        l1_i_write_energy = 0.69

        l2_leakage_power = 75.91
        l2_read_energy = 0.32
        l2_write_energy = 0.40

        l3_leakage_power = 49.00
        l3_read_energy = 1.74
        l3_write_energy = 1.79
        l3_tag_energy = 0.02
        l3_refresh_energy = 0.03
        l3_overhead_power = 0

    elif tech == 'edram_32nm_32MB_mix_4GHz':
        l1_d_leakage_power = 32.85
        l1_d_read_energy = 0.68
        l1_d_write_energy = 0.69

        l1_i_leakage_power = 32.85
        l1_i_read_energy = 0.68
        l1_i_write_energy = 0.69

        l2_leakage_power = 75.91
        l2_read_energy = 0.32
        l2_write_energy = 0.40

        l3_leakage_power = 49.00
        l3_read_energy = 1.74
        l3_write_energy = 1.79
        l3_tag_energy = 0.02
        l3_refresh_energy = 0.03
        l3_overhead_power = 0

    elif tech == 'edram_32nm_64MB_mix':
        l1_d_leakage_power = 32.85
        l1_d_read_energy = 0.68
        l1_d_write_energy = 0.69

        l1_i_leakage_power = 32.85
        l1_i_read_energy = 0.68
        l1_i_write_energy = 0.69

        l2_leakage_power = 75.91
        l2_read_energy = 0.32
        l2_write_energy = 0.40

        l3_leakage_power = 88.17
        l3_read_energy = 2.05
        l3_write_energy = 2.12
        l3_tag_energy = 0.02
        l3_refresh_energy = 0.04
        l3_overhead_power = 0

    elif tech == 'edram_32nm_32MB_mix_95C':
        l1_d_leakage_power = 40.00
        l1_d_read_energy = 0.53
        l1_d_write_energy = 0.53

        l1_i_leakage_power = 40.00
        l1_i_read_energy = 0.53
        l1_i_write_energy = 0.53

        l2_leakage_power = 99.28
        l2_read_energy = 0.22
        l2_write_energy = 0.27

        l3_leakage_power = 66.48
        l3_read_energy = 1.74
        l3_write_energy = 1.75
        l3_tag_energy = 0.02
        l3_refresh_energy = 0.03
        l3_overhead_power = 0

    elif tech == 'edram_45nm_32MB_mix':
        l1_d_leakage_power = 19.10
        l1_d_read_energy = 0.97
        l1_d_write_energy = 0.99

        l1_i_leakage_power = 19.10
        l1_i_read_energy = 0.97
        l1_i_write_energy = 0.99

        l2_leakage_power = 51.57
        l2_read_energy = 0.56
        l2_write_energy = 0.70

        l3_leakage_power = 34.96
        l3_read_energy = 2.99
        l3_write_energy = 3.08
        l3_tag_energy = 0.06
        l3_refresh_energy = 0.03
        l3_overhead_power = 0

    elif tech == 'edram_22nm_32MB_mix':
        l1_d_leakage_power = 50.99
        l1_d_read_energy = 0.37
        l1_d_write_energy = 0.38

        l1_i_leakage_power = 50.99
        l1_i_read_energy = 0.37
        l1_i_write_energy = 0.38

        l2_leakage_power = 118.87
        l2_read_energy = 0.18
        l2_write_energy = 0.22

        l3_leakage_power = 71.75
        l3_read_energy = 0.92
        l3_write_energy = 0.96
        l3_tag_energy = 0.02
        l3_refresh_energy = 0.03
        l3_overhead_power = 0

    elif tech == 'sttram_32nm_32MB':
        l1_d_leakage_power = 32.85
        l1_d_read_energy = 0.68
        l1_d_write_energy = 0.69

        l1_i_leakage_power = 32.85
        l1_i_read_energy = 0.68
        l1_i_write_energy = 0.69

        l2_leakage_power = 75.91
        l2_read_energy = 0.32
        l2_write_energy = 0.40

        l3_leakage_power = 45.28
        l3_read_energy = 0.94
        l3_write_energy = 47.42
        l3_tag_energy = 0.02
        l3_refresh_energy = 0
        l3_overhead_power = 0

    elif tech == 'sttram_32nm_32MB_LP':
        l1_d_leakage_power = 32.85
        l1_d_read_energy = 0.68
        l1_d_write_energy = 0.69

        l1_i_leakage_power = 32.85
        l1_i_read_energy = 0.68
        l1_i_write_energy = 0.69

        l2_leakage_power = 75.91
        l2_read_energy = 0.32
        l2_write_energy = 0.40

        l3_leakage_power = 45.28
        l3_read_energy = 0.94
        l3_write_energy = 20.25
        l3_tag_energy = 0.02
        l3_refresh_energy = 0
        l3_overhead_power = 0

    elif tech == 'sttram_32nm_32MB_LP_3GHz':
        l1_d_leakage_power = 32.85
        l1_d_read_energy = 0.68
        l1_d_write_energy = 0.69

        l1_i_leakage_power = 32.85
        l1_i_read_energy = 0.68
        l1_i_write_energy = 0.69

        l2_leakage_power = 75.91
        l2_read_energy = 0.32
        l2_write_energy = 0.40

        l3_leakage_power = 45.28
        l3_read_energy = 0.94
        l3_write_energy = 20.25
        l3_tag_energy = 0.02
        l3_refresh_energy = 0
        l3_overhead_power = 0

    elif tech == 'sttram_32nm_32MB_LP_4GHz':
        l1_d_leakage_power = 32.85
        l1_d_read_energy = 0.68
        l1_d_write_energy = 0.69

        l1_i_leakage_power = 32.85
        l1_i_read_energy = 0.68
        l1_i_write_energy = 0.69

        l2_leakage_power = 75.91
        l2_read_energy = 0.32
        l2_write_energy = 0.40

        l3_leakage_power = 45.28
        l3_read_energy = 0.94
        l3_write_energy = 20.25
        l3_tag_energy = 0.02
        l3_refresh_energy = 0
        l3_overhead_power = 0

    elif tech == 'sttram_32nm_32MB_LP_95C':
        l1_d_leakage_power = 40.00
        l1_d_read_energy = 0.53
        l1_d_write_energy = 0.53

        l1_i_leakage_power = 40.00
        l1_i_read_energy = 0.53
        l1_i_write_energy = 0.53

        l2_leakage_power = 99.28
        l2_read_energy = 0.22
        l2_write_energy = 0.27

        l3_leakage_power = 61.98
        l3_read_energy = 0.96
        l3_write_energy = 20.26
        l3_tag_energy = 0.02
        l3_refresh_energy = 0
        l3_overhead_power = 0

    elif tech == 'sttram_45nm_32MB_LP':
        l1_d_leakage_power = 19.10
        l1_d_read_energy = 0.97
        l1_d_write_energy = 0.99

        l1_i_leakage_power = 19.10
        l1_i_read_energy = 0.97
        l1_i_write_energy = 0.99

        l2_leakage_power = 51.57
        l2_read_energy = 0.56
        l2_write_energy = 0.70

        l3_leakage_power = 30.76
        l3_read_energy = 1.66
        l3_write_energy = 29.37
        l3_tag_energy = 0.04
        l3_refresh_energy = 0
        l3_overhead_power = 0

    elif tech == 'sttram_22nm_32MB_LP':
        l1_d_leakage_power = 50.99
        l1_d_read_energy = 0.37
        l1_d_write_energy = 0.38

        l1_i_leakage_power = 50.99
        l1_i_read_energy = 0.37
        l1_i_write_energy = 0.38

        l2_leakage_power = 118.87
        l2_read_energy = 0.18
        l2_write_energy = 0.22

        l3_leakage_power = 73.49
        l3_read_energy = 0.52
        l3_write_energy = 13.95
        l3_tag_energy = 0.01
        l3_refresh_energy = 0
        l3_overhead_power = 0

    elif tech == 'sttram_32nm_16MB_LP':
        l1_d_leakage_power = 32.85
        l1_d_read_energy = 0.68
        l1_d_write_energy = 0.69

        l1_i_leakage_power = 32.85
        l1_i_read_energy = 0.68
        l1_i_write_energy = 0.69

        l2_leakage_power = 75.91
        l2_read_energy = 0.32
        l2_write_energy = 0.40

        l3_leakage_power = 30.31
        l3_read_energy = 0.6
        l3_write_energy = 19.93
        l3_tag_energy = 0.02
        l3_refresh_energy = 0
        l3_overhead_power = 0

    elif tech == 'sttram_32nm_64MB_LP':
        l1_d_leakage_power = 32.85
        l1_d_read_energy = 0.68
        l1_d_write_energy = 0.69

        l1_i_leakage_power = 32.85
        l1_i_read_energy = 0.68
        l1_i_write_energy = 0.69

        l2_leakage_power = 75.91
        l2_read_energy = 0.32
        l2_write_energy = 0.40

        l3_leakage_power = 76.77
        l3_read_energy = 1.22
        l3_write_energy = 20.52
        l3_tag_energy = 0.04
        l3_refresh_energy = 0
        l3_overhead_power = 0

    return (l1_d_leakage_power,
            l1_d_read_energy,
            l1_d_write_energy,
            l1_i_leakage_power,
            l1_i_read_energy,
            l1_i_write_energy,
            l2_leakage_power,
            l2_read_energy,
            l2_write_energy,
            l3_leakage_power,
            l3_read_energy,
            l3_write_energy,
            l3_tag_energy,
            l3_refresh_energy,
            l3_overhead_power)


# === calculate energy ===
def cache_power(num_cycle,
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
                num_refresh,
                l1_d_leakage_power,
                l1_d_read_energy,
                l1_d_write_energy,
                l1_i_leakage_power,
                l1_i_read_energy,
                l1_i_write_energy,
                l2_leakage_power,
                l2_read_energy,
                l2_write_energy,
                l3_leakage_power,
                l3_read_energy,
                l3_write_energy,
                l3_tag_energy,
                l3_refresh_energy,
                l3_overhead_power,
                tech):
    fout1 = open('l1_d_power.dat', 'w') 
    fout2 = open('l1_i_power.dat', 'w') 
    fout3 = open('l2_power.dat', 'w') 
    fout4 = open('l3_power.dat', 'w') 
    fout5 = open('l1_d_energy.dat', 'w') 
    fout6 = open('l1_i_energy.dat', 'w')
    fout7 = open('l2_energy.dat', 'w') 
    fout8 = open('l3_energy.dat', 'w') 

    if tech == 'edram_32nm_32MB_mix_3GHz':
        time = num_cycle * 3E-10 # (cycle time = 0.3ns)
    elif tech == 'sram_32nm_32MB_mix_3GHz':
        time = num_cycle * 3E-10 # (cycle time = 0.3ns)
    elif tech == 'sttram_32nm_32MB_LP_3GHz':
        time = num_cycle * 3E-10 # (cycle time = 0.3ns)
    elif tech == 'edram_32nm_32MB_mix_4GHz':
        time = num_cycle * 2.5E-10 # (cycle time = 0.25ns)
    elif tech == 'sram_32nm_32MB_mix_4GHz':
        time = num_cycle * 2.5E-10 # (cycle time = 0.25ns)
    elif tech == 'sttram_32nm_32MB_LP_4GHz':
        time = num_cycle * 2.5E-10 # (cycle time = 0.25ns)
    else:
        time = num_cycle * 5E-10 # (cycle time = 0.5ns)

    # calculate energy
    l1_d_read_E = (l1_d_num_read*l1_d_read_energy + l1_d_num_update*l1_d_read_energy) * 1E-9 # J
    l1_d_write_E = (l1_d_num_write*l1_d_write_energy + l1_d_num_update*l1_d_write_energy) * 1E-9 # J
    l1_d_dynamic_E = l1_d_read_E + l1_d_write_E # J
    l1_d_leakage_E = time * l1_d_leakage_power * 8 * 1E-3 # J (8 cores)

    l1_i_read_E = (l1_i_num_read*l1_i_read_energy + l1_i_num_update*l1_i_read_energy) * 1E-9 # J
    l1_i_write_E = (l1_i_num_write*l1_i_write_energy + l1_i_num_update*l1_i_write_energy) * 1E-9 # J
    l1_i_dynamic_E = l1_i_read_E + l1_i_write_E # J
    l1_i_leakage_E = time * l1_i_leakage_power * 8 * 1E-3 # J (8 cores)

    l2_read_E = (l2_num_read*l2_read_energy + l2_num_update*l2_read_energy) * 1E-9 # J
    l2_write_E = (l2_num_write*l2_write_energy + l2_num_update*l2_write_energy) * 1E-9 # J
    l2_dynamic_E = l2_read_E + l2_write_E # J
    l2_leakage_E = time * l2_leakage_power * 8 * 1E-3 # J (8 cores)

    l3_read_E = (l3_num_read*l3_read_energy + l3_num_update*l3_tag_energy) * 1E-9 # J
    l3_write_E = (l3_num_write*l3_write_energy + l3_num_update*l3_write_energy) * 1E-9 # J
    l3_dynamic_E = l3_read_E + l3_write_E # J
    l3_leakage_E = time * l3_leakage_power * 16 * 1E-3 # J (16 banks)
    l3_refresh_E = num_refresh * l3_refresh_energy * 1E-9 # J
    l3_overhead_E = time * l3_overhead_power * 1E-9 # J

    total_l1_d_E = l1_d_dynamic_E + l1_d_leakage_E
    total_l1_i_E = l1_i_dynamic_E + l1_i_leakage_E
    total_l2_E = l2_dynamic_E + l2_leakage_E
    total_l3_E = l3_dynamic_E + l3_leakage_E + l3_refresh_E + l3_overhead_E

    # calculate power
    l1_d_dynamic_P = l1_d_dynamic_E * 1E+3 / time # mW
    l1_d_leakage_P = l1_d_leakage_E * 1E+3 / time # mW

    l1_i_dynamic_P = l1_i_dynamic_E * 1E+3 / time # mW
    l1_i_leakage_P = l1_i_leakage_E * 1E+3 / time # mW

    l2_dynamic_P = l2_dynamic_E * 1E+3 / time # mW
    l2_leakage_P = l2_leakage_E * 1E+3 / time # mW

    l3_dynamic_P = l3_dynamic_E * 1E+3 / time # mW
    l3_leakage_P = l3_leakage_E * 1E+3 / time # mW
    l3_refresh_P = l3_refresh_E * 1E+3 / time # mW
    l3_overhead_P = l3_overhead_E * 1E+3 / time # mW

    total_l1_d_P = l1_d_dynamic_P + l1_d_leakage_P
    total_l1_i_P = l1_i_dynamic_P + l1_i_leakage_P
    total_l2_P = l2_dynamic_P + l2_leakage_P
    total_l3_P = l3_dynamic_P + l3_leakage_P + l3_refresh_P + l3_overhead_P
    
    print >>fout1, "%f %f %f" %(total_l1_d_P, l1_d_dynamic_P, l1_d_leakage_P)
    print >>fout2, "%f %f %f" %(total_l1_i_P, l1_i_dynamic_P, l1_i_leakage_P)
    print >>fout3, "%f %f %f" %(total_l2_P, l2_dynamic_P, l2_leakage_P)
    print >>fout4, "%f %f %f %f %f" %(total_l3_P, l3_dynamic_P, l3_leakage_P, l3_refresh_P, l3_overhead_P)
    print >>fout5, "%f %f %f" %(total_l1_d_E, l1_d_dynamic_E, l1_d_leakage_E)
    print >>fout6, "%f %f %f" %(total_l1_i_E, l1_i_dynamic_E, l1_i_leakage_E)
    print >>fout7, "%f %f %f" %(total_l2_E, l2_dynamic_E, l2_leakage_E)
    print >>fout8, "%f %f %f %f %f" %(total_l3_E, l3_dynamic_E, l3_leakage_E, l3_refresh_E, l3_overhead_E)

    fout1.close()
    fout2.close()
    fout3.close()
    fout4.close()
    fout5.close()
    fout6.close()
    fout7.close()
    fout8.close()


# === main ===
(num_cycle,
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
 num_refresh) = get_perf_dat()

(l1_d_leakage_power,
 l1_d_read_energy,
 l1_d_write_energy,
 l1_i_leakage_power,
 l1_i_read_energy,
 l1_i_write_energy,
 l2_leakage_power,
 l2_read_energy,
 l2_write_energy,
 l3_leakage_power,
 l3_read_energy,
 l3_write_energy,
 l3_tag_energy,
 l3_refresh_energy,
 l3_overhead_power) = cache_power_map(tech)

cache_power(num_cycle,
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
            num_refresh,
            l1_d_leakage_power,
            l1_d_read_energy,
            l1_d_write_energy,
            l1_i_leakage_power,
            l1_i_read_energy,
            l1_i_write_energy,
            l2_leakage_power,
            l2_read_energy,
            l2_write_energy,
            l3_leakage_power,
            l3_read_energy,
            l3_write_energy,
            l3_tag_energy,
            l3_refresh_energy,
            l3_overhead_power,
            tech)
