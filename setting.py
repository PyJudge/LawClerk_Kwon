import logging

class Setting:
    def __init__(self, \
        PDF_dir, add_to_existing_case = False, is_saving_evid = False, is_saving_compilation = False, is_annotating = False, intellimode_date = True, is_making_abstract_data= True, date_no_later_than = ''):
        self.PDF_dir = PDF_dir
        self.add_to_existing_case = add_to_existing_case
        self.is_saving_evid = is_saving_evid
        self.is_saving_compilation = is_saving_compilation
        self.is_annotating = is_annotating
        self.intellimode_date = intellimode_date
        self.is_making_abstract= is_making_abstract_data
        if date_no_later_than: 
            self.date_no_later_than = int(date_no_later_than)
        else:
            self.date_no_later_than =  99999999

    def log(self):
        logging.debug("""
        SETTING
            PDF_dir:                    {}
            add_to_existing_case:       {}
            is_saving_evid:             {}
            is_saving_compilation:          {}
            is_annotating:              {}
            intellimode_date:           {}
            is_making_abstract_data:    {}
        ----------------------------------------------------------------""".format(self.PDF_dir, self.add_to_existing_case,self.is_saving_evid, self.is_saving_compilation, self.is_annotating, self.intellimode_date, self.is_making_abstract))
