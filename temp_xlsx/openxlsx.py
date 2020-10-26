#%%
from openpyxl import load_workbook
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows
from itertools import chain
#%%
src = load_workbook("사실관계 정리표.xlsx")
form = load_workbook("저장 폼.xlsx")
src_ws = src.active
form_ws = form.active

"""
for i, row in enumerate(src_ws.iter_cols()):
    for j, cell in enumerate(row): 
        if cell.value in ['번호', '증거명', '작성자/id', '서면', '쪽수', '내용']:
            form_ws[i, j]

"""

# %%
for i, row in enumerate(src_ws.iter_cols(min_row = 2)): # omit first row 
    for j, cell in enumerate(row):
        # print(cell.value)

        # where to start
        position = [i+1, j+3]
        print(*position, n_cell(*position), form_ws[n_cell(*position)].value)
        form_ws[n_cell(*position)] = cell.value

form.save("일시.xlsx")

# %%
# 11 > A1
# 56 > E6
def n_cell(i: int, j : int ) -> str:
    return chr(i + 64) + str(j)
# %%

# %%
# 새로운 인텔리 버젼 ! 
# 1단계 sentence를 발라낸다 
# 2단계 sentence 중, 증거가 있는 것을 찾는다 
# 2-1단계  
# 2-1단계 증거가 많은 것을 우선한다 
# 
# 
raw_data = [
    [1, 2, 3, 4, 5, 6,], [2, 3, 6, 7], [4, 5, 8], [1, 6, 7, 9], [3, 6], [2, 6, 9], 
    [5, 1, 2, 3, 9], [3, 6, 8]]

# %%
remaining = set([raw for raw in raw_data])
#%%
remaining_elements = set([remaining - for ])
# %%
