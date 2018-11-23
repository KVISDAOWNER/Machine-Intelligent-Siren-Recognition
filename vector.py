# This file contains functionality for extracting vector data from vectors


# Vector [3 5 3 5] will become [0 1 -1 1 0]
def get_growth_vector(vect):
    g_vector = []
    first = True
    old = 0
    for x in range(len(vect)):
        if first:
            first = False
        else:
            if vect[x] > vect[old]:
                g_vector.append(1)
            elif vect[x] < vect[old]:
                g_vector.append(-1)
            else:
                g_vector.append(0)
        old = x

    return g_vector


# Zero pads a list
def get_zero_padded(list):
    pad_list = []
    pad_list.append(0)
    pad_list.extend(list)
    pad_list.append(0)
    return pad_list
