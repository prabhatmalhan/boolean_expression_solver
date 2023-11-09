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
    if c!=1:return (False,)
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
        min_groups = temp.copy()
    
    prime_implicants_table = dict()
    for i in minterms:
        prime_implicants_table[int(i)]=set()

    for i in min_groups:
        for j in min_groups[i]:
            for k in j[1]:
                prime_implicants_table[k].add(create_term_from_binary(j[0],variables))

    for i in rem_implicants:
            for j in i[1]:
                prime_implicants_table[j].add(create_term_from_binary(i[0],variables))

    solution = set()
    for i in prime_implicants_table:
        if len(prime_implicants_table[i])==1:
            for j in prime_implicants_table[i]:
                solution.add(j)
    return '+'.join(solution)


def solve(equation=None):
    if equation == None:return ""
    x = to_sop(equation=equation)
    if x=='1' or x=='0':return x
    return QMccluskey(x)   