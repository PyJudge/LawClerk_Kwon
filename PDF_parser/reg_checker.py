# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 09:08:33 2020

@author: LatteFairy
"""
#%%
class Cursor: 
    def __init__(self, t, pos): #text, position 
        self.t = t
        if pos < len(t):
            self.pos = pos
        else:
            raise ValueError('pos error, 길이가', len(t),'인데 pos가', pos)
            
    #%% 

def letter_f(to_f: str): # cursor 포지션만 본 다음, to_find와 다르면 '', 아니면 cursor pos 글자와 같은 글자를 아웃풋하는 함수를 만듦
    assert len(to_f) == 1 # to_f는 한 글자여야 함

    def ret_f(c: Cursor) -> str:
        if c.t[c.pos] == to_f:
            return to_f
        else:
            return ''
    
    return ret_f

def or_f(l: list): # list 중 하나에 해당하면 letter_f 와 같은 동작 수행 
    l1 = [str(i) for i in l]
    rst = list(map(letter_f, l1))    
    
    def ret_f(c : Cursor) -> str:  
        for f in rst:
            if f(c):
                return f(c)
        return ''
    
    return ret_f
#%%        
        
        
    
#%%
t = 'cursor 포지션만 본 다음, to_find와 다르면 '', 아니면 cursor pos 글자와 같은 글자를 아웃풋하는 함수를 만듦'
f = letter_f('u')
c1 = Cursor(t, 2) # false
c2 = Cursor(t, 1) # true
f(c1), f(c2)
#%%
f = or_f(['포', 'u'])
f(c1), f(c2)

#%%
def chunk_f(to_f: list): 
    #to_find는 각 글자에 대한 것임, to_f[0]은 0번째에 일치할 문자열 집합, 1자보다 길 때, 문자열을 아웃풋하는 함수(없으면 '') 만듦
    #정확히 동일한 사이즈만 동작함, 커서 위치부터 읽기 시작하여 len만큼 읽음 
    #문자열은 다 일치할 때만 output할 것 
    def ret_f(c:Cursor) -> str:
        cc = [Cursor(c.t, i) for i in range(c.pos, c.pos + len(to_f))] # len만큼 읽고, 
#        print('cc', [c.t[c.pos] for i,c in enumerate(cc)])
        ref = [to_f[i] for i in range(len(to_f))]  # 여기에 맞는 찾기 기준을 불러옴 
        ff = list(map(or_f, ref)) # 함수의 리스트를 만들고 
#        print('len to_f', len(to_f), len(ff), len(cc))
        result = [ff[i](cc[i])  for i in range(len(to_f))] # 각 자리에 찾은 결과를 만들어 줌
        output = ''
        for r in result:
            if r == '':
                return '' # 다 맞는 결과를 못 찾을 경우 빈 글자를 반환 
            else :
                output += r 
        return output

#        assert len(text) == len(to_f) #정확히 동일한 사이즈에만 동작함, 이후 확장할 것임 
#        while (c.pos < end)
    return ret_f
    
#%% 
def sent_f(to_f: list):
    """
    to_f를 받아서 
        text를 주면, Cursor를 만들어서 [(찾은 글자, 위치), (찾은 글자, 위치),....]/ 못찾으면 빈 리스트 
        반환하는 함수를 반환함 
    """
    length = len(to_f) # 0~ length번까지 postion으로 cursor를 만듦 0~ 9까지에서 5글자 찾으려면 0, 1, 2, 3, 4, 5(9번까지 하면 5글자)]
    def ret_f(text: str) -> list:
        cc = [Cursor(text, i) for i in range(len(text) - length + 1)]
        result = [(chunk_f(to_f)(c), c.pos) for c in cc] # to find를 c에서 찾아라 
        result = [r for r in result if r[0] !=''] # 못 찾은 경우는 지우기
        return result
    return ret_f
    
    
#%%
y = [str(i) for i in range(10)]
m = [str(i) for i in range(10)]
d = [str(i) for i in range(10)]

"""
reg_list = [
        [y, y, y, y, ['-'], m, m, ['-'], d, d],
        [y, y, y, y, ['.', ],[' '], m, m, ['.',]],
        [y, y, y, y, ['.', ],[' '], m, ['.',]],
        [y, y, ['.', ],[' '], m, m, ['.',]],
        [y, y, ['.', ],[' '], m, ['.',]],
        [y, y, y, y, ['년'],[' '], m, m, ['월']],
        [y, y, y, y, ['년'],[' '], m, ['월']],
        [y, y, ['년'],[' '], m, m, ['월']],
        [y, y, ['년'],[' '], m, ['월']],
        [y, y, y, y, ['.', ],[' '], m, m, ['.',], [' '], d, d, ['.']],
        [y, y, y, y, ['.', ],[' '], m, ['.',], [' '], d, d, ['.']],
        [y, y, ['.', ],[' '], m, m, ['.',], [' '], d, d, ['.']],
        [y, y, ['.', ],[' '], m, ['.',], [' '], d, d, ['.']],
        [y, y, y, y, ['.', ],[' '], m, m, ['.',], [' '], d, ['.']],
        [y, y, y, y, ['.', ],[' '], m, ['.',], [' '], d, ['.']],
        [y, y, ['.', ],[' '], m, m, ['.',], [' '], d, ['.']],
        [y, y, ['.', ],[' '], m, ['.',], [' '], d, ['.']],
        [y, y, y, y, ['년'],[' '], m, m, ['월'], [' '], d, d, ['일']],
        [y, y, y, y, ['년'],[' '], m, ['월'], [' '], d, d, ['일']],
        [y, y, ['년'],[' '], m, m, ['월'], [' '], d, d, ['일']],
        [y, y, ['년'],[' '], m, ['월'], [' '], d, d, ['일']],
        [y, y, y, y, ['년'],[' '], m, m, ['월'], [' '], d, ['일']],
        [y, y, y, y, ['년'],[' '], m, ['월'], [' '], d, ['일']],
        [y, y, ['년'],[' '], m, m, ['월'], [' '], d, ['일']],
        [y, y, ['년'],[' '], m, ['월'], [' '], d, ['일']],
        [y, y, y, y, ['.', ]],
        [y, y, y, y, ['년', ]],
        [y, y, y, y, ['.', ],[' ']],
        [y, y, ['.', ],['경']],
        [y, y, ['년', ]],
        [y, y, ['.', ],[' ']],
        ]
"""

#%%

def is_in_span(x, y): #x가 y span 안에 있다
    start_x, start_y = x[1], y[1]
    end_x, end_y= (x[1] + len(x[0])), (y[1] + len(y[0]))
    if (start_y <= start_x) and (end_x<= end_y):
        return True
    else:
        return False

def reg_finder(text, reg_list):
    ff = list(map(sent_f, reg_list))
    result = [f(text) for f in ff if f(text)]
    result = [j for res in result for j in res]
    final = []
    for i in range(len(result)):
        copy = True
        for j in range(len(result)):
            if i != j and is_in_span(result[i], result[j]):
                copy = False
        if copy:
            final.append(result[i])
            
    return final 
        
#%% 연 월 일 스플릿한 다음 > 연월일 숫자로 
yyyy_reg = [[y,y,y,y], [y,y], [y]]

def ymd_spliter(final, year_reg = yyyy_reg):    
    data = [c[0] for c in final] 
    
    year = []
    for i in data:
        d = reg_finder(i, reg_list=yyyy_reg)
        d = sorted(d, key = lambda x : x[1])
        year.append(d)
    date = []
    for each_date in year:
        each_ = 0
        for i, m in enumerate(each_date):
            if i == 0 : #연이면, 
                if m[0] == 0: # 연도는 반드시 필요함 
                    continue
                if not (len(m[0]) == 2 or len(m[0]) == 4): #2자리 아니면 네 자리 
                    continue
                if (int(m[0]) <= 2030) and (int(m[0]) >= 1890) or (len(m[0]) == 2): # m[0]가 실제 연, 월, 일 등이 표시되는 란임, 연도가 될 조건 충족시
                    if len(m[0]) == 2 and int(m[0]) < 30:
                        each_ += int('20'+ m[0]) * 10000
                    elif len(m[0]) == 2 and int(m[0]) >= 30:
                        each_ += int('19'+ m[0])*10000
                    else:
                        each_ += int(m[0]) *10000
            if i == 1: 
                if int(m[0]) > 13:
                    continue
                each_ += int(m[0]) * 100
            if i == 2:
                each_ += int(m[0])
        if each_ > 18900000:
            date.append(each_date[0], each_)
    return date             
        

# %%

# %%
