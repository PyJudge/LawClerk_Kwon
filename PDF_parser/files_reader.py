from regex.reg_list import split_reg, evid_reg, year_reg
from PDF_parser.sentence_parser import sent_splitter, evidence_detector, date_detector
from PDF_parser.file_container import FilesContainer
from setting import Setting
import os, logging
import pandas as pd


def files_parser(files: FilesContainer, setting : Setting):
    doc_id_dict = files.doc_id_dict
    evid_result = []
    date_result = []
    
    for doc_id in doc_id_dict.keys():
        file = files.each(doc_id)

        f_name = file.short_name
        doc = file.fitz_doc
        logging.info("STARTING file parsing\n------------- {}".format( file.f_name))
        if not file.is_brief: # 증거는 읽지 않음 
            continue

        for pnum, page in enumerate(doc): # num 은 페이지 number, 다만 0부터 시작하는 점에 유의할 것  
            data = page.getText().replace('\xa0',' ').replace('\n', '')
            data = " ".join(data.split())
            splitted = sent_splitter(data, split_reg) # page 안에서 문장으로 나누기 

            for sent in splitted: # page 안에서 문장 마다 찾기 
                #For evid
                logging.debug("sent {}".format(sent))
                if setting.is_saving_evid:
                    evids, annos = evidence_detector(page, sent, evid_reg)
                    if evids: # date가 비지 않았다면, 즉 date가 찾아졌다면
                        logging.debug(evids)
                        evid_result.append([list(set(evids)), f_name, pnum, sent, doc_id])
                        if setting.is_annotating:
                            for anno in annos:
                                page.addHighlightAnnot(anno)

                #For date
                dates, annos = date_detector(setting, page, sent, year_reg) # 
                if dates: # date가 비지 않았다면, 즉 date가 찾아졌다면
                    logging.debug(dates)
                    date_result.append([list(set(dates)), f_name, pnum, sent, doc_id])
                    if setting.is_annotating:
                        for anno in annos:
                            page.addHighlightAnnot(anno)  

        if setting.is_annotating:
            anno_path = file.dir_name + '/날짜 형광펜'
            if not os.path.isdir(anno_path):
                os.mkdir(anno_path)
            output_fname = os.path.join(anno_path, file.f_name) 
            doc.save(output_fname)        

    return evid_result, date_result
#splitter = SentenceSplitter(API.OKT)

#%% 제출자 합병
