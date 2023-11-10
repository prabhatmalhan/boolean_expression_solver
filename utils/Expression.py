import regex as re

class Expression:
    def __add_term__(self,x:str,y:str):
        if x=='1' or y=='1':return '1'
        if x=='0':return y
        elif y=='0':return x
        sum_term = list(set(f'{x}+{y}'.split('+')))
        return '+'.join(sum_term)
    
    def __add_iter__(self,x):
        if not x.__iter__():raise Exception('Parameter is not iterable')
        if len(x)==1:
            return x[0]
        s = self.__add_term__(x[0],x[1])
        for i in x[2:]:
            s = self.__add_term__(s,i)
        return s

    def __multiply_term__(self,x:str,y:str):
        product_term = []
        for i in x.split('+'):
            for j in y.split('+'):
                term = list(set([c for c in f'{i}{j}']))
                try:
                    term.remove('*')
                except:
                    pass
                if '0' in term:continue
                if '1' in term:term.remove('1')
                term.sort(key=str.lower)
                product_term.append('*'.join(term))
        if len(product_term)==0:return '0'
        return '+'.join(set(product_term))
    
    def __multiply_iter__(self,x):
        if not x.__iter__():raise Exception('Parameter is not iterable')
        if len(x)==1:
            return x[0]
        prod = self.__multiply_term__(x[0],x[1])
        for i in x[2:]:
            prod = self.__multiply_term__(prod,i)
        return prod

    def __complement__(self,x:str):
        x = x.replace('1','$')
        x = x.replace('0','1')
        x = x.replace('$','0')
        x = x.swapcase()
        
        to_product = []
        for i in x.split('+'):
            to_sum = i.split('*')
            to_product.append(self.__add_iter__(to_sum))
        
        return self.__multiply_iter__(to_product)

    def __addSymbols__(self,equation:str=None):
        if equation==None:return
        equation ='('+ equation.strip().upper()+')'
        for i in re.findall("[A-Z]'",equation):equation = equation.replace(i,i[0].lower())
        equation = re.sub(r" +",'',equation)

        l = re.findall("[^a-zA-Z0-9][a-zA-Z]+",equation)
        for i in l:
            if(len(i))>2:
                x = i[1:]
                p = '*'.join([*x])
                equation = equation.replace(i,i[0]+p)

        equation = equation.replace(')(',')*(')
        equation = equation.replace("'(","'*(")
        equation = re.sub(r"\)([a-zA-z0-9])",r')*\1',equation)
        equation = re.sub(r"([a-zA-z0-9])\(",r'\1*(',equation)
        return equation
    
    def __postfix__(self,equation:str=None):
        if equation==None:return None
        equation = '('+equation+')'
        postfix = ''
        stack = []
        precedence = {'(':0,'+':1,'*':3,"'":4}

        for i in equation:
            if i.isalpha() or i=='0' or i=='1':
                postfix=postfix+i
            elif i=='(':
                stack.append(i)
            elif i==')':
                while stack[-1]!='(':postfix+=stack.pop()
                stack.pop()
            else:
                while precedence[stack[-1]]>=precedence[i]:postfix+=stack.pop()
                stack.append(i)

        return postfix
    
    def __solve_postfix__(self,equation:str=None):
        if equation==None:return None
        stack = []
        for i in equation:
            if i.isalpha() or i=='0' or i=='1':
                stack.append(i)
            elif i=='+':
                y = stack.pop()
                x = stack.pop()
                stack.append(self.__add_term__(x,y))
            elif i=='*':
                y = stack.pop()
                x = stack.pop()
                stack.append(self.__multiply_term__(x,y))
            elif i=="'":
                x = stack.pop()
                stack.append(self.__complement__(x))
        s_equation = stack.pop()
        for i in re.findall("[a-z]",s_equation):s_equation = s_equation.replace(i,f"{i.upper()}'")
        return s_equation.replace('*','')
            
def solve(equation:str=None):
    if equation==None:return None
    self = Expression()
    x= self.__solve_postfix__(equation=self.__postfix__(equation=self.__addSymbols__(equation=equation)))
    return x

def to_sop(equation:str=None):
    if equation==None:return None
    equation = solve(equation)
    all_elements = set(re.findall('[A-Z]',equation))

    to_be_minterm = []
    for i in equation.split('+'):
        term = i
        for j in all_elements-set(re.findall('[A-Z]',i)):
            term+=f"({j}+{j}')"
        to_be_minterm.append(term)
    n_equation = '+'.join(to_be_minterm)
    return solve(n_equation)
