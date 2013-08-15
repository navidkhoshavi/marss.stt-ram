# sram cache power characteristics

def sram_power(tech_node, cache_size, implementation, temperature):
    # L1 and L2 power
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
                    l3_leakage_power = 91.62 * 0.95
                    l3_read_energy = 3.69
                    l3_write_energy = 4.00
                    l3_tag_energy = 0.04
                    l3_refresh_energy = 0
                    l3_overhead_power = 0
    elif tech_node == '32nm':
        if cache_size == '16MB':
            if implementation == 'lp':
                if temperature == '75C':
                    l3_leakage_power = 77.69 * 0.95
                    l3_read_energy = 1.76
                    l3_write_energy = 1.93
                    l3_tag_energy = 0.02
                    l3_refresh_energy = 0
                    l3_overhead_power = 0
        elif cache_size == '32MB':
            if implementation == 'hp':
                if temperature == '75C':
                    l3_leakage_power = 690.963
                    l3_read_energy = 2.31
                    l3_write_energy = 2.42
                    l3_tag_energy = 0.01
                    l3_refresh_energy = 0
                    l3_overhead_power = 0
            elif implementation == 'lp':
                if temperature == '75C':
                    l3_leakage_power = 131.58 * 0.95
                    l3_read_energy = 2.10
                    l3_write_energy = 2.21
                    l3_tag_energy = 0.02
                    l3_refresh_energy = 0
                    l3_overhead_power = 0
                elif temperature == '95C':
                    l3_leakage_power = 182.31 * 0.95
                    l3_read_energy = 2.12
                    l3_write_energy = 2.29
                    l3_tag_energy = 0.02
                    l3_refresh_energy = 0
                    l3_overhead_power = 0
        elif cache_size == '40MB':
            if implementation == 'lp':
                if temperature == '75C':
                    l3_leakage_power = 147.86 * 0.95
                    l3_read_energy = 2.26
                    l3_write_energy = 2.39
                    l3_tag_energy = 0.03
                    l3_refresh_energy = 0
                    l3_overhead_power = 0
        elif cache_size == '48MB':
            if implementation == 'lp':
                if temperature == '75C':
                    l3_leakage_power = 164.04 * 0.95
                    l3_read_energy = 2.43
                    l3_write_energy = 2.59
                    l3_tag_energy = 0.03
                    l3_refresh_energy = 0
                    l3_overhead_power = 0
        elif cache_size == '56MB':
            if implementation == 'lp':
                if temperature == '75C':
                    l3_leakage_power = 180.22 * 0.95
                    l3_read_energy = 2.60
                    l3_write_energy = 2.76
                    l3_tag_energy = 0.03
                    l3_refresh_energy = 0
                    l3_overhead_power = 0
        elif cache_size == '60MB':
            if implementation == 'lp':
                if temperature == '75C':
                    l3_leakage_power = 188.31 * 0.95
                    l3_read_energy = 2.68
                    l3_write_energy = 2.85
                    l3_tag_energy = 0.04
                    l3_refresh_energy = 0
                    l3_overhead_power = 0
        elif cache_size == '64MB':
            if implementation == 'lp':
                if temperature == '75C':
                    l3_leakage_power = 185.95 * 0.95
                    l3_read_energy = 3.32
                    l3_write_energy = 3.67
                    l3_tag_energy = 0.04
                    l3_refresh_energy = 0
                    l3_overhead_power = 0
    elif tech_node == '22nm':
        if cache_size == '32MB':
            if implementation == 'lp':
                if temperature == '75C':
                    l3_leakage_power = 201.95 * 0.95
                    l3_read_energy = 1.15
                    l3_write_energy = 1.25
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
