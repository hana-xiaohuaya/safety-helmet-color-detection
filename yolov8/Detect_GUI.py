import sys
import cv2
from ultralytics import YOLO
from PyQt5.QtCore import Qt
from PyQt5.QtCore import Qt, QTimer

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import ui_img.detect_images_rc
import os
from tqdm import tqdm   # 进度条
import shutil


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setWindowTitle("基于YOLOv8的检测演示软件V1.0")
        self.resize(1500, 1000)
        self.setStyleSheet("QWidget#centralwidget{background-image: url(:/detect_background/detect.JPG);}")
        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")

        # 模型选择        
        self.btn_selet_model = QtWidgets.QPushButton(self.centralwidget)
        self.btn_selet_model.setGeometry(QtCore.QRect(70, 810, 70, 70))
        self.btn_selet_model.setStyleSheet("border-image: url(:/detect_button_background/upload.png);")
        self.btn_selet_model.setText("")
        self.btn_selet_model.setObjectName("btn_selet_model")
        self.btn_selet_model.clicked.connect(self.seletModels)

        # 选择图像进行检测
        self.btn_detect_img = QtWidgets.QPushButton(self.centralwidget)
        self.btn_detect_img.setGeometry(QtCore.QRect(390, 810, 70, 70))
        self.btn_detect_img.setStyleSheet("border-image: url(:/detect_button_background/images.png);")
        self.btn_detect_img.setText("")
        self.btn_detect_img.setObjectName("btn_detect_img")
        self.btn_detect_img.clicked.connect(self.openImage)
        
        # 保存结果图像
        self.btn_save_img = QtWidgets.QPushButton(self.centralwidget)
        self.btn_save_img.setGeometry(QtCore.QRect(730, 810, 70, 70))
        self.btn_save_img.setStyleSheet("border-image: url(:/detect_button_background/save.png);")
        self.btn_save_img.setText("")
        self.btn_save_img.setObjectName("btn_save_img")
        self.btn_save_img.clicked.connect(self.saveImage)

        # 清除结果图像
        self.btn_clear_img = QtWidgets.QPushButton(self.centralwidget)
        self.btn_clear_img.setGeometry(QtCore.QRect(1050, 810, 70, 70))
        self.btn_clear_img.setStyleSheet("border-image: url(:/detect_button_background/delete.png);")
        self.btn_clear_img.setText("")
        self.btn_clear_img.setObjectName("btn_clear_img")
        self.btn_clear_img.clicked.connect(self.clearImage)

        # 退出应用
        self.btn_exit_app = QtWidgets.QPushButton(self.centralwidget)
        self.btn_exit_app.setGeometry(QtCore.QRect(1360, 810, 70, 70))
        self.btn_exit_app.setStyleSheet("border-image: url(:/detect_button_background/exit.png);")
        self.btn_exit_app.setText("")
        self.btn_exit_app.setObjectName("btn_exit_app")
        self.btn_exit_app.clicked.connect(self.exitApp)

        # 呈现原始图像
        self.label_show_yuanshi = QtWidgets.QLabel(self.centralwidget)
        self.label_show_yuanshi.setGeometry(QtCore.QRect(0, 80, 700, 700))
        self.label_show_yuanshi.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label_show_yuanshi.setObjectName("label_show_yuanshi")
        
        # 呈现结果图像
        self.label_show_jieguo = QtWidgets.QLabel(self.centralwidget)
        self.label_show_jieguo.setGeometry(QtCore.QRect(800, 80, 700, 700))
        self.label_show_jieguo.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label_show_jieguo.setObjectName("label_show_jieguo")

        # 呈现功能按键
        self.label_show_button = QtWidgets.QLabel(self.centralwidget)
        self.label_show_button.setGeometry(QtCore.QRect(0, 800, 1501, 141))
        self.label_show_button.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label_show_button.setText("")
        self.label_show_button.setObjectName("label_show_button")

        #编写模型加载
        self.edit_selet_model = QtWidgets.QLineEdit(self.centralwidget)
        self.edit_selet_model.setGeometry(QtCore.QRect(20, 890, 161, 40))
        font = QtGui.QFont()
        font.setFamily("Adobe 宋体 Std L")
        font.setPointSize(15)
        self.edit_selet_model.setFont(font)
        self.edit_selet_model.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.edit_selet_model.setObjectName("edit_selet_model")

        #编写图像加载
        self.edit_detect_img = QtWidgets.QLineEdit(self.centralwidget)
        self.edit_detect_img.setGeometry(QtCore.QRect(300, 890, 250, 40))
        font = QtGui.QFont()
        font.setFamily("Adobe 宋体 Std L")
        font.setPointSize(15)
        self.edit_detect_img.setFont(font)
        self.edit_detect_img.setObjectName("edit_detect_img")
        
        #编写图像保存
        self.edit_save_img = QtWidgets.QLineEdit(self.centralwidget)
        self.edit_save_img.setGeometry(QtCore.QRect(650, 890, 250, 40))
        font = QtGui.QFont()
        font.setFamily("Adobe 宋体 Std L")
        font.setPointSize(15)
        self.edit_save_img.setFont(font)
        self.edit_save_img.setObjectName("edit_save_img")
        
        #编写图像清除
        self.edit_clear_img = QtWidgets.QLineEdit(self.centralwidget)
        self.edit_clear_img.setGeometry(QtCore.QRect(950, 890, 250, 40))
        font = QtGui.QFont()
        font.setFamily("Adobe 宋体 Std L")
        font.setPointSize(15)
        self.edit_clear_img.setFont(font)
        self.edit_clear_img.setObjectName("edit_clear_img")
        
        #编写应用退出
        self.edit_exit_app = QtWidgets.QLineEdit(self.centralwidget)
        self.edit_exit_app.setGeometry(QtCore.QRect(1315, 890, 161, 40))
        font = QtGui.QFont()
        font.setFamily("Adobe 宋体 Std L")
        font.setPointSize(15)
        self.edit_exit_app.setFont(font)
        self.edit_exit_app.setObjectName("edit_exit_app")

        # 标题
        self.label_show_title = QtWidgets.QLabel(self.centralwidget)
        self.label_show_title.setGeometry(QtCore.QRect(190, 10, 1101, 80))
        font = QtGui.QFont()
        font.setFamily("Adobe 黑体 Std R")
        font.setPointSize(15)
        self.label_show_title.setFont(font)
        self.label_show_title.setStyleSheet("")
        self.label_show_title.setObjectName("label_show_title")

        self.label_show_button.raise_()
        self.btn_selet_model.raise_()
        self.btn_detect_img.raise_()
        self.btn_save_img.raise_()
        self.btn_clear_img.raise_()
        self.btn_exit_app.raise_()
        self.label_show_title.raise_()
        self.label_show_yuanshi.raise_()
        self.label_show_jieguo.raise_()
        self.edit_selet_model.raise_()
        self.edit_detect_img.raise_()
        self.edit_save_img.raise_()
        self.edit_clear_img.raise_()
        self.edit_exit_app.raise_()

        # 主窗口
        self.setCentralWidget(self.centralwidget)
        self.retranslateUi(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(self.centralwidget)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_show_title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600; color:#ffffff;\">基于YOLOv8的检测演示软件</span></p></body></html>"))
        self.label_show_yuanshi.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt;\">原始图像和视频</span></p></body></html>"))
        self.label_show_jieguo.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt;\">检测图像和视频</span></p></body></html>"))
        self.edit_selet_model.setText(_translate("MainWindow", "模型加载"))
        self.edit_detect_img.setText(_translate("MainWindow", "图像和视频加载"))
        self.edit_save_img.setText(_translate("MainWindow", "图像和视频保存"))
        self.edit_clear_img.setText(_translate("MainWindow", "图像和视频清除"))
        self.edit_exit_app.setText(_translate("MainWindow", "应用退出"))
        self.edit_selet_model.setAlignment(Qt.AlignCenter)
        self.edit_detect_img.setAlignment(Qt.AlignCenter)
        self.edit_save_img.setAlignment(Qt.AlignCenter)
        self.edit_clear_img.setAlignment(Qt.AlignCenter)
        self.edit_exit_app.setAlignment(Qt.AlignCenter)


    
    # 模型选择函数
    def seletModels(self):
        self.openfile_name_model, _ = QFileDialog.getOpenFileName(self.btn_selet_model, '选择weights文件', '.', '权重文件(*.pt)')
        if not self.openfile_name_model:
            QMessageBox.warning(self, "Warning:", "打开权重失败", buttons=QMessageBox.Ok,)
        else:
            print('加载weights文件地址为：' + str(self.openfile_name_model))
            QMessageBox.information(self, u"Notice", u"权重打开成功", buttons=QtWidgets.QMessageBox.Ok)
            
    # 图像选择函数
    def openImage(self):
        name_list = []
        fname, _ = QFileDialog.getOpenFileName()
        # video_file, _ = QFileDialog.getOpenFileName(self, "选择视频文件", "", "视频文件 (*.mp4 *.avi)")
        self.fname = fname
        if not self.fname:
            self.openImage()
        model = YOLO(self.openfile_name_model)
        if not self.fname.endswith(".mp4"):
            pixmap = QtGui.QPixmap(fname)
            self.label_show_yuanshi.setPixmap(pixmap)
            self.label_show_yuanshi.setScaledContents(True)
            img = cv2.imread(fname)
            # 引入模型
            # 通过引用模型进行图像检测
            results = model.predict(source=self.fname)
            annotated_frame = results[0].plot()
            # 将图像数据转换为QImage格式
            height, width, channel = annotated_frame.shape
            bytes_per_line = 3 * width
            qimage = QtGui.QImage(annotated_frame.data, width, height, bytes_per_line, QtGui.QImage.Format_BGR888)
            self.qImg = qimage
            # 将QImage转换为QPixmap
            pixmap = QtGui.QPixmap.fromImage(qimage)
            self.label_show_jieguo.setPixmap(pixmap)
            self.label_show_jieguo.setScaledContents(True)
            return self.qImg
        else:
            # self.video_capture = cv2.VideoCapture(self.fname)
            # self.timer = QTimer()
            # self.timer.timeout.connect(self.origin_update_frame)
            # self.timer.start(33)  # 每秒刷新30帧
            self.video_capture = cv2.VideoCapture(self.fname)
            boolresult=self.predict_video(model,self.fname)
            if boolresult:
                self.predict_video_capture = cv2.VideoCapture(".temp/temp.mp4")
                self.timer2 = QTimer()
                self.timer2.timeout.connect(self.display)
                self.timer2.start(33)  # 每秒刷新30帧
            else:
                self.openImage()



    def predict_video(self,model,fname):
        try :
            cap = cv2.VideoCapture(self.fname)
            if not os.path.exists(".temp"):
                os.mkdir(".temp")
            temp_file=".temp/temp.mp4"
            frame_width = int(cap.get(3))
            frame_height = int(cap.get(4))
            # 创建VideoWriter对象
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(temp_file, fourcc, 25.0, (frame_width, frame_height))

            # 设置整个视频处理的进度条
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            pbar = tqdm(total=total_frames, desc="Processing video", unit="frames")

            # 处理视频帧
            for _ in range(total_frames):
                # 读取某一帧
                success, frame = cap.read()
                if success:
                    # 使用yolov8进行预测
                    results = model(frame)
                    # 可视化结果
                    annotated_frame = results[0].plot()
                    # 将带注释的帧写入视频文件
                    out.write(annotated_frame)
                    # 更新进度条
                    pbar.update(1)
                else:
                    # 最后结尾中断视频帧循环
                    break

            # 若有部分帧未正常打开，进度条是不会达到百分之百的，下面这行代码会让进度条跑满
            pbar.update(total_frames - pbar.n)
            # 完成视频处理，关闭进度条
            pbar.close()

            # 释放读取和写入对象
            cap.release()
            out.release()

            return True
        except Exception as e:
            return False
    
    def display(self):
        ret, frame = self.video_capture.read()
        
        ret2, frame2 = self.predict_video_capture.read()

        if ret and ret2:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            rgb_image2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)

            # 创建QImage并显示在标签1上
            image_height, image_width, _ = rgb_image.shape
            image_height2, image_width2, _ = rgb_image2.shape

            q_image1 =  QtGui.QImage(rgb_image.data, image_width, image_height,  QtGui.QImage.Format_RGB888)
            pixmap1 =  QtGui.QPixmap.fromImage(q_image1)
            self.label_show_yuanshi.setPixmap(pixmap1.scaled(self.label_show_yuanshi.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


            # 创建QImage并显示在标签2上
            q_image2 =  QtGui.QImage(rgb_image2.data, image_width2, image_height2,  QtGui.QImage.Format_RGB888)
            pixmap2 =  QtGui.QPixmap.fromImage(q_image2)
            self.label_show_jieguo.setPixmap(pixmap2.scaled(self.label_show_jieguo.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    # 图像保存函数
    def saveImage(self):
        if not self.fname.endswith(".mp4"):
            fd, _ = QFileDialog.getSaveFileName(self, "保存图片", ".", "*.jpg")
            self.qImg.save(fd)
        else:
            fd, _ = QFileDialog.getSaveFileName(self, "保存视频", ".", "*.mp4")
            shutil.copyfile(".temp/temp.mp4",fd)
            # # #  关闭文件句柄
            # file = open(".temp/temp.mp4", 'r')
            # file.close()
        
    # 图像清除函数
    def clearImage(self, stopp):
        result = QMessageBox.question(self, "Warning:", "是否清除本次检测结果", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if result == QMessageBox.Yes:
            self.label_show_yuanshi.clear()
            self.label_show_jieguo.clear()
            # if self.fname.endswith(".mp4"):
            #     shutil.rmtree(".temp")
        else:
            stopp.ignore()
            
    # 应用退出函数
    def exitApp(self, event):
        event = QApplication.instance()
        result = QMessageBox.question(self, "Notice:", "您真的要退出此应用吗", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if result == QMessageBox.Yes:
            # if self.fname.endswith(".mp4"):
            #     shutil.rmtree(".temp")
            event.quit()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())
    # if os.path.exists(".temp"):
    #     shutil.rmtree(".temp")
