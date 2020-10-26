import fitz
from PDF_parser.file_reader import onefilereader

def combine_pdf(flist):
    toc = []  
    page_now = 1
    doc = fitz.open()
    for f in flist:
        infile, fname, _ = onefilereader(f, flist)
        print(fname)
        lastPage = len(infile) - 1 
        doc.insertPDF(infile, to_page= lastPage)
        print('len doc', len(doc))
        toc.append([1, fname + '_', page_now])
        page_now += len(infile)
        infile.close()
    doc.setToC(toc)
    doc.save("기록 병합.pdf", deflate=True, garbage=3)