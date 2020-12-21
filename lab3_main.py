import numpy as np
import time
import matplotlib.pyplot as plt
from tqdm import tqdm

from utils import str_to_bin_array, bin_array_to_str, bin_array_to_int, sum_dec_digits, r_calc
from task1 import setup, step1, step2, step3, step4, get_time




def main():


    # ----------- TESTING THE PROTOCOL -----------
    # testing protocol steps with: n = 0, lc = lk = 8 

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




    # ----------- PLOT TASK 1 -----------
    # this method compute the total protocol time for specific lengths of c and k (the n init is always 0)
    def time_protocol(len_k, len_c):
        start = time.time()

        _, _ = setup(0, len_k)
        _ = step1()
        _ = step2(len_c)
        _ = step3()
        step4()

        end = time.time()
        
        # computing time and returning it, a scalar is returned
        return end - start


    # save array computed using the get_time method in order not to calculate it every script run
    # np.save('time_arr_lc_1024', get_time(10000, 1024))

    # this is useful for the following interpolations
    x_values = np.arange(0, 10000, step=1)

    # loading the protocol times for lc = 8, and find the linear interpolation of degree 1 
    arr_plot1 = np.load('time_arr_lc_8.npy')
    m1, b1 = np.polyfit(x_values, arr_plot1, 1)

    # loading the protocol times for lc = 256, and find the linear interpolation of degree 1 
    arr_plot2 = np.load('time_arr_lc_256.npy')
    m2, b2 = np.polyfit(x_values, arr_plot2, 1)

    # loading the protocol times for lc = 1024, and find the linear interpolation of degree 1 
    arr_plot3 = np.load('time_arr_lc_1024.npy')
    m3, b3 = np.polyfit(x_values, arr_plot3, 1)


    # actual plotting of raw data and the corresponding linear interpolations
    plt.plot(arr_plot1, label='raw lc = 8', alpha=0.3, c='b')
    plt.plot((np.inner(m1, x_values)) + b1, label='interpol lc = 8', alpha=1, c='b')

    plt.plot(arr_plot2, label='raw lc = 256', alpha=0.3, c='g')
    plt.plot((np.inner(m2, x_values)) + b2, label='interpol lc = 256', alpha=1, c='g')

    plt.plot(arr_plot3, label='raw lc = 1024', alpha=0.3, c='r')
    plt.plot((np.inner(m3, x_values)) + b3, label='interpol lc = 1024', alpha=1, c='r')

    plt.title('computational complexity of a legitimate protocol run for different key length')
    plt.xlabel('key length')
    plt.ylabel('protocol time')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()