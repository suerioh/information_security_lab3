import numpy as np
import timeit
import time
import matplotlib.pyplot as plt
from tqdm import tqdm
import random

from utils import str_to_bin_array, bin_array_to_str, bin_array_to_int,sum_dec_digits, r_calc,getSum,countDigits,findNdigitNums
from task1 import setup,step1,step2,step3,step4

# ----------- INIT -----------
# A and B have a dictionary which contains protocol parameters and values they exchange each other 
A = {'key' : None, 'challenge' : None, 'n_counter' : None, 'id_A' : None , 'u2' : None, 'r' : None}
B = {'key' : None, 'challenge' : None, 'n_counter' : None, 'id_A' : None , 'u2' : None, 'r' : None}

def task2(r,c,n,lk):

    #bin string -> decimal
    c_dec = int(bin_array_to_str(c),2)

    sc = getSum(c_dec)
    #r = str(bin(int(r,2))[2:].zfill(lk))
    s = int(r,2)

    st = int(s/sc)
    ln = countDigits(n)
    lt_max = countDigits((2**lk)-1)
    
    t = []
    for i in range(ln,lt_max+1):
        findNdigitNums(i,st,t)

    #print(t)

    k =[str(int(x,10) - n) for x in t if int(x,10) - n >= 0 and int(x,10) - n <= ((2**lk)-1)]
    return k


def setup_task2(n,lk,lc):
    ida,k = setup(n,lk)
    A['key'] = str_to_bin_array(k)
    B['key'] = str_to_bin_array(k)
    # store n inside B dictionaty
    B['n_counter'] = n
    A['id_A'] = str_to_bin_array(ida)
    # keyTrue = ''.join(random.choice(['0','1']) for i in range(lk))
    # #print('true key: ',int(keyTrue,2))
    # B['key'] = str_to_bin_array(keyTrue)
    # B['n_counter'] = n  
    # A['id_A'] = np.random.randint(0, 2, 1, dtype=int)
    # A['key'] = str_to_bin_array(keyTrue)   
    
    u1 = step1()#ida
    u2 = step2(lc) #c,n     
    r_computed = step3()#r
    r_expected = step4()#responce

    k = task2(r_computed,u2[0],n+1,lk)
    
    for key in k:
        #print('possible key: ',key)
        A['key'] = str_to_bin_array(str(bin(int(key,10))[2:].zfill(lk))) 
        u1 = step1()#ida
        u2 = step2(lk) #c,n    
        #print("challenge: ",bin_array_to_int(u2[0])," n: ",u2[1]) 
        r_computed = step3()#r
        r_expected = step4()#responce
        if r_expected == r_computed:
            success_prob = 1/len(k)
            return True,key,success_prob
    
    return False,None,0

def execution_Task2(lk,lc):

    start = time.time()
    res,key,success_prob = setup_task2(25,lk,lc)
    if res:
        print("Key founded: ",key)
    else:
        print("Key not founded")

    end = time.time()

    return end-start,success_prob

def test_complexity_task2():

    time = np.zeros(30)
    suc_prob = np.zeros(30)

    for i in range(30):
        print(i)
        time[i],suc_prob[i] = execution_Task2(i+4,8)
    
    np.save('time_arr_lc_8',time)
    np.save('succ_prob_arr_lc_8',suc_prob)

    for i in range(20):
        print(i)
        time[i],suc_prob[i] = execution_Task2(i+1,16)
    
    np.save('time_arr_lc_16',time)
    np.save('succ_prob_arr_lc_16',suc_prob)
    
test_complexity_task2()

plt.plot(np.arange(30),np.load('time_arr_lc_8.npy'))
plt.show()
