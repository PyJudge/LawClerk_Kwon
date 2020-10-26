import sys, os, time
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets \
    import (QApplication, QSlider, QLineEdit, QPushButton, \
        QVBoxLayout,QHBoxLayout, QWidget, QMainWindow, QProgressBar, QFileDialog, QLabel, QSpacerItem, QSizePolicy, QCheckBox) 
from PyQt5.QtCore import Qt

sys.path.append("./PDF_parser")
from PDF_parser.save_case_from_PDF import save_case_from_folder

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
        self.is_saving_new_PDF = False

    def init_ui(self):
        """[새로운 사건에 관한 정리 gui]

        """

        v_box = QVBoxLayout()
        v_box.addWidget(QLabel("""
        사건 1개의 pdf 파일을 폴더에 담고, (옵션을 선택한 후) 그 폴더를 선택해 주세요. 
        폴더 내 pdf 파일을 읽어들이고, 그중 날짜를 기재한 문장을 추출하여 시간 순서대로 정리합니다.
        '사실관계 정리표.xlsx'로 출력됩니다.
        """))

        h_box1 = QHBoxLayout()
        self.saving_PDF_chk = QCheckBox()
        self.saving_PDF_chk.setText("준비서면만 합친 pdf 만들기")
        h_box1.addWidget(self.saving_PDF_chk)
        v_box.addLayout(h_box1)

        h_box2 = QHBoxLayout()
        self.newcase_btn = QPushButton("폴더 열기")
        self.description_newcase = QLabel()
        h_box2.addWidget(self.description_newcase)
        h_box2.addWidget(self.newcase_btn)
        v_box.addLayout(h_box2)
        
        # v_box.addWidget(QLabel("[기존 사건]"))
        h_box3 = QHBoxLayout()
        # Progress bar 
        # h_box3.addWidget(QLabel("진행률"))
        # self.progress = QProgressBar()
        # h_box3.addWidget(self.progress)
        h_box3.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Preferred, QSizePolicy.Preferred))
        self.view_case_btn = QPushButton ("결과는 여기에서 열 수 있습니다.")
        self.view_case_btn.setEnabled(False)
        h_box3.addWidget(self.view_case_btn)
        v_box.addLayout(h_box3)

        self.newcase_btn.clicked.connect(self.make_newcase)
        self.saving_PDF_chk.stateChanged.connect(self.saving_PDF)
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
        self.setWindowTitle("컴연권 v.0.01")
        self.show()

    def make_newcase(self):
        self.path = QFileDialog.getExistingDirectory(self, "폴더 선택", os.getcwd(), QFileDialog.ShowDirsOnly)

        print(self.path)
        if self.path != "": 
            self.view_case_btn.setText("진행 중입니다.")
        # set progress bar 
         
        # call real function, 
            save_case_from_folder(self.path, is_saving_new_PDF = self.is_saving_new_PDF)

        # make current_case available 
            # self.progress.reset()
            self.current_case = "" # 나중에 current case를 여기다가 지정해주고 
            self.view_case_btn.setText("사실관계 정리표 열기")
            self.view_case_btn.setEnabled(True) # 버튼 활성화(다 하고 나서 해야 할듯 )
        # works well so far 

    def saving_PDF(self):
        self.is_saving_new_PDF = not self.is_saving_new_PDF
    
    def view_case(self):
        # for macOS
        if sys.platform == "darwin":
            os.system('open "{}"'.format(os.path.join(self.path, "사실관계 정리표.xlsx")))
        #for Windows(I dont know!!!!)
        else:
            os.system("{}".format(os.path.join(self.path, "사실관계 정리표.xlsx")))
            

app = QtWidgets.QApplication(sys.argv)
a_window = PDF2CaseWindow()
sys.exit(app.exec_())