import re

class Minterms:
    def __init__(self,*,rep:str=None,n:int=None):
        if not rep is None:
            self.__rep = rep
            self.__bin = Minterms.__create_b_from_r__(minterm=self.__rep)
            self.__n = int(self.__bin,base=2)
        
        elif not n is None:
            self.__n = n
            self.__bin ='{0:b}'.format(n)
            self.__rep = rep

    def __str__(self):
        return self.__bin

    def __int__(self):
        return self.__n

    def __create_b_from_r__(minterm:str):
        minterm=minterm.upper()
        minterm = re.sub("[A-Z]'",'0',minterm)
        minterm = re.sub("[A-Z]",'1',minterm)
        return minterm
    
    def get_representation(self):
        return self.__rep

def create_term_from_binary(bin:str,order:list):
    term = ''
    for i in range(len(order)):
        if bin[i]=='0':
            term+=f"{order[i]}'"
        elif bin[i]=='1':
            term+=order[i]
    return term

def equation_to_minterms(equation:str):
    return [Minterms(rep=i) for i in equation.split('+')]
