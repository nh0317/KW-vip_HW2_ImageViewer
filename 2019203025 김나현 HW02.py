import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import qimage2ndarray
import numpy as np

#Qt Designer에서 편집한 ui파일을 블러와 클래스 생성
basic_ui = uic.loadUiType("uistyle.ui")[0]

class WindowClass(QMainWindow, basic_ui) :
    qPixmapVar = None
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        #load 버튼 클릭시 showimage함수가 작동하도록 연결
        self.pushButton.clicked.connect(self.showimage)
        #flip 버튼 클릭시 flipimage함수가 작동하도록 연결
        self.pushButton_2.clicked.connect(self.flipimage)

    #이미지를 출력하는 showimage함수
    def showimage (self):
        #폴더에서 사진을 선택하고 선택된 사진의 경로 저장
        file = QFileDialog.getOpenFileName(self, "Open File", ".")
        filepath = file[0]

        #Qixmap 객체를 생성하여 Label에 QPixmap 객체 표시
        self.qPixmapVar = QPixmap()
        self.qPixmapVar.load(filepath)
        self.qPixmapVar = self.qPixmapVar.scaled(411,301)
        self.label.setPixmap(self.qPixmapVar)

    #이미지를 상하로 반전하는 flipimage함수
    def flipimage(self):
        #이미지 파일이 없을 경우 Label에 문자열 출력
        if self.qPixmapVar is None :
            QMessageBox.information(self, "Restart", "Please Load Image First.")
            return

        #생성된 Qixmap이미지를 QImage로 변환하여 변수에 저장
        image = QImage(self.qPixmapVar)

        #QImage를 numpy로 변환
        image_array = qimage2ndarray.rgb_view(image)

        #변환된 numpy를 상하로 뒤집고 QImage로 다시 변환
        image_array = np.flip(image_array, 0)
        image = qimage2ndarray.array2qimage(image_array, normalize=False)

        #QImage를 QPixmap으로 변환하여 Label에 표시
        self.qPixmapVar = QPixmap.fromImage(image)
        self.label.setPixmap(self.qPixmapVar)

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()