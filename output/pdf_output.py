import fitz, logging, os
from setting import Setting
from PDF_parser.file_container import FilesContainer

def combine_pdf(setting: Setting, files: FilesContainer):
    toc = []  
    page_now = 1
    doc = fitz.open()

    combine_path = setting.PDF_dir + '/날짜 형광펜' if setting.is_annotating else setting.PDF_dir
    combine_flist = os.listdir(combine_path)
    
    logging.info("START COMBINING -------------------")

    for to_combine in combine_flist:
        short_name = files.long_name_find(to_combine).short_name 
        logging.debug("in ", short_name)
        f_name = os.path.join(combine_path, to_combine)
        infile_doc = fitz.open(f_name)

        lastPage = len(infile_doc) - 1 
        doc.insertPDF(infile_doc, to_page= lastPage)
        logging.debug('len doc', len(doc))
        toc.append([1, short_name , page_now])
        page_now += len(infile_doc)
        infile_doc.close()
    doc.setToC(toc)
    doc.save(os.path.join(setting.PDF_dir, "기록 병합.pdf"), deflate=True, garbage=3)
    logging.info("COMBINING DONE -------------------")
