# get cache power characteristics

from cache_power_map_module.sram import *
from cache_power_map_module.sttram import *
from cache_power_map_module.edram import *

def cache_power_map(mem_type,
                    tech_node,
                    cache_size,
                    implementation,
                    temperature,
                    machine):
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

    if mem_type == 'sram':
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
         l3_overhead_power) = sram_power(tech_node,
                                         cache_size,
                                         implementation,
                                         temperature)
    elif mem_type == 'sttram':
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
         l3_overhead_power) = sttram_power(tech_node,
                                           cache_size,
                                           implementation,
                                           temperature)
    elif mem_type == 'edram':
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
         l3_overhead_power) = edram_power(tech_node,
                                          cache_size,
                                          implementation,
                                          temperature)

    # If there is no L3 cache
    if machine == 'ooo_l2' or machine == 'atom_l2':
        l3_leakage_power = 0 # mW (per bank)
        l3_read_energy = 0 # nJ (per read)
        l3_write_energy = 0 # nJ (per write)
        l3_tag_energy = 0 # nJ (per tag access)
        l3_refresh_energy = 0 # nJ (per refresh)
        l3_overhead_power = 0 # nW (all)

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
