## import modules here 
import pandas as pd
import numpy as np


################# Question 1 #################

# helper functions

def read_data(filename):
    df = pd.read_csv(filename, sep = '\t')
    return df
def project_data(df, d):
    # Return only the d-th column of INPUT
    return df.iloc[:, d]

def select_data(df, d, val):
    # SELECT * FROM INPUT WHERE input.d = val
    col_name = df.columns[d]
    return df[df[col_name] == val]

def remove_first_dim(df):
    # Remove the first dim of the input
    return df.iloc[:, 1:]

def slice_data_dim0(df, v):
    # syntactic sugar to get R_{ALL} in a less verbose way
    df_temp = select_data(df, 0, v)
    return remove_first_dim(df_temp)

def buc_rec4(data, L, R, x, y, dic):

    dims = data.shape[1]

    if dims == 1:
        input_sum = sum(project_data(data, 0))
        dic[tuple(L)] = input_sum
        R.append(input_sum)


    else:
        dim0_vals = set(project_data(data, 0).values)



        for dim0_v in dim0_vals:

            if(data.shape[0] == x and data.shape[1] == y):
                L.append(str(dim0_v))

            else:
                L.append(str(dim0_v))
            sub_data = slice_data_dim0(data, dim0_v)
            buc_rec4(sub_data, L, R, x, y, dic)
            L.pop()
        
        
        
        sub_data = remove_first_dim(data)
        if(data.shape[0] == x and data.shape[1] == y):
            L.append('ALL')

        else:
            L.append('ALL')
        
        buc_rec4(sub_data,L, R, x ,y, dic)

        L.pop()

def buc_rec_optimized(df):# do not change the heading of the function
    data = df
    columns_list = list(data.columns.values)

    measure_list = columns_list[-1]
    columns_L = columns_list[: -1]
    
    
    (x, y) = data.shape
    L = []
    R = []
    dic = {}
    buc_rec4(data, L, R, x, y, dic)


    dic_List = []

    for i in range(len(columns_L)):
        l = []
        for j in dic:
            l.append(j[i])

        dic_temp = {}
        dic_temp[columns_L[i]] = l
        dic_List.append(dic_temp)


    dic_temp = {}
    l = []
    for j in dic:
        l.append(dic[j])

    dic_temp[measure_list] = l
    dic_List.append(dic_temp)
    

    a= dic_List[0]

    for i in range(1, len(dic_List)):
        a.update(dic_List[i])

    new_df = pd.DataFrame(a, dtype = 'int64')
    return new_df

################# Question 2 #################

def getSSE(lst):
    s = sum(lst)
    mean = s / len(lst)

    res = 0

    for i in lst:
        res += (i - mean) ** 2

    return res

def v_opt_dp(x, num_bins):# do not change the heading of the function
    b = num_bins
    matrix = [[-1] * len(x) for _ in range(b)]
    matrixPath = [[None] * len(x) for _ in range(b)]
    
    rightmost = len(x) - 1

    res = []
    #print(rightmost)
    
    for i in range(b):
        for j in range(rightmost - i, rightmost - i - b + 1, -1):

            if j == rightmost - i:
                matrix[i][j] = 0

                temp_l = []
                for jj in range(j, rightmost + 1):
                    temp_l += [x[jj]]

                matrixPath[i][j] = temp_l
                continue

            if i + 1 == 1:
                matrix[i][j] = getSSE(x[j:])
                matrixPath[i][j] = [x[j:]]
                continue

           
            splitNb = i + 1
            k = j
            kMax = rightmost - i
            targetK = j;
           
            minValue = float('inf')

            
            for kk in range(k, kMax + 1):

                currValue = getSSE(x[j: kk + 1]) + matrix[i - 1][kk + 1]
                
                if(minValue > currValue):
                    targetK = kk
                    minValue = currValue


            matrix[i][j] = minValue
            matrixPath[i][j] = [x[j: targetK + 1]] + matrixPath[i - 1][targetK + 1]
            
            
            


    return matrix, matrixPath[b - 1][0]