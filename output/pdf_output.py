import fitz, logging, os
from setting import Setting
from PDF_parser.file_container import FilesContainer

def combine_pdf(setting: Setting, files: FilesContainer):
    toc = []  
    page_now = 1
    doc = fitz.open()

    combine_path = setting.PDF_dir + '/날짜 형광펜' if setting.is_annotating else setting.PDF_dir
    # skip directories
    combine_flist = []
    for fname in os.listdir(combine_path):
        path = os.path.join(combine_path, fname)
        if os.path.isdir(path):
            continue
        elif fname == "기록 병합.pdf":
            continue
        else:
            combine_flist.append(fname)

    logging.info("START COMBINING -------------------")
    #귀찮아서 코딩 한 거 베끼기 
    f_list = []
    for fname in os.listdir(combine_path):
        if fname[-3:] == 'pdf':
            f_list.append(fname)    

    combine_flist = sorted(f_list) # TODO 현재 형광펜 기능을 안 할때 준비서면 이외의 서면도 같이 합쳐진다는 문제가 있음 
    for to_combine in combine_flist:
        short_name = files.long_name_find(to_combine).short_name 
        logging.debug("in {}".format( short_name))
        f_name = os.path.join(combine_path, to_combine)
        infile_doc = fitz.open(f_name)

        lastPage = len(infile_doc) - 1 
        doc.insertPDF(infile_doc, to_page= lastPage)
        logging.debug('len doc {}'.format(len(doc)))
        toc.append([1, short_name , page_now])
        page_now += len(infile_doc)
        infile_doc.close()
    doc.setToC(toc)
    doc.save(os.path.join(setting.PDF_dir, "기록 병합.pdf"), deflate=True, garbage=3)
    logging.info("COMBINING DONE -------------------")
