#%%
import sys, os, time, logging
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPixmap, QIntValidator
from PyQt5.QtWidgets \
    import (QApplication, QSlider, QLineEdit, QPushButton, \
        QVBoxLayout,QHBoxLayout, QWidget, QMainWindow, QProgressBar, QFileDialog, QLabel, QErrorMessage, QSpacerItem, QSizePolicy, QCheckBox, QMessageBox) 
from PyQt5.QtCore import Qt

sys.path.append("./PDF_parser")
from save_case import save_case, Setting 

"""
[TODO]
PDF2case
Case2CSV
Case2Excel

"""

class PDF2CaseWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui() 
        self.current_case = ""
        self.path = ""
        self.is_saving_compilation = True
        self.is_saving_evid = False
        self.is_annotating = False
        self.date_no_later_than  = 0
        self.is_making_evidpdf =False
    def init_ui(self):
        """[새로운 사건에 관한 정리 gui]

        """

        v_box = QVBoxLayout()
        v_box.addWidget(QLabel("""
        시간별 메모를 자동으로 작성하여 주는 프로그램입니다. 
        권원명 판사(helloden@scourt.go.kr)가 작성하였습니다. 
        사실 인정이나 메모 작성에 조금이나마 도움이 되면 좋겠습니다:) 

        사용법:  
            1) 사건의 준비서면 등의 pdf 파일을 폴더에 담고, (옵션을 선택한 후) 그 폴더를 선택해 주세요.
                가장 결과가 좋으려면, 가장 평범하게 내부용 기록뷰어를 이용하여 pdf 파일을 받으세요. 즉, 
                    가) 내부 기록뷰어를 사용하여 
                    나) 암호를 설정하지 않고
                    다) pdf를 1개의 파일로 병합하지 않은 채 다운로드해 주세요.
                        (준비서면과 증거가 섞여 있어도, 이 경우 증거를 자동으로 무시합니다)
                준비서면 등을 한 개의 pdf 파일로 병합한 경우에도 비교적 잘 작동합니다.
            2) 프로그램이 폴더 내 pdf 파일을 읽어들이고 그중 날짜를 기재한 문장을 추출하여 시간 순서대로 정리합니다.

        결과:
            1) '사실관계 정리표-서식 적용.xlsx', '사실관계 정리표-요약-서식 적용.xlsx'로 출력됩니다.
            2) '요약' 파일 한 날짜에 대하여 가장 관련성이 높은 문장 하나만을 적어 둔 것이고, 
                다른 파일은 그 날짜가 표시된 문장을 모두 정리한 것입니다.

        일러두기: 
            1) 시간이 좀 걸릴 수 있어요. 
                pdf의 어쩔 수 없는 한계(글씨 깨짐, 문장이 page를 넘어가는 경우, 텍스트를 읽을 수 없는 형식인 경우 등)가 분명히 있습니다.
            2) 기록 목록을 "목록.xlsx"라는 이름으로 저장하여 두면 조금 더 정확히 찾을 수 있긴 합니다. 
            3) 서식은 template 폴더 안에 있습니다(template.xlsx). 이미 저장된 양식을 적절히 수정하여 쓰셔도 됩니다.
        """))

        #h_box1 = QHBoxLayout()
        #self.saving_PDF_chk = QCheckBox()
        #self.saving_PDF_chk.setText("준비서면만 합친 pdf 만들기. 내부용 기록뷰어를 이용하여 여러 개 pdf로 기록을 받았을 때에만 가능합니다.")
        #h_box1.addWidget(self.saving_PDF_chk)
        #v_box.addLayout(h_box1)


        #h_box3 = QHBoxLayout()
        #self.highlight_chk = QCheckBox()
        #self.highlight_chk.setText("각각 날짜에 형광펜 칠한 파일 만들기")
        #h_box3.addWidget(self.highlight_chk)
        #v_box.addLayout(h_box3) # 날짜 형광펜 안 쓸거임

        #h_box7 = QHBoxLayout()
        #self.saving_evidpdf_chk = QCheckBox()
        #self.saving_evidpdf_chk.setText("(실험적 기능) 증거만 모은 pdf 만들기")
        #h_box7.addWidget(self.saving_evidpdf_chk)
        #v_box.addLayout(h_box7)

        h_box2 = QHBoxLayout()
        self.saving_evid_chk = QCheckBox()
        self.saving_evid_chk.setText("(실험적 기능) 서증 정리 만들기. 기록 목록(목록.xlsx)이 반드시 필요합니다.")
        h_box2.addWidget(self.saving_evid_chk)
        v_box.addLayout(h_box2)
       
        h_box6 = QHBoxLayout()
        self.date_no_later_than_edit = QLineEdit()
        self.date_no_later_than_edit.setMaxLength(8)
        self.date_no_later_than_edit.setValidator(QIntValidator())
        h_box6.addWidget(self.date_no_later_than_edit)
        h_box6.addWidget(QLabel("yyyyddmm 형태로 넣으면, 그 이후 날짜는 무시합니다(소 제기 날짜 등으로 하면 편해요!)"))
        v_box.addLayout(h_box6)

        h_box4 = QHBoxLayout()
        self.newcase_btn = QPushButton("시작! 폴더를 선택해 주세요.")
        self.description_newcase = QLabel()
        h_box4.addWidget(self.description_newcase)
        h_box4.addWidget(self.newcase_btn)
        v_box.addLayout(h_box4)
        
        # v_box.addWidget(QLabel("[기존 사건]"))
        h_box5 = QHBoxLayout()
        # Progress bar 
        # h_box3.addWidget(QLabel("진행률"))
        # self.progress = QProgressBar()
        # h_box3.addWidget(self.progress)
        h_box5.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Preferred, QSizePolicy.Preferred))
        self.view_case_btn = QPushButton ("결과는 여기에서 열 수 있습니다.")
        self.view_case_btn.setEnabled(False)
        h_box5.addWidget(self.view_case_btn)
        v_box.addLayout(h_box5)


        after_label = QLabel("-----실행 이후 다음과 같이 해 주세요-----")
        after_label.setAlignment(Qt.AlignCenter)
        v_box.addWidget(after_label)
        description_label= QLabel()
        description_label.setPixmap(QPixmap("./img/description.png"))
        description_label.setAlignment(Qt.AlignCenter)
        v_box.addWidget(description_label)

        self.newcase_btn.clicked.connect(self.make_newcase)
        #self.saving_PDF_chk.stateChanged.connect(self.saving_PDF)
        self.saving_evid_chk.stateChanged.connect(self.saving_evid)
        #self.saving_evidpdf_chk.stateChanged.connect(self.saving_evid_pdf)
        #self.highlight_chk.stateChanged.connect(self.annotating_new_pdf)
        self.view_case_btn.clicked.connect(self.view_case)
        """
        self.oldcase_folder_open = QFileDialog() # 새로 추가할 파일의 폴더
        self.oldcase_folder_btn = QPushButton("폴더 열기")
        self.oldcase_file_open = QFileDialog() # 이미 저장된 파일의 폴더 
        self.oldcase_file_btn = QPushButton("기존 정리파일 열기")
        self.description_oldcase = QLabel("사건 1개의 pdf 파일을 폴더에 담고, 그 폴더를 선택해 주세요. 폴더 내 pdf 파일을 시간 순서대로 정리합니다.")
        """
        """
        self.b2 = QPushButton("print")
        self.s1 = QSlider(Qt.Horizontal)
        self.s1.setMinimum(1)
        self.s1.setMaximum(99)
        self.s1.setValue(25)
        self.s1.setTickInterval(10)
        self.s1.setTickPosition(QSlider.TicksBelow)

        v_box = QVBoxLayout()
        v_box.addWidget(self.le)
        v_box.addWidget(self.b1)
        v_box.addWidget(self.b2)
        v_box.addWidget(self.s1)
        """

        self.setLayout(v_box) 
        self.setWindowTitle("컴연권 v.0.3 약식")
        self.show()

    def make_newcase(self):
        self.path = QFileDialog.getExistingDirectory(self, "폴더 선택", os.getcwd(), QFileDialog.ShowDirsOnly)

        print(self.path)

        
        is_having_PDF = False
        if self.path:
            for f_name in os.listdir(self.path):
                if f_name[-3:] == 'pdf':
                    is_having_PDF = True
        
        if is_having_PDF: 
            self.view_case_btn.setText("진행 중입니다.")
            # TODO: 기존 케이스에 추가, set progress bar  
            date_limit = self.date_no_later_than_edit.text()
            # call real function,
#            self.setting = Setting(self.path, is_saving_evid= self.is_saving_evid, is_saving_compilation = self.is_saving_compilation, is_annotating = self.is_annotating, date_no_later_than = date_limit) 
            self.setting = Setting(self.path, is_saving_evid= self.is_saving_evid, is_saving_compilation = True, is_annotating = True, date_no_later_than = date_limit)  # pdf에 하이라이트 사용 안할래, 항상 준비서면 합본도 만들래.
            is_date_data_found = save_case(self.setting)
        # make current_case available 
            # self.progress.reset()
            self.current_case = "" # 나중에 current case를 여기다가 지정해주고 
            msg = QMessageBox()
            if is_date_data_found: 
                self.view_case_btn.setText("완료! 사실관계 정리표(요약) 열기")
                self.view_case_btn.setEnabled(True) # 버튼 활성화(다 하고 나서 해야 할듯 )
                msg.setText('작업 완료!')
                msg.exec_() 
            else:
                self.view_case_btn.setText("유효한 날짜 정보가 없어 작업을 완료하지 못하였습니다. 스캔된 PDF 파일인지 확인해 주세요.")
                msg.setText('유효한 날짜 정보가 없어 작업을 완료하지 못하였습니다. 스캔된 PDF 파일인지 확인해 주세요.')
                msg.exec_()     

        else:
            msg = QMessageBox()
            msg.setText('PDF가 있는 폴더를 선택해 주세요.')
            msg.exec_()     
        
    def saving_PDF(self):
        self.is_saving_compilation = not self.is_saving_compilation

    def saving_evid(self):
        self.is_saving_evid = not self.is_saving_evid

    def saving_evid_pdf(self):
        self.is_making_evidpdf = not self.is_making_evidpdf
        print(self.is_making_evidpdf)
    def annotating_new_pdf(self):
        self.is_annotating = not self.is_annotating
        # if self.is_saving_compilation:
        #     self.is_annotating = not self.is_annotating
        # else:
        #     msg = QMessageBox()
        #     msg.setText("날짜 형광펜은 '준비서면만 합친 PDF 만들기'를 선택할 때에만 가능합니다")                        
    def view_case(self):
        # for macOS
        if sys.platform == "darwin":
            os.system('open "{}"'.format(os.path.join(self.setting.PDF_dir, "사실관계 정리표-서식 적용.xlsx")))
        #for Windows(I dont know!!!!)
        else:
            os.startfile(r"{}".format(os.path.join(self.setting.PDF_dir, "사실관계 정리표-요약-서식 적용.xlsx")))


logger = logging.getLogger()            
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# # log를 파일에 출력 이해가 안 되게;;; 안 됨;;; 거의 로그 출력이 안 됨....왜일까-_ㅠㅠㅠㅠ
# file_handler = logging.FileHandler('email_this.log')
# file_handler.setFormatter(formatter)
# file_handler.setLevel(logging.INFO)
# logger.addHandler(file_handler)

app = QtWidgets.QApplication(sys.argv)
a_window = PDF2CaseWindow()
# file_handler.close()
sys.exit(app.exec_())

