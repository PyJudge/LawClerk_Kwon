#%%
import fitz
import re, os, logging
import pandas as pd
import datetime
from PDF_parser.files_reader import files_parser
from PDF_parser.girok_list_parser import get_girok_evid_list
from output.pdf_output import combine_pdf
from output.excel_output import excel_output
from template.apply_template import apply_template
from PDF_parser.file_container import FilesContainer
from PDF_parser.girok_list_parser import get_girok_evid_list
from setting import Setting
#%%

#%%
# 사실상의 메인 함수 
def save_case(setting: Setting):

    # 1. Setting and FilesContainer init 
    PDF_dir = setting.PDF_dir
    files = FilesContainer(PDF_dir)
    flist = files.f_list

    if setting.add_to_existing_case: 
        # TODO 이미 정리한 파일을 불러, flist의 중복을 없애는 방법으로 프로그래밍
        pass
    # TODO 여기서 파일 개수를 gui에 보내야 함 

    # 2. pdf 파일 처리함 
    # TODO files_parser 안에서 gui에 진행 상황 보내야 함
    girok_dict, evid_dict = get_girok_evid_list(PDF_dir)
    logging.info("\n기록목록", girok_dict, evid_dict)
    evid_data, date_data = files_parser(files, setting)
    
    # 3. excel 내보내기
    excel_output(setting, files, girok_dict, evid_dict, evid_data, date_data)

    # 4. 병합 pdf 파일 생성
    if setting.is_saving_compilation:
        combine_pdf(setting, files) 

if __name__ == "__main__":
    save_case(Setting(os.path.join(os.getcwd())))


# %%
