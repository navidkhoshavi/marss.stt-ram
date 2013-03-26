# compute cache power

def compute_cache_power(num_cycle,
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
                        proc_freq,
                        num_core,
                        num_bank):
    fout1 = open('l1_d_power.dat', 'w') 
    fout2 = open('l1_i_power.dat', 'w') 
    fout3 = open('l2_power.dat', 'w') 
    fout4 = open('l3_power.dat', 'w') 
    fout5 = open('l1_d_energy.dat', 'w') 
    fout6 = open('l1_i_energy.dat', 'w')
    fout7 = open('l2_energy.dat', 'w') 
    fout8 = open('l3_energy.dat', 'w') 

    time = 0
    if proc_freq == '1GHz': time = num_cycle * 1E-9 # (cycle time = 1ns)
    elif proc_freq == '2GHz': time = num_cycle * 5E-10
    elif proc_freq == '3GHz': time = num_cycle * 3E-10
    elif proc_freq == '4GHz': time = num_cycle * 2.5E-10

    # calculate energy
    l1_d_read_E = (l1_d_num_read*l1_d_read_energy + l1_d_num_update*l1_d_read_energy) * 1E-6 # mJ
    l1_d_write_E = (l1_d_num_write*l1_d_write_energy + l1_d_num_update*l1_d_write_energy) * 1E-6 # mJ
    l1_d_dynamic_E = l1_d_read_E + l1_d_write_E # mJ
    l1_d_leakage_E = time * l1_d_leakage_power * num_core # mJ

    l1_i_read_E = (l1_i_num_read*l1_i_read_energy + l1_i_num_update*l1_i_read_energy) * 1E-6 # mJ
    l1_i_write_E = (l1_i_num_write*l1_i_write_energy + l1_i_num_update*l1_i_write_energy) * 1E-6 # mJ
    l1_i_dynamic_E = l1_i_read_E + l1_i_write_E # mJ
    l1_i_leakage_E = time * l1_i_leakage_power * num_core # mJ

    l2_read_E = (l2_num_read*l2_read_energy + l2_num_update*l2_read_energy) * 1E-6 # mJ
    l2_write_E = (l2_num_write*l2_write_energy + l2_num_update*l2_write_energy) * 1E-6 # mJ
    l2_dynamic_E = l2_read_E + l2_write_E # mJ
    l2_leakage_E = time * l2_leakage_power * num_core # mJ

    l3_read_E = (l3_num_read*l3_read_energy + l3_num_update*l3_tag_energy) * 1E-6 # mJ
    l3_write_E = (l3_num_write*l3_write_energy + l3_num_update*l3_write_energy) * 1E-6 # mJ
    l3_dynamic_E = l3_read_E + l3_write_E # mJ
    l3_leakage_E = time * l3_leakage_power * num_bank # mJ
    l3_refresh_E = num_refresh * l3_refresh_energy * 1E-6 # mJ
    l3_overhead_E = time * l3_overhead_power * 1E-6 # mJ

    total_l1_d_E = l1_d_dynamic_E + l1_d_leakage_E
    total_l1_i_E = l1_i_dynamic_E + l1_i_leakage_E
    total_l2_E = l2_dynamic_E + l2_leakage_E
    total_l3_E = l3_dynamic_E + l3_leakage_E + l3_refresh_E + l3_overhead_E

    # calculate power
    l1_d_dynamic_P = l1_d_dynamic_E / time # mW
    l1_d_leakage_P = l1_d_leakage_E / time # mW

    l1_i_dynamic_P = l1_i_dynamic_E / time # mW
    l1_i_leakage_P = l1_i_leakage_E / time # mW

    l2_dynamic_P = l2_dynamic_E / time # mW
    l2_leakage_P = l2_leakage_E / time # mW

    l3_dynamic_P = l3_dynamic_E / time # mW
    l3_leakage_P = l3_leakage_E / time # mW
    l3_refresh_P = l3_refresh_E / time # mW
    l3_overhead_P = l3_overhead_E / time # mW

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
