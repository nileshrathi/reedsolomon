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

# for i in range(0,255,2):
#     #rs=RSCodec(nsym=i,c_exp=10)
#     rs=RSCodec(i)
#     msg=bytearray(randomString(255), "latin1")
#     enc=rs.encode(msg)
#     poscorrup=random.sample(range(0, 128), i/2)
#     for j in range(0,len(poscorrup)):
#         enc[j]=random.randint(0,100)
#     start_time = time.time()
#     dec=rs.decode(enc)
#     end_time = time.time()
#     #print("msg= ", msg)
#     #print("enc= ", enc)
#     #print("dec= ", dec)
#     if msg==dec:
#         print("Success decoding RS<%d,%d> time = %f " %(255-i,i,end_time-start_time))
#     else:
#         print("fail")

prim = rs.find_prime_polys(c_exp=12, fast_primes=True, single=True)
rs.init_tables(c_exp=12, prim=prim)
n = 255
nsym = 12
mes = "a" * (n-nsym)
#mesbytarray=[elem.encode(decimal.Decimal) for elem in mes]
gen = rs.rs_generator_poly_all(n)
print(len(gen))
enc = rs.rs_encode_msg(mes, nsym, gen=gen[nsym])
enc[1] = 0
enc[2]=0
enc[4]=0
enc[8]=0
enc[32] = 0
enc[33]=0

rmes, recc = rs.rs_correct_msg(enc, nsym, erase_pos=None)
# print("msg= ", mes)
# print("enc= ", enc)
# print("dec= ", rmes)

mesbytarray="".join(chr(i) for i in rmes)
#print("mesba= ",mesbytarray)
#print(type(mes),type(mesbytarray))
if mes == mesbytarray:
    print("Sucess")
else:
    print("FAIL")
# i=10
# #rs=RSCodec(nsym=i,c_exp=10)
# rs=RSCodec(i)
# msg=bytearray(randomString(20), "latin1")
# enc=rs.encode(msg)
# poscorrup=random.sample(range(0, 128), i/2)
# for j in range(0,len(poscorrup)):
#     enc[j]=random.randint(0,100)
# start_time = time.time()
# dec, dec_enc = rs.decode(enc)
# end_time = time.time()
# print("msg= ", msg)
# print("enc= ", enc)
# print("dec= ", dec)
# if msg==dec:
#     print("Success decoding RS<%d,%d> time = %f " %(255-i,i,end_time-start_time))
# else:
#     print("fail")

