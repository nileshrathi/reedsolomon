from __future__ import print_function

import unittest
import sys
import string
import random
import pickle
from random import sample
from pympler import asizeof
import itertools
try:
    from itertools import izip
except ImportError:  #python3.x
    izip = zip

from reedsolo import *
import reedsolo as rs
try:
    bytearray
except NameError:
    from reedsolo import bytearray

try: # compatibility with Python 3+
    xrange
except NameError:
    xrange = range
import time
import decimal
def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))



#code starts here


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

#parameters
c_exp=20
max_length = 2**c_exp - 1
init_message_len=10
#generate a prime for large field
print("generating a prime for large field")
start_time1 = time.time()
prim = rs.find_prime_polys(c_exp=c_exp, fast_primes=True, single=True)
end_time1= time.time()
prime_poly_time=end_time1-start_time1
print("Time Prime polynomial generation", prime_poly_time)
#initilaize to log and exponenent tables and genrate polynomials
start_time2 = time.time()
print("initializing tables")
rs.init_tables(c_exp=c_exp, prim=prim)
end_time2= time.time()
# gf_exp=open('exp.pkl', 'r')
# gf_log=open('log.pkl', 'r')
# rs.gf_exp=pickle.load(gf_exp)
# rs.gf_log=pickle.load(gf_log)
start_time3 = time.time()
# gf_exp.close()
# gf_log.close()
print("generating polynomial")
#gen = rs.rs_generator_poly_all(2**c_exp - 1)
end_time3= time.time()

table_init_time=end_time2-start_time2
poly_gen_time=end_time3-start_time3
print("TIME table initilaization ", table_init_time)
print("TIME generaring all generator polynomial ", poly_gen_time)

#saving tables

afile = open('exp.pkl', 'w')
pickle.dump(rs.gf_exp, afile)
afile.close()

afile = open('log.pkl', 'w')
pickle.dump(rs.gf_log, afile)
afile.close()

# need to print size of tables here
print("size of exp table ", asizeof.asizeof(rs.gf_exp))
print("size of log table is ",asizeof.asizeof(rs.gf_log))


msg_len_array=[]
nsym_len_array=[]
enc_time_array=[]
dec_time_array=[]
for msg_len in range(10,max_length/3,100):
    msg=randomString(msg_len)
    nsym=msg_len*2 #consider corruption of all bits
    if nsym+msg_len>max_length:
    	nsym=max_length-msg_len
    #encode the message
    gen_one=rs.rs_generator_poly(nsym=nsym)
    start_time4 = time.time()
    enc = rs.rs_encode_msg(msg, nsym, gen=gen_one)
    end_time4 = time.time()
    encoding_time=end_time4-start_time4


    poscorrup=random.sample(range(0, msg_len+nsym-2), nsym/2)
    for x in poscorrup:
        enc[x]=random.randint(0,100)
    
    start_time5=time.time()
    rmes, recc = rs.rs_correct_msg(enc, nsym, erase_pos=None)
    end_time5=time.time()
    decoding_time=end_time5-start_time5


    mesbytarray="".join(chr(i) for i in rmes)
    if msg == mesbytarray:
        print(" msg len= %d errors=%d  enc_timr= %f dec_time= %f" %(msg_len,nsym/2,encoding_time,decoding_time))
        msg_len_array.append(msg_len)
        nsym_len_array.append(nsym)
        enc_time_array.append(encoding_time)
        dec_time_array.append(decoding_time)
    else:
        print("FAIL")

msg_len_file=open('msg_len_arr.obj', 'w')
nsym_len_file=open('nsym_len_arr.obj', 'w')
enc_time_file=open('enc_time_arr.obj', 'w')
dec_time_file=open('dec_time_arr.obj', 'w')

pickle.dump(msg_len_array, msg_len_file)
pickle.dump(nsym_len_array, nsym_len_file)
pickle.dump(enc_time_array, enc_time_file)
pickle.dump(dec_time_array, dec_time_file)

msg_len_file.close()
nsym_len_file.close()
enc_time_file.close()
dec_time_file.close()