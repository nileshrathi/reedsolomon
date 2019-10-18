from __future__ import print_function

import unittest
import sys
import string
import random
from random import sample
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
c_exp=10
max_length = 2**c_exp - 1
init_message_len=10
#generate a prime for large field
print("generating a prime for large field")
start_time1 = time.time()
prim = rs.find_prime_polys(c_exp=12, fast_primes=True, single=True)
end_time1= time.time()
prime_poly_time=end_time1-start_time1
print("Time Prime polynomial generation", prime_poly_time)
#initilaize to log and exponenent tables and genrate polynomials
start_time2 = time.time()
print("initializing tables")
rs.init_tables(c_exp=12, prim=prim)
end_time2= time.time()
start_time3 = time.time()
print("generating polynomial")
gen = rs.rs_generator_poly_all(2**c_exp - 1)
end_time3= time.time()

table_init_time=end_time2-start_time2
poly_gen_time=end_time3-start_time3
print("TIME table initilaization ", table_init_time)
print("TIME generaring all generator polynomial ", poly_gen_time)
# need to print size of tables here
print("size of exp table ", sys.getsizeof(rs.gf_exp))
print("size of log table is ",sys.getsizeof(rs.gf_log))


for msg_len in range(10,max_length/2):
    msg=randomString(msg_len)
    nsym=msg_len*2 #consider corruption of all bits
    if nsym+msg_len>max_length:
    	nsym=max_length-msg_len
    enc = rs.rs_encode_msg(msg, nsym, gen=gen[nsym])
    #encode the message
    start_time4 = time.time()
    enc = rs.rs_encode_msg(msg, nsym, gen=gen[nsym])
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
    else:
        print("FAIL")



