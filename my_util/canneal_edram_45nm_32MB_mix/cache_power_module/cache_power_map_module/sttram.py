# sttram cache power characteristics
# hp: 10 year retention time
# lp: 1 sec retention time

def sttram_power(tech_node, cache_size, implementation, temperature):
    # L1 and L2 power (these are SRAM caches)
    if tech_node == '45nm':
        if temperature == '75C':
            l1_d_leakage_power = 19.10
            l1_d_read_energy = 0.97
            l1_d_write_energy = 0.99
                    
            l1_i_leakage_power = 19.10
            l1_i_read_energy = 0.97
            l1_i_write_energy = 0.99
                    
            l2_leakage_power = 51.57
            l2_read_energy = 0.56
            l2_write_energy = 0.70
    elif tech_node == '32nm':
        if temperature == '75C':
            l1_d_leakage_power = 32.85
            l1_d_read_energy = 0.68
            l1_d_write_energy = 0.69
            
            l1_i_leakage_power = 32.85
            l1_i_read_energy = 0.68
            l1_i_write_energy = 0.69
                    
            l2_leakage_power = 75.91
            l2_read_energy = 0.32
            l2_write_energy = 0.40
        elif temperature == '95C':
            l1_d_leakage_power = 40.00
            l1_d_read_energy = 0.53
            l1_d_write_energy = 0.53
            
            l1_i_leakage_power = 40.00
            l1_i_read_energy = 0.53
            l1_i_write_energy = 0.53
            
            l2_leakage_power = 99.28
            l2_read_energy = 0.22
            l2_write_energy = 0.27
    elif tech_node == '22nm':
        if temperature == '75C':
            l1_d_leakage_power = 50.99
            l1_d_read_energy = 0.37
            l1_d_write_energy = 0.38
            
            l1_i_leakage_power = 50.99
            l1_i_read_energy = 0.37
            l1_i_write_energy = 0.38
            
            l2_leakage_power = 118.87
            l2_read_energy = 0.18
            l2_write_energy = 0.22

    # L3 power
    if tech_node == '45nm':
        if cache_size == '32MB':
            if implementation == 'lp':
                if temperature == '75C':
                    l3_leakage_power = 30.76
                    l3_read_energy = 1.66
                    l3_write_energy = 29.37
                    l3_tag_energy = 0.04
                    l3_refresh_energy = 0
                    l3_overhead_power = 0
    elif tech_node == '32nm':
        if cache_size == '16MB':
            if implementation == 'lp':
                if temperature == '75C':
                    l3_leakage_power = 30.31
                    l3_read_energy = 0.6
                    l3_write_energy = 19.93
                    l3_tag_energy = 0.02
                    l3_refresh_energy = 0
                    l3_overhead_power = 0
        elif cache_size == '32MB':
            if implementation == 'hp':
                if temperature == '75C':
                    l3_leakage_power = 45.28
                    l3_read_energy = 0.94
                    l3_write_energy = 47.42
                    l3_tag_energy = 0.02
                    l3_refresh_energy = 0
                    l3_overhead_power = 0
            elif implementation == 'lp':
                if temperature == '75C':
                    l3_leakage_power = 45.28
                    l3_read_energy = 0.94
                    l3_write_energy = 20.25
                    l3_tag_energy = 0.02
                    l3_refresh_energy = 0
                    l3_overhead_power = 0
                elif temperature == '95C':
                    l3_leakage_power = 61.98
                    l3_read_energy = 0.96
                    l3_write_energy = 20.26
                    l3_tag_energy = 0.02
                    l3_refresh_energy = 0
                    l3_overhead_power = 0
        elif cache_size == '64MB':
            if implementation == 'hp':
                if temperature == '75C':
                    l3_leakage_power = 76.77
                    l3_read_energy = 1.22
                    l3_write_energy = 47.69
                    l3_tag_energy = 0.04
                    l3_refresh_energy = 0
                    l3_overhead_power = 0
            elif implementation == 'lp':
                if temperature == '75C':
                    l3_leakage_power = 76.77
                    l3_read_energy = 1.22
                    l3_write_energy = 20.52
                    l3_tag_energy = 0.04
                    l3_refresh_energy = 0
                    l3_overhead_power = 0
        elif cache_size == '128MB':
            if implementation == 'hp':
                if temperature == '75C':
                    l3_leakage_power = 115.26
                    l3_read_energy = 1.57
                    l3_write_energy = 48.05
                    l3_tag_energy = 0.05
                    l3_refresh_energy = 0
                    l3_overhead_power = 0
        elif cache_size == '160MB':
            if implementation == 'hp':
                if temperature == '75C':
                    l3_leakage_power = 128.18
                    l3_read_energy = 1.75
                    l3_write_energy = 48.24
                    l3_tag_energy = 0.06
                    l3_refresh_energy = 0
                    l3_overhead_power = 0
        elif cache_size == '192MB':
            if implementation == 'hp':
                if temperature == '75C':
                    l3_leakage_power = 170.61
                    l3_read_energy = 1.94
                    l3_write_energy = 48.44
                    l3_tag_energy = 0.07
                    l3_refresh_energy = 0
                    l3_overhead_power = 0
        elif cache_size == '224MB':
            if implementation == 'hp':
                if temperature == '75C':
                    l3_leakage_power = 183.18
                    l3_read_energy = 2.13
                    l3_write_energy = 48.66
                    l3_tag_energy = 0.08
                    l3_refresh_energy = 0
                    l3_overhead_power = 0
        elif cache_size == '240MB':
            if implementation == 'hp':
                if temperature == '75C':
                    l3_leakage_power = 193.31
                    l3_read_energy = 2.34
                    l3_write_energy = 48.88
                    l3_tag_energy = 0.09
                    l3_refresh_energy = 0
                    l3_overhead_power = 0
    elif tech_node == '22nm':
        if cache_size == '32MB':
            if implementation == 'lp':
                if temperature == '75C':
                    l3_leakage_power = 73.49
                    l3_read_energy = 0.52
                    l3_write_energy = 13.95
                    l3_tag_energy = 0.01
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
