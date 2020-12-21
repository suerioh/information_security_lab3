import numpy as np




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
    c = bin_array_to_str(c)
    sc = sum_dec_digits(c)
    k = int(bin_array_to_str(k))
    t = k + n
    st = sum_dec_digits(t)
    s = st * sc
    return int(bin(s)[2:])