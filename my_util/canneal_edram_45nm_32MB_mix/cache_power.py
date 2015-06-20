#!/usr/bin/python -O

import sys

from cache_power_module.get_perf_dat import *
from cache_power_module.cache_power_map import *
from cache_power_module.compute_cache_power import *

# python cache_power.py edram 45nm 32MB lp 3GHz 75C 1 64 ooo_l3  #my change
# === initialization ===
mem_type = sys.argv[1] # memory type (sram, sttram, edram)
tech_node = sys.argv[2] # technology node (45nm, 32nm, 22nm)
cache_size = sys.argv[3] # cache size
implementation = sys.argv[4] # implementation (hp, lp)
proc_freq = sys.argv[5] # processor frequency (1GHz, 2GHz, 3GHz, 4GHz)
temperature = sys.argv[6] # temperature
num_core = int(sys.argv[7]) # number of cores
num_bank = int(sys.argv[8]) # number of LLC banks
machine = sys.argv[9] # machine type (ooo_l3, ooo_l2, atom_l3, atom_l2)
access_mode = "seq"

def main():
    (num_cycle,
     l1_d_num_read,
     l1_d_num_read_hit,
     l1_d_num_read_miss,
     l1_d_num_write,
     l1_d_num_write_hit,
     l1_d_num_write_miss,
     l1_d_num_update,
     l1_d_num_insert,
     l1_i_num_read,
     l1_i_num_read_hit,
     l1_i_num_read_miss,
     l1_i_num_write,
     l1_i_num_write_hit,
     l1_i_num_write_miss,
     l1_i_num_update,
     l1_i_num_insert,
     l2_num_read,
     l2_num_read_hit,
     l2_num_read_miss,
     l2_num_write,
     l2_num_write_hit,
     l2_num_write_miss,
     l2_num_update,
     l2_num_insert,
     l3_num_read,
     l3_num_read_hit,
     l3_num_read_miss,
     l3_num_write,
     l3_num_write_hit,
     l3_num_write_miss,
     l3_num_update,
     l3_num_insert,
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
     l3_overhead_power) = cache_power_map(mem_type,
                                          tech_node,
                                          cache_size,
                                          implementation,
                                          temperature,
                                          machine)

    compute_cache_power(num_cycle,
                        l1_d_num_read,
                        l1_d_num_read_hit,
                        l1_d_num_read_miss,
                        l1_d_num_write,
                        l1_d_num_write_hit,
                        l1_d_num_write_miss,
                        l1_d_num_update,
                        l1_d_num_insert,
                        l1_i_num_read,
                        l1_i_num_read_hit,
                        l1_i_num_read_miss,
                        l1_i_num_write,
                        l1_i_num_write_hit,
                        l1_i_num_write_miss,
                        l1_i_num_update,
                        l1_i_num_insert,
                        l2_num_read,
                        l2_num_read_hit,
                        l2_num_read_miss,
                        l2_num_write,
                        l2_num_write_hit,
                        l2_num_write_miss,
                        l2_num_update,
                        l2_num_insert,
                        l3_num_read,
                        l3_num_read_hit,
                        l3_num_read_miss,
                        l3_num_write,
                        l3_num_write_hit,
                        l3_num_write_miss,
                        l3_num_update,
                        l3_num_insert,
                        num_refresh,
                        access_mode,
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
                        proc_freq,
                        num_core,
                        num_bank)

if __name__ == '__main__':
    main()
