import numpy as np
import timeit
import time
import matplotlib.pyplot as plt
from tqdm import tqdm






# ----------- UTILS -----------
# converts strings like '0100101' into numpy arrays, where each entry is a different value
def str_to_bin_array(s):
	a = np.array(list(s), dtype=int)
	return a


# opposite of str_to_bin_array
def bin_array_to_str(a):
	b = ''
	for x in a:
		b += str(x)
	return b


# converts a np bin array to an int
def bin_array_to_int(a):
    return int(bin_array_to_str(a), 2)


# sum decimal digits of a decimal integer
def sum_dec_digits(a):
    a = str(a)
    s = 0
    for x in a:
        s = s + int(x)
    return s


# r computaton starting from the key, challenge and counter
def r_calc(k, c, n):
    # takes as input k and c np arrays and n integer
    c = int(bin_array_to_str(c),2)
    sc = sum_dec_digits(c)
    k = int(bin_array_to_str(k),2)
    t = k + n
    st = sum_dec_digits(t)
    s = st * sc
    return int(bin(s)[2:],2)






# ----------- INIT -----------
# A and B have a dictionary which contains protocol parameters and values they exchange each other 
A = {'key' : None, 'challenge' : None, 'n_counter' : None, 'id_A' : None , 'u2' : None, 'r' : None}
B = {'key' : None, 'challenge' : None, 'n_counter' : None, 'id_A' : None , 'u2' : None, 'r' : None}


# ----------- PROTOCOL -----------
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
    '''
    if r_exp == B.get('r'):
        print('authentication accepted')
    else:
        print('authentication rejected')
    '''
    return str(r_exp)






# ----------- TESTING THE PROTOCOL -----------
# testing with n = 0, lc = lk = 8 
def task1():
  print('-------- SETUP --------')
  n_init, key = setup(0, 8) 
  print('n initial value =', n_init)
  print('key value =', key)

  print('\n-------- STEP 1 --------')
  u1 = step1()
  print('u1 =', u1)

  print('\n-------- STEP 2 --------')
  u2 = step2(8)
  print('u2 = ' + '(' + bin_array_to_str(u2[0]) + ', ' + str(u2[1]) + ')')

  print('\n-------- STEP 3 --------')
  r_computed = step3()
  print('u3 =', r_computed)

  print('\n-------- STEP 4 --------')
  r_expected = step4()
  if r_expected == r_computed:
          print('authentication accepted')
  else:
      print('authentication rejected')
  complexity_task1()

def method_for_task3(tryKey,trueKey,n,Lk):
  A['key'] = str_to_bin_array(tryKey)
  B['key'] = str_to_bin_array(trueKey)

  B['n_counter'] = n

  A['id_A'] = np.random.randint(0, 2, 1, dtype=int)

  u1 = step1()

  u2 = step2(Lk)

  r_computed = step3()

  r_expected = step4()

  if r_expected == r_computed:
      return True
  else:
      return False


# ----------- PLOT TASK 1 -----------
# this method compute the protocol time for specific lengths of c and k
def time_protocol(len_k, len_c):
    start = time.time()

    _, _ = setup(0, len_k)
    _ = step1()
    _ = step2(len_c)
    _ = step3()
    step4()

    end = time.time()
    return end - start

'''
# THIS IS  DONE JUST FOR COMPUTING THE .npy FILE -> TOO LONG IN ORDER TO COMPUTE EVERY TIME
# fill a matrix to compute a countout plot
time_protocol_arr = np.zeros((256, 256))
# computing ideal capacity matrix based on different values of epsilon and delta
for i in tqdm(range (1, 256)):
    for j in range(256):
        time_protocol_arr[i, j] = time_protocol(i, j)

# save array 
np.save('arr_task1', time_protocol_arr)
'''
def complexity_task1():
  # load the .npy file in a np array
  time_protocol_arr = np.load('arr_task1.npy')


  '''
  # the linear tren is real just for high intervals of lk values
  test = np.zeros(10000)
  for i in range(1, 10000):
      test[i] = time_protocol(i, 8)
  '''


  # plots for different len of c
  ticks_arr = np.arange(0, 256, step=16)
  for x in range(16):
      plt.plot(time_protocol_arr[:][x])

  plt.xticks(ticks_arr)
  plt.title('computational complexity of a legitimate protocol run')
  plt.xlabel('key length')
  plt.ylabel('protocol time')
  plt.show()



  # countour plot
  max_time = np.amax(time_protocol_arr) # getting nice levels
  lengths_arr = np.arange(0, 256, step=1)
  ticks_arr = np.arange(0, 256, step=8)
  levels = np.arange(0, max_time, step=0.0001)
  plt.contour(lengths_arr, lengths_arr, time_protocol_arr, levels, linewidths=1, cmap='RdYlGn')
  n_label = lengths_arr
  plt.xticks(ticks_arr)
  plt.yticks(ticks_arr)
  plt.title('computational complexity of a legitimate protocol run')
  plt.xlabel('key length')
  plt.ylabel('challenge length')
  plt.colorbar()
  plt.show()