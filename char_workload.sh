#!/bin/bash

# $1 = benchmark (e.g., canneal)
# $2 = tech (e.g., sram_32nm_32MB_mix)

./my_util/access_pattern.py $1 $2
./my_util/workload_char.py $1 $2

mv workload_char.dat $1_$2
