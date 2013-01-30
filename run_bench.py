#!/usr/bin/env python

#
# This script is used to run checkpointed images of MARSSx86 Simulator.
# To use this script, make sure that following variables are set correctly:
#   - qemu_bin : Path to the binary 'qemu-system-x86_64' compiled for MARSS
#   - qemu_img : A list of qemu images that contains checkpoints to run.  These
#                images must be identical.  Based on number of images listed,
#                the script will invoke threads to run benchmarks in parallel
#   - vnc_counter : Every simulation run its QEMU window in VNC so it can be
#                   accessed later.  By defalt it starts with 10, but change if
#                   other applications are using those vnc servers
#
# Author  : Avadh Patel 
# Contact : apatel at cs.binghamton.edu
#


import os
import subprocess
import sys

from optparse import OptionParser

from threading import Thread, Lock

# First check if user has provided directory to save all results files
opt_parser = OptionParser("Usage: %prog [-d output_dir_name]")
opt_parser.add_option("-d", "--output-dir", dest="output_dir",
        type="string", help="Name of the output directory to save all results")

(options, args) = opt_parser.parse_args()

if options.output_dir == None:
    options.output_dir = "."
else:
    print("Results files will be stored in %s directory" % options.output_dir)
    if not os.path.exists(options.output_dir):
        os.makedirs(options.output_dir)

output_dir = options.output_dir + "/"

# Set up default variables
# It assumes its in '$MARSS' directory
cwd = os.getcwd()
qemu_bin = '%s/qemu/qemu-system-x86_64' % cwd
disk = sys.argv[1]
qemu_img = ['%s/../parsec_roi/linux-%s.qcow2' %(cwd, disk)]
vm_memory = 8192
qemu_cmd = ''
vnc_counter = 100

num_threads = len(qemu_img)

# If user give argument 'out' then print the output of simulation run
# to stdout else ignore it
out_to_stdout = False
#if len(sys.argv) == 2 and sys.argv[1] == 'out':
#    out_to_stdout = True

# Checkpoint list
check_list = []

benchmark = sys.argv[2]
parsec_list = [benchmark]
# parsec_list += ['blackscholes']
# parsec_list += ['bodytrack']
# parsec_list += ['canneal']
# parsec_list += ['dedup']
# parsec_list += ['facesim']
# parsec_list += ['ferret']
# parsec_list += ['fluidanimate']
# parsec_list += ['freqmine']
# parsec_list += ['raytrace']
# parsec_list += ['streamcluster']
# parsec_list += ['swaptions']
# parsec_list += ['vips']
# parsec_list += ['x264']
# parsec_list += ['lbm']
# parsec_list += ['milc']

# To run single checkpoint
#check_list.append(parsec_list[0])

# To run all spec checkpoints
check_list = parsec_list

checkpoint_lock = Lock()
checkpoint_iter = iter(check_list)

# Simulation Command
sim_file_generic = '''
#-corefreq 2000000000
#-corefreq 3333333333
-corefreq 4000000000
-bench-name %s
-machine shared_l3
-logfile %s.log
-stats %s.stats
-run
-stopinsns 2400m
-kill-after-run
'''

print("Execution command: %s" % qemu_cmd)
print("Chekcpoints to run: %s" % str(check_list))
print("All files will be saved in: %s" % output_dir)


def pty_to_stdout(fd, untill_chr):
    chr = '1'
    while chr != untill_chr:
        chr = os.read(fd, 1)
        sys.stdout.write(chr)
    sys.stdout.flush()


# Thread class that will store the output on the serial port of qemu to file
class SerialOut(Thread):

    def __init__(self, out_filename, out_devname):
        global output_dir
        super(SerialOut, self).__init__()
        self.out_filename = output_dir + out_filename
        self.out_devname = out_devname

    def run(self):
        # Open the serial port xand a file
        out_file = open(self.out_filename, 'w')
        out_dev_file = os.open(self.out_devname, os.O_RDONLY)

        try:
            while True:
                line = os.read(out_dev_file, 1)
                out_file.write(line)
                if len(line) == 0:
                    break
        except OSError:
            pass

        print("Writing to output file completed")
        out_file.close()
        os.close(out_dev_file)

# Thread class that will store the output on the serial port of qemu to file
class StdOut(Thread):

    def __init__(self, out_obj_):
        super(StdOut, self).__init__()
        self.out_obj = out_obj_

    def run(self):
        # Open the serial port and a file
        global out_to_stdout
        try:
            while True:
                line = self.out_obj.read(1)
                if len(line) == 0:
                    break
                if out_to_stdout:
                    sys.stdout.write(line)
        except OSError:
            pass

        print("Writing to stdout completed")


class RunSim(Thread):

    def __init__(self, qemu_img_name):
        super(RunSim, self).__init__()
        self.qemu_img = qemu_img_name

    def add_to_cmd(self, opt):
        self.qemu_cmd = "%s %s" % (self.qemu_cmd, opt)

    def run(self):
        global checkpoint_lock
        global checkpoint_iter
        global vnc_counter
        global output_dir

        print("Running thread with img: %s" % self.qemu_img)

        # Start simulation from checkpoints
        pty_prefix = 'char device redirected to '
        # for checkpoint in check_list:
        while True:
            checkpoint = None
            self.qemu_cmd = ''

            try:
                checkpoint_lock.acquire()
                checkpoint = checkpoint_iter.next()
                self.vnc_counter = vnc_counter
                if vnc_counter != None:
                    vnc_counter += 1
            except:
                checkpoint = None
            finally:
                checkpoint_lock.release()

            if checkpoint == None:
                break

            sim_file_cmd_name = "/tmp/%s.simconfig" % checkpoint
            sim_file_cmd = open(sim_file_cmd_name, "w")
            sim_file_cmd.write(sim_file_generic % (output_dir + checkpoint, 
                                                   output_dir + checkpoint, 
                                                   checkpoint))
            sim_file_cmd.write("\n")
            sim_file_cmd.close()

            # Generate a common command string
            self.add_to_cmd(qemu_bin)
            self.add_to_cmd('-m %s' % str(vm_memory))
            self.add_to_cmd('-serial pty')
            if self.vnc_counter:
            	self.add_to_cmd('-vnc :%d' % self.vnc_counter)
            else:
                self.add_to_cmd('-nographic')

            # Add Image at the end
            self.add_to_cmd('-drive file=%s,cache=unsafe' % self.qemu_img)
            self.add_to_cmd('-simconfig %s' % sim_file_cmd_name)
            self.add_to_cmd('-loadvm %s' % checkpoint)

            print("Starting Checkpoint: %s" % checkpoint)
            print("Command: %s" % self.qemu_cmd)

            p = subprocess.Popen(self.qemu_cmd.split(), stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, stdin=subprocess.PIPE, bufsize=0)

            monitor_pty = None
            serial_pty = None

            while p.poll() is None:
                line = p.stdout.readline()
                sys.stdout.write(line)
                if line.startswith(pty_prefix):
                    dev_name = line[len(pty_prefix):].strip()

                    # Open the device terminal and send simulation command
                    # pty_term = os.open(dev_name, os.O_RDWR)
                    pty_term = dev_name

                    serial_pty = pty_term
                    
                    if serial_pty != None:
                        break

            # Redirect output of serial terminal to file
            serial_thread = SerialOut('%s.out' % (checkpoint), serial_pty)

            # os.dup2(serial_pty, sys.stdout.fileno())

            stdout_thread = StdOut(p.stdout)
            stdout_thread.start()
            serial_thread.start()

            # Wait for simulation to complete
            p.wait()

            serial_thread.join()
            stdout_thread.join()


# Now start RunSim threads
threads = []

for i in range(num_threads):
    th = RunSim(qemu_img[i])
    threads.append(th)
    th.start()

for th in threads:
    th.join()

print "Done :)\n"
