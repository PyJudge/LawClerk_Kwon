#%%
from regex.reg_checker import reg_finder
from regex.reg_list import split_reg, evid_reg, year_reg, month_reg, useless_token, ignore_date_3_chars, ignore_date_2_chars, ignore_date_w_space
import re, logging
from setting import Setting

# 다음과 같은 문장으로 시작하는 경우, 사건 선후와 관계없는 등 정리할 필요 없는 것으로 보임, 3글자로 만들 것

def sent_splitter(text, split_reg = split_reg):
    splited = re.split(split_reg, text) #결과값에 none도 있으므로 지우고, reg와 같은 결과값이 '다.'하는 식으로 남아 있으므로 이 부분은 합침 
    #작은 함수 정의 
    none_cleaner = lambda splited : [e for e in splited if e != None] 
    none_cleaned = none_cleaner(splited)
    none_cleaned = [sent.strip() for sent in none_cleaned]

    if len(none_cleaned) % 2 == 0 : # 마지막 문장이 split 이후 남아 있는 경우임 
        return [e + none_cleaned[i+1] for i, e in enumerate(none_cleaned) if i % 2 == 0]
    else:
        return [e + none_cleaned[i+1] for i, e in enumerate(none_cleaned) if i % 2 == 0 and i < len(none_cleaned)-1] + [none_cleaned[-1]]

#%% date_detector 

def formatter(final): # 자료형: final -> 텍스트 그대로, '갑1'꼴 
    y = [str(i) for i in range(10)]
    d_reg = [[y,y,y], [y,y],[y]]
    result = []
    for f in final:
        name = f[0]
        gap = f[0][0]
        num = reg_finder(name, d_reg)
        if num :
            num = reg_finder(name, d_reg)[0][0]
        result.append([name, gap+num])
    return result

def evidence_detector(page, text, reg_list = evid_reg):
    evidence = reg_finder(text, reg_list) 
    evidence = formatter(evidence)
    evid_list = []
    anno_list = []
    for evid in evidence:
        if evid != '':
            evid_list.append(evid[1])
            anno_list.append(page.searchFor(evid[0]))
    return evid_list, anno_list

def date_detector(setting: Setting, page, text, year_reg = year_reg, month_reg= month_reg, useless_token = useless_token):
    # 시작부터 쓸모 없는 데이터들 지우기
    if text[0:3] in useless_token:
        return [], []

    dd = re.finditer(year_reg, text)
    date_list = []
    anno_list = []
    for yyyy in dd:
        date = 0 #yyyymmdd 형태
        if int(yyyy.group()) > 2100 or int(yyyy.group()) < 1870: # 연도가 될 수 없는 것을 제외함
            continue 
        if  (text[yyyy.span()[0] - 3 : yyyy.span()[0] - 1] in ignore_date_w_space) or \
            (text[yyyy.span()[0] - 2 : yyyy.span()[0]]     in ignore_date_2_chars) or \
            (text[yyyy.span()[0] - 3 : yyyy.span()[0]]     in ignore_date_3_chars):
             # 판결문(헌법재판소), 법령이라면 또 패스  
            continue
         
        
        month_i = yyyy.span()[1] + 1 # 길면 7글자 더하면 됨 " 10. 30"
        month = text[month_i : month_i + 7]
        month_list = re.split(month_reg, month)
        day = False
        def isNum(s):
            try:
                int(s)
                return True
            except ValueError:
                return False
        for mm in month_list:
            if not isNum(mm):
                continue
            mm = int(mm)
            if mm > 0 : 
                if day : 
                    date += mm
                if not day: # 월이라면  
                    if mm >= 13: 
                        continue #13월보다 크니... 망한 것임 아니면
                    date += mm * 100
                    date += int(yyyy.group()) * 10000
                    day = True 
        if date != 0 and date < setting.date_no_later_than:
            date_list.append(date)
            logging.debug('{} 에서 찾은 {}'.format(date, text))
            h_text = text[yyyy.span()[0] : yyyy.span()[1] + 7] 
            anno_list.append(page.searchFor(h_text))
    return date_list, anno_list
