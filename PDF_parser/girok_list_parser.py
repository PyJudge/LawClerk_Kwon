import os, logging
import pandas as pd

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
        logging.debug(girok_dict, evid_dict)
    except:
        evid_dict = {}
    return girok_dict, evid_dict 
    