from file_reader import onefilereader
from reg_list import split_reg, evid_reg, year_reg
from sentence_parser import sent_splitter, evidence_detector, date_detector
import os 
import pandas as pd

def files_parser(flist, is_saving_annotated_PDF= False, evid_search= False):
    print(flist)
    evid_result = []
    date_result = []
    for fname in flist:
        doc, f, doc_id = onefilereader(fname, flist) #reading 
        for pnum, page in enumerate(doc): # num 은 페이지 number, 다만 0부터 시작하는 점에 유의할 것  
            data = page.getText().replace('\xa0',' ').replace('\n', '')
            data = " ".join(data.split())
            splitted = sent_splitter(data, split_reg) # page 안에서 문장으로 나누기 
            for sent in splitted: # page 안에서 문장 마다 찾기 
                #For evid
                print("sent", sent)
                if evid_search:
                    evids, annos = evidence_detector(page, sent, evid_reg)
                    if evids: # date가 비지 않았다면, 즉 date가 찾아졌다면
                        print(evids)
                        evid_result.append([list(set(evids)), f, pnum, sent, doc_id])
                        for anno in annos:
                            page.addHighlightAnnot(anno)

                #For date
                dates, annos = date_detector(page, sent, year_reg) # 
                if dates: # date가 비지 않았다면, 즉 date가 찾아졌다면
                    print(dates)
                    date_result.append([list(set(dates)), f, pnum, sent, doc_id])
                    for anno in annos:
                        page.addHighlightAnnot(anno)  
        print(doc, f)
        if is_saving_annotated_PDF:
            output_fname = f + "_" + str(doc_id).zfill(3) 
            doc.save(output_fname + ".pdf")        
    return evid_result, date_result
#splitter = SentenceSplitter(API.OKT)

#%% 제출자 합병
def get_girok_evid_list(PDF_dir): 
    """
    파일 중 목록.xlsx나 xls를 읽어서 기록 목록으로 만들고, 
    없으면, 목록으로 아무것도 사용하지 않음, 
    즉 기록 저자로 doc_id를 쓰고(만약 파일 이름 생긴 게 이상하다면, 그냥 서류이름이 될 것임 ), 
    증거이름으로 아무것도 사용하지 않음 
    반환형 : girok_dict, evid_dict 
    
    """
    flist = os.listdir(PDF_dir)
    if '목록.xlsx' in flist:
        fname = os.path.join(PDF_dir, '목록.xlsx')
    elif '목록.xls' in flist:
        fname = os.path.join(PDF_dir, '목록.xls')
    else:
        return {}, {}
    girok_list = pd.read_excel(fname, header = 0)

    try:
        evid_list = pd.read_excel(fname, header = 0, sheet_name = "서증등목록 ") # 원래 생긴 게 스페이스 포함임.  신 버젼은 모르겠음 
        girok_list['문건명'] = pd.Series(['(' + t[2:] + ')' + d for t, d in zip(girok_list['기준일자'], girok_list['문건명'])])    
        def is_dup(t):
            girok_temp = list(girok_list['문건명'])    
            groupby = list(set(girok_temp))
            dup_result = dict()
            for ip in groupby:
                dup_result[ip]=girok_temp.count(ip)   
            return dup_result[t] != 1
        
        girok_dict = {t:d for t, d in zip(girok_list['문건명'], girok_list['제출자']) if not is_dup(t)}
        evid_dict = {t:d for t, d in zip(evid_list['번호'], evid_list['서증명'])}
        print(girok_dict, evid_dict)
    except:
        evid_dict = {}
    return girok_dict, evid_dict 
    