# get key parameters

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
