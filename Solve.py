from Expression import to_sop
from Minterms import equation_to_minterms,create_term_from_binary
import re

def is_bit_diff1(x,y):
    c=0
    for i,j in enumerate(zip(x,y)):
        if j[0]!=j[1]:
            c+=1
            ind=i
        if c>1:return (False,)
    return (True,ind)

def count1(x):
    return len(re.findall('1',x))

def get_flat_list(x:dict):
    res = []
    for i in x:
        for j in x[i]:
            res.append(j)
    return res

def get_list_diffrence(x:list,y:list):
    res = []
    for i in x:
        exists = False
        for j in y:
            if i[0]==j[0]:
                exists=True
                break
        if not exists:
            res.append(i)
    return res

def QMccluskey(equation:str):
    minterms = equation_to_minterms(equation)
    variables = list(re.findall('[A-Z]',minterms[0].get_representation()))
    variables.sort(key=str.lower)
    min_groups = dict()
    for i in minterms:
        try:
            min_groups[count1(str(i))].append((str(i),[int(i)]))
        except KeyError:
            min_groups[count1(str(i))]=[(str(i),[int(i)])]
    
    rem_implicants = []

    while True:
        print("min_groups :",min_groups)
        k = sorted(min_groups.keys())
        temp=dict()
        change=False
        visited=[]
        for c in range(len(k)-1):
            for i in min_groups[k[c]]:
                for j in min_groups[k[c+1]]:
                    a = is_bit_diff1(i[0],j[0])
                    if a[0]==True:
                        i_st = i[0][0:a[1]]+'_'+i[0][a[1]+1:]
                        i_lis = i[1].copy()
                        i_lis.extend(j[1])
                        try:
                            temp[c].append((i_st,i_lis))
                        except KeyError:
                            temp[c]=[(i_st,i_lis)]
                        change=True
                        visited.extend([i,j])
        if not change:break
        rem_implicants.extend(get_list_diffrence(get_flat_list(min_groups),visited))
        print('rem_implicants :',rem_implicants)
        min_groups = temp.copy()
    
    print('-'*50)
    print(min_groups)
    print(rem_implicants)
    prime_implicants_table = dict()
    for i in minterms:
        prime_implicants_table[int(i)]=set()

    for i in min_groups.keys():
        for j in min_groups[i]:
            for k in j[1]:
                prime_implicants_table[k].add(create_term_from_binary(j[0],variables))

    for i in prime_implicants_table:
        print(i)

def solve(equation="ab+c"):
    QMccluskey(to_sop(equation=equation))   

solve()