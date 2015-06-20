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
    l1_d_num_insert = 0
    l1_i_num_read = 0
    l1_i_num_read_hit = 0
    l1_i_num_read_miss = 0
    l1_i_num_write = 0
    l1_i_num_write_hit = 0
    l1_i_num_write_miss = 0
    l1_i_num_update = 0
    l1_i_num_insert = 0
    l2_num_read = 0
    l2_num_read_hit = 0
    l2_num_read_miss = 0
    l2_num_write = 0
    l2_num_write_hit = 0
    l2_num_write_miss = 0
    l2_num_update = 0
    l2_num_insert = 0
    l3_num_read = 0
    l3_num_read_hit = 0
    l3_num_read_miss = 0
    l3_num_write = 0
    l3_num_write_hit = 0
    l3_num_write_miss = 0
    l3_num_update = 0
    l3_num_insert = 0
    num_refresh = 0

    fin = open('perf.dat', 'r')

    for line in fin: 
        key = line.split()

    fin.close()

    num_cycle = float(key[1])
    l1_d_num_read = float(key[4])
    l1_d_num_read_hit = float(key[5])
    l1_d_num_read_miss = float(key[6])
    l1_d_num_write = float(key[7])
    l1_d_num_write_hit = float(key[8])
    l1_d_num_write_miss = float(key[9])
    l1_d_num_update = float(key[10])
    l1_d_num_insert = float(key[11])
    l1_i_num_read = float(key[12])
    l1_i_num_read_hit = float(key[13])
    l1_i_num_read_miss = float(key[14])
    l1_i_num_write = float(key[15])
    l1_i_num_write_hit = float(key[16])
    l1_i_num_write_miss = float(key[17])
    l1_i_num_update = float(key[18])
    l1_i_num_insert = float(key[19])
    l2_num_read = float(key[20])
    l2_num_read_hit = float(key[21])
    l2_num_read_miss = float(key[22])
    l2_num_write = float(key[23])
    l2_num_write_hit = float(key[24])
    l2_num_write_miss = float(key[25])
    l2_num_update = float(key[26])
    l2_num_insert = float(key[27])
    l3_num_read = float(key[28])
    l3_num_read_hit = float(key[29])
    l3_num_read_miss = float(key[30])
    l3_num_write = float(key[31])
    l3_num_write_hit = float(key[32])
    l3_num_write_miss = float(key[33])
    l3_num_update = float(key[34])
    l3_num_insert = float(key[35])
    num_refresh = float(key[36])

    return (num_cycle,
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
            num_refresh)
