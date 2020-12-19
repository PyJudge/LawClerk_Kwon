#%%
import fitz
import re, os
import pandas as pd
import datetime
from PDF_parser.file_reader import get_fname_in_dir
from PDF_parser.files_reader import files_parser, get_girok_evid_list
from PDF_parser.pdf_output import combine_pdf
from Intellimode.date_trim import delete_duplicate
from template.apply_template import apply_template
from Intellimode.make_abstract import make_abstract, score_date_data

def save_case_from_folder(
    PDF_dir, add_to_existing_case = False, is_saving_evid = False, is_saving_new_PDF = False):
    flist = get_fname_in_dir(PDF_dir)
    if add_to_existing_case: 
        # TODO 이미 정리한 파일을 불러, flist의 중복을 없애는 방법으로 프로그래밍
        pass
    # TODO 여기서 파일 개수를 gui에 보내야 함 
    save_case_from_flist(PDF_dir, flist, is_saving_evid, is_saving_new_PDF)

def save_case_from_flist(PDF_dir, flist, is_saving_evid, is_saving_new_PDF, intellimode_date = True):
    
    #pdf 파일 처리함 
    girok_dict, evid_dict = get_girok_evid_list(PDF_dir)
    print("\n기록목록", girok_dict, evid_dict)

    # TODO files_parser 안에서 gui에 진행 상황 보내야 함
    flist = [os.path.join(PDF_dir, fpath) for fpath in flist]
    evid_data, date_data = files_parser(flist, is_saving_annotated_PDF = False, evid_search = is_saving_evid)
    
    # 목록 파일 처리 함
    #for evid csv 내보내기
    # dd를 날짜별로 쪼가르기 > sorting > csv 형태
    
    #for date csv 내보내기 
    def get_girok_author(dname):
        try:
            return girok_dict[r[1]]
        except:
            return str(r[4]).zfill(3) # authur를 못 찾으면, doc_id를 반환
        
    csv_data = []
    for r in date_data:
        score = score_date_data(r, flist)
        for date in r[0]:
            csv_data.append([date, get_girok_author(r[1]), r[1], r[2] + 1, r[3], score]) #date, 작성자, 서면, 쪽수, 내용
    csv_data = sorted(csv_data, key = lambda x : (x[0], x[1], x[2], x[3]))

    abs = make_abstract(csv_data, flist)
    df = pd.DataFrame(abs, columns = ['날짜', '작성자/id', '서면', '쪽수', '내용', '점수'])
    df.drop(columns= '점수', inplace=True)
    df.to_excel(os.path.join(PDF_dir, '사실관계 정리표-요약.xlsx'), sheet_name = '날짜 정리', index = False)

    # TODO : intellimode 추가 pdf
    if intellimode_date:
        csv_data = delete_duplicate(csv_data)
    df = pd.DataFrame(csv_data, columns = ['날짜', '작성자/id', '서면', '쪽수', '내용', '점수'])
    df.drop(columns= '점수', inplace=True)
    df.to_excel(os.path.join(PDF_dir, '사실관계 정리표.xlsx'), sheet_name = '날짜 정리', index = False)

    # Apply Template
    apply_template(PDF_dir, '사실관계 정리표.xlsx')
    apply_template(PDF_dir, '사실관계 정리표-요약.xlsx')
    
    # TODO: 이미 정리한 pdf.xlsx가 있는지 보고, 있으면 뒤에 추가하며, 없으면 만들어서 추가함 
    # today = str(datetime.date.today()).replace('-', '') # 20201005 형태
    # flist_df = list(zip(flist, [today for i in range(len(flist))])) 
    # flist_df = pd.DataFrame(flist_df, columns= ['PDF 파일명', '정리 날짜']) # 오늘의 날짜를 모두 붙이는 것임 
    # flist_df.to_excel(os.path.join(PDF_dir, '이미 정리한 pdf.xlsx'), sheet_name = 'PDF', index= False)

    if is_saving_evid:
        csv_data = []
        for r in evid_data:
            for enum in r[0]:
                def evid_name(ename):
                    try:
                        return evid_dict[ename]
                    except:
                        return ' ' # 증거이름 못 찾으면 빈칸 출력함
                csv_data.append([enum, evid_name(enum), get_girok_author(r[1]), r[1], r[2] + 1, r[3]]) #date, 작성자, 서면, 쪽수, 내용
        csv_data = sorted(csv_data, key = lambda x : (x[0], x[2], x[3], x[4]))
    
        df = pd.DataFrame(csv_data, columns = ['번호', '증거명', '작성자/id', '서면', '쪽수', '내용']).sort_values(["번호"], ascending=[True])
        df.to_excel(os.path.join(PDF_dir, '증거 정리표.xlsx'), sheet_name = '날짜 정리', index = False)
    
    if is_saving_new_PDF:
        combine_pdf(flist) # 병합 생성

if __name__ == "__main__":
    save_case_from_folder(os.path.join(os.getcwd()))


# %%
