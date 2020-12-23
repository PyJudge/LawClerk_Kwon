import sys, os, time
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPixmap
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
        self.is_saving_evid = False

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
                그러나 준비서면 등을 한 개의 pdf 파일로 병합한 경우에도 비교적 잘 작동합니다.
            2) 프로그램이 폴더 내 pdf 파일을 읽어들이고 그중 날짜를 기재한 문장을 추출하여 시간 순서대로 정리합니다.

        결과:
            1) '사실관계 정리표-서식 적용.xlsx', '사실관계 정리표-요약-서식 적용.xlsx'로 출력됩니다.
            2) '요약' 파일 한 날짜에 대하여 가장 관련성이 높은 문장 하나만을 적어 둔 것이고, 
                다른 파일은 그 날짜가 표시된 문장을 모두 정리한 것입니다.

        일러두기: 
            1) 시간이 좀 걸릴 수 있어요. 
                그리고 pdf의 어쩔 수 없는 한계(글씨 깨짐, 문장이 page를 넘어가는 경우 등)가 분명히 있습니다.
            2) 기록 목록을 "목록.xlsx"라는 이름으로 저장하여 두면 조금 더 정확히 찾을 수 있긴 합니다. 
            3) 서식은 template 폴더 안에 있습니다(template.xlsx). 이미 저장된 양식을 적절히 수정하여 쓰셔도 됩니다.
            4) 저는 보통 소 제기일 이후의 사건은 지워버리고 잘 안 봅니다.
        """))

        h_box1 = QHBoxLayout()
        self.saving_PDF_chk = QCheckBox()
        self.saving_PDF_chk.setText("준비서면만 합친 pdf 만들기. 내부용 기록뷰어를 이용하여 여러 개 pdf로 기록을 받았을 때에만 가능합니다.")
        h_box1.addWidget(self.saving_PDF_chk)
        v_box.addLayout(h_box1)

        h_box2 = QHBoxLayout()
        self.saving_evid_chk = QCheckBox()
        self.saving_evid_chk.setText("서증 정리 만들기. 기록 목록(목록.xlsx)이 반드시 필요합니다. 5분 이상 걸릴 수도 있고 품질이 완벽하지 않습니다.")
        h_box2.addWidget(self.saving_evid_chk)
        v_box.addLayout(h_box2)

        h_box3 = QHBoxLayout()
        self.newcase_btn = QPushButton("폴더 열기")
        self.description_newcase = QLabel()
        h_box3.addWidget(self.description_newcase)
        h_box3.addWidget(self.newcase_btn)
        v_box.addLayout(h_box3)
        
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


        after_label = QLabel("-----실행 이후 다음과 같이 해 주세요-----")
        after_label.setAlignment(Qt.AlignCenter)
        v_box.addWidget(after_label)
        description_label= QLabel()
        description_label.setPixmap(QPixmap("./img/description.png"))
        description_label.setAlignment(Qt.AlignCenter)
        v_box.addWidget(description_label)

        self.newcase_btn.clicked.connect(self.make_newcase)
        self.saving_PDF_chk.stateChanged.connect(self.saving_PDF)
        self.saving_evid_chk.stateChanged.connect(self.saving_evid)
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
        self.setWindowTitle("컴연권 v.0.21")
        self.show()

    def make_newcase(self):
        self.path = QFileDialog.getExistingDirectory(self, "폴더 선택", os.getcwd(), QFileDialog.ShowDirsOnly)

        print(self.path)
        if self.path != "": 
            self.view_case_btn.setText("진행 중입니다.")
        # set progress bar 

        if self.path != "": 
        # call real function, 
            save_case_from_folder(
                self.path, is_saving_evid= self.is_saving_evid, is_saving_new_PDF = self.is_saving_new_PDF)

        # make current_case available 
            # self.progress.reset()
            self.current_case = "" # 나중에 current case를 여기다가 지정해주고 
            self.view_case_btn.setText("완료! 사실관계 정리표(요약) 열기")
            self.view_case_btn.setEnabled(True) # 버튼 활성화(다 하고 나서 해야 할듯 )
        # works well so far 

    def saving_PDF(self):
        self.is_saving_new_PDF = not self.is_saving_new_PDF

    def saving_evid(self):
        self.is_saving_evid = not self.is_saving_evid

    def view_case(self):
        # for macOS
        if sys.platform == "darwin":
            os.system('open "{}"'.format(os.path.join(self.path, "사실관계 정리표-서식 적용.xlsx")))
        #for Windows(I dont know!!!!)
        else:
            os.startfile(r"{}".format(os.path.join(self.path, "사실관계 정리표-요약-서식 적용.xlsx")))
            

app = QtWidgets.QApplication(sys.argv)
a_window = PDF2CaseWindow()
sys.exit(app.exec_())