#%%
import os
import fitz
#from PDF_parser.reg_list import fileevid_reg # for dist 
#from PDF_parser.reg_checker import sent_f 
from reg_list import file_evid_reg, file_to_ignore_reg # FOR TEST
from reg_checker import reg_finder
#%%
class OneFileContainer:
    """
    CONTAINER DETAIL:
        doc_id, 
        dir_name, 
        f_name, 
        short_name, 
        is_brief(boolean), not to do any heavy processing with fitz
        fitz.doc(only if is_brief)
    """
    def __init__(self, doc_id, dir_name, f_name):
        self.doc_id = doc_id
        self.dir_name = dir_name
        self.f_name = f_name
        self.short_name, \
            self.is_brief, \
                self.fitz_doc = self.filenameparser_(self.f_name)

    def filenameparser_(self, f_name):
        """
        fname to file check
        """
        def trim_f_name_(fname, reg = file_evid_reg):
            """
            형태를 다음과 같이 만들어 줌 
            ['(19.06.17)답변서',
            '__을1_사전통지서',
            '__을2_의견서',
            '__을3_법제처 유권해석',
            '__서울중앙지방법원 2015 12 17 선고 2015노3758 판결']
            """
            _fname = fname[:-4] # WITHOUT .PDF
            is_brief = True # UNLESS PROVEN EVIDENCE 
            try : 
                _fname = _fname.split('_', 1)[1] # TRY TO CATCH A FILE DOWNLOADED IN THE COURT                 
                evid_f = reg_finder(_fname, reg)
                print("-----------------------------------")
                print(evid_f)
                if not evid_f[0]: # 만약 갑, 을이 없다면, 즉 증거 아니라면
                    a = _fname[_fname.index('(') : _fname.index(')') + 1]
                else: # 증거라면 
                    a = '  '
                    is_brief = False

                b = ''
                for f in _fname.split('.')[3:]:
                    b += f

                return a + b, is_brief

            except:
                return _fname, is_brief # JUST PDF NAME 

        short_name, is_brief = trim_f_name_(f_name)
        fitz_doc = fitz.open(f_name) if is_brief else None 
        return short_name, is_brief, fitz_doc 


class FilesContainer:
    def __init__(self, dir_name):
        self.dir_name = dir_name
        self.f_list = sorted(
            [fname for fname in os.listdir(dir) \
                if fname[-3:] == 'pdf' and not reg_finder(fname, file_to_ignore_reg)]) 
                # pdf 파일만 골라서 넣음, file_to_ignore_reg에 있는 것은 생략함  
        self.doc_id_dict= {self.f_list.index(fname) : fname \
                            for fname in self. f_list} # (file sequence as doc id) : (fname)  
        
    def each(self, doc_id):
        f_name = self.doc_id_dict[doc_id]
        return OneFileContainer(doc_id, self.dir_name, f_name)
# %%
# test code 
def test():
    dir = os.getcwd()
    t = FilesContainer(dir)
    t272 = t.each(272) #갑 55호증 
    for i in t.doc_id_dict.keys():
        each = t.each(i)
        print( each.f_name)
        print(each.short_name, each.is_brief)
        input()
test()     
# %
# %%
