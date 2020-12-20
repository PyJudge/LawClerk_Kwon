"""
    요약 만들기 
    기준 1: 날짜의 수가 적은 것이 더 우월하다. 
    기준 2: 날짜 수가 동일하다면, 표준편차가 적은 놈이 우월하다. 
    기준 3: 표준편차가 동일하다면, 증거가 적시된 놈이 우월하다. 
    기준 4: 다 동일하다면 여러 번 같은 문장 나온 놈이 우월하다. 
"""
#%%
import statistics
from PDF_parser.reg_checker import reg_finder 
from PDF_parser.reg_list import evid_reg

def score_date_data(sent_chunk, flist):
    dates = sent_chunk[0] # [20200110, 20021120]
    file_name = sent_chunk[1]
    page = sent_chunk[2]
    sent = sent_chunk[3]  # '사법연수원은 2020. 1. 10. 원명이가 안 오는 변화를 맞이하여..

    if (len(sent) < 20) or (len(sent) > 400) :
        return 0  # It is useless if it is too short

    num_dates = len(dates)
    if num_dates > 4:
        return 0 # It is useless if there are too many dates
    elif num_dates > 1: 
        var = int(statistics.stdev(dates)/1000)
    else: 
        var = 0
    flag_evid = 1 if reg_finder(sent, evid_reg) != [] else 0 
    occured_in = (flist.index(file_name)+1) * 10000 + page  # 각 서면의 page가 9999 넘지 않는다는 가정... 파일 개수는 9999개 넘지 않고 

    score =  ((101 - num_dates) * 10000000000000000) + (var * 1000000000) + (flag_evid * 100000000) + occured_in
    return score
#%%
def make_abstract(csv_data, flist):
    abstract_data = []
    score_max = 0
    date_old = csv_data[0][0] # 첫날 
    sentence_best_old = ''
    best_sent_chunk = []
    print("\n\n\n 요약본 작업 시작함", date_old)

    for n, sent_chunk in enumerate(csv_data): 
        date_new = sent_chunk[0]
        score_new = sent_chunk[5]
        sentence_new = sent_chunk[4]
        if date_old != date_new: # 날짜가 바뀌면, 기존 데이터를 append 하고, 그 부분 지움
            print("날짜 바뀜")
            if best_sent_chunk != []:
                sentence_best_new = best_sent_chunk[4]
                if sentence_best_old == sentence_best_new:
                    best_sent_chunk[4] = "상동" 
                    # 중복을 없애기 위함. 그리고 다음 문장을 위해 sentence_best_old를 바꾸지 않음. 상동 2개 이상일 수도 있음
                else:
                    sentence_best_old = sentence_best_new                    
                abstract_data.append(best_sent_chunk)
            
            best_sent_chunk = []
            score_max = 0

        if score_new > score_max: 
            score_max = score_new  
            best_sent_chunk = sent_chunk
            print("신기록", print(best_sent_chunk))

        if n == len(csv_data): 
            abstract_data.append(best_sent_chunk) # 마지막 날에는 털고 갑니다. 
        date_old = date_new

    return abstract_data
