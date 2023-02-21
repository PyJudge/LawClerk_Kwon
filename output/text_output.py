# excel_output을 대체하는 파일임 
# output as TXT file,  
# logging TXT too 
#%%
from output.Intellimode.make_abstract import make_abstract, score_date_data
from output.Intellimode.date_trim import delete_duplicate
from setting import Setting
import re, os, logging
import pandas as pd
from PDF_parser.file_container import FilesContainer
from template.apply_template import apply_template
 #%%

 
