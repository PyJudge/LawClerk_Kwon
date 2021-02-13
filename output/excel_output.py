    # 목록 파일 처리 함
    #for evid csv 내보내기
    # dd를 날짜별로 쪼가르기 > sorting > csv 형태
from output.Intellimode.make_abstract import make_abstract, score_date_data
from output.Intellimode.date_trim import delete_duplicate
from setting import Setting
import re, os, logging
import pandas as pd
from PDF_parser.file_container import FilesContainer
from template.apply_template import apply_template


def excel_output(setting:Setting, files: FilesContainer, girok_dict, evid_dict, evid_data, date_data):
    logging.info("STARTING OUTPUTTING EXCEL-------------------------------")

    PDF_dir = setting.PDF_dir
    flist = files.f_list

    # get_girok_author refactored. 중요한 변화이므로 잘 안 되면 다시 고칠 것 
    #def get_girok_author(dname):
    #    try:
    #        return girok_dict[ele[1]]
    #    except:
    #        return str(ele[4]).zfill(3) # authur를 못 찾으면, doc_id를 반환 

    # date excel 내보내기 
    csv_data = []
    for ele in date_data:
        authur = girok_dict[ele[1]] if ele[1] in girok_dict.keys() else str(ele[4]).zfill(3) 
        logging.info("PROCESSING DOCUMENT", ele[1], "AUTHOR IS", authur) 
        score = score_date_data(ele, files)
        for date in ele[0]:
            csv_data.append([date, authur, ele[1], ele[2] + 1, ele[3], score]) #date, 작성자, 서면, 쪽수, 내용
    csv_data = sorted(csv_data, key = lambda x : (x[0], x[1], x[2], x[3]))
    logging.info("DATE DATA PROCESSED -----------------------------------------")

    if setting.is_making_abstract:
        abs = make_abstract(csv_data, flist)
        df = pd.DataFrame(abs, columns = ['날짜', '작성자/id', '서면', '쪽수', '내용', '점수'])
        df.drop(columns= '점수', inplace=True)
        df.to_excel(os.path.join(PDF_dir, '사실관계 정리표-요약.xlsx'), sheet_name = '날짜 정리', index = False)

    if setting.intellimode_date:
        csv_data = delete_duplicate(csv_data)

    logging.info("MAKING FILES AND FINALIZING DATE DATA-----------------------------------------")
    df = pd.DataFrame(csv_data, columns = ['날짜', '작성자/id', '서면', '쪽수', '내용', '점수'])
    df.drop(columns= '점수', inplace=True)
    df.to_excel(os.path.join(PDF_dir, '사실관계 정리표.xlsx'), sheet_name = '날짜 정리', index = False)

    # Apply Template
    apply_template(PDF_dir, '사실관계 정리표.xlsx')
    apply_template(PDF_dir, '사실관계 정리표-요약.xlsx')
    os.remove(os.path.join(PDF_dir, "사실관계 정리표.xlsx"))
    os.remove(os.path.join(PDF_dir,"사실관계 정리표-요약.xlsx"))
    # TODO: 이미 정리한 pdf.xlsx가 있는지 보고, 있으면 뒤에 추가하며, 없으면 만들어서 추가함 
    # today = str(datetime.date.today()).replace('-', '') # 20201005 형태
    # flist_df = list(zip(flist, [today for i in range(len(flist))])) 
    # flist_df = pd.DataFrame(flist_df, columns= ['PDF 파일명', '정리 날짜']) # 오늘의 날짜를 모두 붙이는 것임 
    # flist_df.to_excel(os.path.join(PDF_dir, '이미 정리한 pdf.xlsx'), sheet_name = 'PDF', index= False)

    # evid excel 내보내기 
    logging.info("EVIDENCE DATA-----------------------------------------")
    if setting.is_saving_evid:
        csv_data = []
        for ele in evid_data:
            authur = get_girok_author(ele[1])
            for enum in ele[0]:
                def evid_name(ename):
                    try:
                        return evid_dict[ename]
                    except:
                        return ' ' # 증거이름 못 찾으면 빈칸 출력함
                csv_data.append([enum, evid_name(enum), authur, ele[1], ele[2] + 1, ele[3]]) #date, 작성자, 서면, 쪽수, 내용
        csv_data = sorted(csv_data, key = lambda x : (x[0], x[2], x[3], x[4]))
    
        df = pd.DataFrame(csv_data, columns = ['번호', '증거명', '작성자/id', '서면', '쪽수', '내용']).sort_values(["번호"], ascending=[True])
        df.to_excel(os.path.join(PDF_dir, '증거 정리표.xlsx'), sheet_name = '날짜 정리', index = False)
