import os 
import fitz

from PDF_parser.reg_list import fileevid_reg 
from PDF_parser.reg_checker import sent_f 

def get_fname_in_dir(dir):
    """
    Make a filelist 
    dir: path to the directory 
    """
    dir_file_list = sorted([fname for fname in os.listdir(dir) if fname[-3:] == 'pdf'])
    return dir_file_list


def onefilenameparser(fname, reg = fileevid_reg):
    """
    형태를 다음과 같이 만들어 줌 
    ['(19.06.17)답변서',
     '__을1_사전통지서',
     '__을2_의견서',
     '__을3_법제처 유권해석',
     '__서울중앙지방법원 2015 12 17 선고 2015노3758 판결']
    """

    _fname = fname[:-4]
    d = [str(i) for i in range(10)]
    reg = [['갑','을'], d]
    evid_f = sent_f(reg)

    a = ''
    if not evid_f(_fname): # 만약 갑, 을이 없다면, 즉 증거 아니라면
        a = _fname[_fname.index('('):_fname.index(')')+1]
    else: # 증거라면 
        a = '  '
        
    b = ''
    for f in _fname.split('.')[3:]:
        b += f
    
    return a + b


def onefilereader(fname, flist):
    """
    fname to file check
    """
    doc = fitz.open(fname)
    def fname_no_clutter(fname):
        try:
            fname.split('_')[1]
            return onefilenameparser(fname), flist.index(fname) + 1   # file 순서를 doc_id로 사용함 
        except:
            return fname[:-4], flist.index(fname) + 1 # file 순서를 doc_id로 사용함 
    f, doc_id = fname_no_clutter(fname)
    print(f)
    return doc, f, doc_id



