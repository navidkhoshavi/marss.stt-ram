# get key parameters

def get_perf_dat():
    num_cycle = 0
    l1_d_num_read = 0
    l1_d_num_read_hit = 0
    l1_d_num_read_miss = 0
    l1_d_num_write = 0
    l1_d_num_write_hit = 0
    l1_d_num_write_miss = 0
    l1_d_num_update = 0
    l1_i_num_read = 0
    l1_i_num_read_hit = 0
    l1_i_num_read_miss = 0
    l1_i_num_write = 0
    l1_i_num_write_hit = 0
    l1_i_num_write_miss = 0
    l1_i_num_update = 0
    l2_num_read = 0
    l2_num_read_hit = 0
    l2_num_read_miss = 0
    l2_num_write = 0
    l2_num_write_hit = 0
    l2_num_write_miss = 0
    l2_num_update = 0
    l3_num_read = 0
    l3_num_read_hit = 0
    l3_num_read_miss = 0
    l3_num_write = 0
    l3_num_write_hit = 0
    l3_num_write_miss = 0
    l3_num_update = 0
    num_refresh = 0

    fin = open('perf.dat', 'r')

    for line in fin: 
        key = line.split()

    fin.close()

    num_cycle = float(key[1])
    l1_d_num_read = float(key[5])
    l1_d_num_read_hit = float(key[6])
    l1_d_num_read_miss = float(key[7])
    l1_d_num_write = float(key[8])
    l1_d_num_write_hit = float(key[9])
    l1_d_num_write_miss = float(key[10])
    l1_d_num_update = float(key[11])
    l1_i_num_read = float(key[12])
    l1_i_num_read_hit = float(key[13])
    l1_i_num_read_miss = float(key[14])
    l1_i_num_write = float(key[15])
    l1_i_num_write_hit = float(key[16])
    l1_i_num_write_miss = float(key[17])
    l1_i_num_update = float(key[18])
    l2_num_read = float(key[19])
    l2_num_read_hit = float(key[20])
    l2_num_read_miss = float(key[21])
    l2_num_write = float(key[22])
    l2_num_write_hit = float(key[23])
    l2_num_write_miss = float(key[24])
    l2_num_update = float(key[25])
    l3_num_read = float(key[26])
    l3_num_read_hit = float(key[27])
    l3_num_read_miss = float(key[28])
    l3_num_write = float(key[29])
    l3_num_write_hit = float(key[30])
    l3_num_write_miss = float(key[31])
    l3_num_update = float(key[32])
    num_refresh = float(key[33])

    return (num_cycle,
            l1_d_num_read,
            l1_d_num_read_hit,
            l1_d_num_read_miss,
            l1_d_num_write,
            l1_d_num_write_hit,
            l1_d_num_write_miss,
            l1_d_num_update,
            l1_i_num_read,
            l1_i_num_read_hit,
            l1_i_num_read_miss,
            l1_i_num_write,
            l1_i_num_write_hit,
            l1_i_num_write_miss,
            l1_i_num_update,
            l2_num_read,
            l2_num_read_hit,
            l2_num_read_miss,
            l2_num_write,
            l2_num_write_hit,
            l2_num_write_miss,
            l2_num_update,
            l3_num_read,
            l3_num_read_hit,
            l3_num_read_miss,
            l3_num_write,
            l3_num_write_hit,
            l3_num_write_miss,
            l3_num_update,
            num_refresh)
