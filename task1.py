import numpy as np
import time
import matplotlib.pyplot as plt
from tqdm import tqdm

from utils import str_to_bin_array, bin_array_to_str, bin_array_to_int, sum_dec_digits, r_calc




# ----------- INIT -----------
# A and B have a dictionary which contains protocol parameters and values they exchange each other 
A = {'key' : None, 'challenge' : None, 'n_counter' : None, 'id_A' : None , 'u2' : None, 'r' : None}
B = {'key' : None, 'challenge' : None, 'n_counter' : None, 'id_A' : None , 'u2' : None, 'r' : None}


# ----------- TASK 1 -----------
# setup init the key and challenge length and the initial value of the counter
def setup(n, lk):
    k = np.random.randint(0, 2, lk, dtype=int)
    # update key value in each dictionary
    A['key'] = k
    B['key'] = k
    # store n inside B dictionaty
    B['n_counter'] = n
    # also A generate its identity idA as a single random bit
    idA = np.random.randint(0, 2, 1, dtype=int)
    # A stores idA in its dictionary
    A['id_A'] = idA
    return bin_array_to_str(idA), bin_array_to_str(k)


# step 1 -> A sends B its id
def step1():
    # B get the idA
    B['id_A'] = A.get('id_A')
    u1 = B.get('id_A')
    # print('u1 =', u1)
    return bin_array_to_str(u1)


# step 2 -> B sends to B a challenge and the counter value
def step2(lc):
    # B generates a random challenge, update the counter and store them in its dictionary
    c = np.random.randint(0, 2, lc, dtype=int)
    B['challenge'] = c
    B['n_counter'] += 1
    # B computes u2, stores it and sends it to A
    B['u2'] = [B.get('challenge'), B.get('n_counter')]
    # A gets u2 and store it in its dictionary
    u2 = B.get('u2')
    A['u2'] = u2
    # print('u2 = ', u2)
    return u2


# step 3 -> A computes r and sent it to B
def step3():
    # A extract c and n from u2 and store them in the dictionary
    A['challenge'] = A.get('u2')[0]
    A['n_counter'] = A.get('u2')[1]
    # u3 computation using the r_calc util method
    r = r_calc(A.get('key'), A.get('challenge'), A.get('n_counter'))
    A['r'] = r
    # print('u3 =', r)
    return str(r)
    

# step 4 -> B compares r with the expected response r^
def step4():
    # B receive the u3 = r
    B['r'] = A.get('r')
    # B compute the expected response using its values
    r_exp = r_calc(B.get('key'), B.get('challenge'), B.get('n_counter'))
    return str(r_exp)


# compute an array which contains protocol time for the first len_k keys and for a fixed len_c 
def get_time(len_k, len_c):
    time_arr = np.zeros(len_k)

    # for each iteration i use the time_procol method to compute the protocol time
    for i in tqdm(range(1, len_k)):
        time_arr[i] = time_protocol(i, len_c)

    # a np array is returned
    return time_arr