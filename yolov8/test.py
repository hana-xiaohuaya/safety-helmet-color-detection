# # import sys
# # import cv2
# # from PyQt5.QtCore import Qt, QTimer
# # from PyQt5.QtGui import QImage, QPixmap
# # from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout

# # class VideoPlayer(QWidget):
# #     def __init__(self):
# #         super().__init__()
        
# #         self.video_path = 'test_video.mp4'  # 视频文件的路径
# #         self.video_capture = cv2.VideoCapture(self.video_path)
        
# #         self.image_label = QLabel(self)
# #         self.image_label.setAlignment(Qt.AlignCenter)
        
# #         layout = QVBoxLayout()
# #         layout.addWidget(self.image_label)
# #         self.setLayout(layout)
        
# #         self.timer = QTimer()
# #         self.timer.timeout.connect(self.update_frame)
# #         self.timer.start(33)  # 每秒刷新30帧
        
# #     def update_frame(self):
# #         ret, frame = self.video_capture.read()
# #         if ret:
# #             rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# #             image_height, image_width, _ = rgb_image.shape
# #             q_image = QImage(rgb_image.data, image_width, image_height, 
# #                              QImage.Format_RGB888)
# #             pixmap = QPixmap.fromImage(q_image)
# #             self.image_label.setPixmap(pixmap.scaled(self.image_label.size(),
# #                                                      Qt.KeepAspectRatio,
# #                                                      Qt.SmoothTransformation))
        
# # if __name__ == '__main__':
# #     app = QApplication(sys.argv)
# #     player = VideoPlayer()
# #     player.show()
# #     sys.exit(app.exec_())


# #         # 图像选择函数
# #     def openImage(self):
# #         name_list = []
# #         fname, _ = QFileDialog.getOpenFileName()
# #         # video_file, _ = QFileDialog.getOpenFileName(self, "选择视频文件", "", "视频文件 (*.mp4 *.avi)")
# #         self.fname = fname
# #         model = YOLO(self.openfile_name_model)
# #         if not self.fname.endswith(".mp4"):
# #             pixmap = QtGui.QPixmap(fname)
# #             self.label_show_yuanshi.setPixmap(pixmap)
# #             self.label_show_yuanshi.setScaledContents(True)
# #             img = cv2.imread(fname)
# #             # 引入模型
# #             # 通过引用模型进行图像检测
# #             results = model.predict(source=self.fname)
# #             annotated_frame = results[0].plot()
# #             # 将图像数据转换为QImage格式
# #             height, width, channel = annotated_frame.shape
# #             bytes_per_line = 3 * width
# #             qimage = QtGui.QImage(annotated_frame.data, width, height, bytes_per_line, QtGui.QImage.Format_BGR888)
# #             self.qImg = qimage
# #             # 将QImage转换为QPixmap
# #             pixmap = QtGui.QPixmap.fromImage(qimage)
# #             self.label_show_jieguo.setPixmap(pixmap)
# #             self.label_show_jieguo.setScaledContents(True)
# #             return self.qImg
# #         else:
# #             self.video_capture = cv2.VideoCapture(self.fname)
# #             self.timer = QTimer()
# #             self.timer.timeout.connect(self.update_frame(self.video_capture,self.label_show_yuanshi))
# #             self.timer.start(33)  # 每秒刷新30帧
# #             boolresult=self.predict_video(model,self.video_capture)
# #             if boolresult:
# #                 self.video_capture = cv2.VideoCapture(".temp/temp.mp4")
# #                 self.timer = QTimer()
# #                 self.timer.timeout.connect(self.update_frame(self.video_capture,self.label_show_yuanshi))
# #                 self.timer.start(33)  # 每秒刷新30帧
# #             else:
# #                 self.openImage()

# #     def predict_video(self,model,cap):
# #         try :
# #             if not os.path.exists(".temp"):
# #                 os.mkdir(".temp")
# #             temp_file=".temp/temp.mp4"
# #             frame_width = int(cap.get(3))
# #             frame_height = int(cap.get(4))
# #             # 创建VideoWriter对象
# #             fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# #             out = cv2.VideoWriter(temp_file, fourcc, 25.0, (frame_width, frame_height))
# #             # 设置整个视频处理的进度条
# #             total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# #             # 处理视频帧
# #             for _ in range(total_frames):
# #                 # 读取某一帧
# #                 success, frame = cap.read()
# #                 if success:
# #                     # 使用yolov8进行预测
# #                     results = model(frame)
# #                     # 可视化结果
# #                     annotated_frame = results[0].plot()
# #                     # 将带注释的帧写入视频文件
# #                     out.write(annotated_frame)
# #                     # 最后结尾中断视频帧循环
# #                     break

# #             # 释放读取和写入对象
# #             cap.release()
# #             out.release()
# #             return True
# #         except Exception as e:
# #             return False

# import sys
# import cv2
# from PyQt5.QtCore import Qt, QTimer
# from PyQt5.QtGui import QImage, QPixmap
# from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

# class VideoPlayer(QWidget):
#     def __init__(self):
#         super().__init__()

#         # 设置视频文件路径
#         self.video_path = 'test_video.mp4'

#         # 创建视频标签1
#         self.video_label1 = QLabel(self)
#         self.video_label1.setAlignment(Qt.AlignCenter)

#         # 创建视频标签2
#         self.video_label2 = QLabel(self)
#         self.video_label2.setAlignment(Qt.AlignCenter)

#         # 创建布局并添加标签
#         layout = QVBoxLayout()
#         layout.addWidget(self.video_label1)
#         layout.addWidget(self.video_label2)
#         self.setLayout(layout)

#         # 加载视频
#         self.load_video()

#     def load_video(self):
#         # 使用OpenCV加载视频
#         self.video_capture = cv2.VideoCapture(self.video_path)

#         # 创建定时器，定期读取视频帧并显示在标签上
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.display_frame)
#         self.timer.start(33)  # 设置定时器间隔，单位为毫秒

#     def display_frame(self):
#         # 从视频中读取帧
#         ret, frame = self.video_capture.read()
#         if ret:
#             # 转换为RGB格式
#             rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#             # 创建QImage并显示在标签1上
#             image_height, image_width, _ = rgb_image.shape
#             q_image1 = QImage(rgb_image.data, image_width, image_height, QImage.Format_RGB888)
#             pixmap1 = QPixmap.fromImage(q_image1)
#             self.video_label1.setPixmap(pixmap1.scaled(self.video_label1.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

#             # 创建QImage并显示在标签2上
#             q_image2 = QImage(rgb_image.data, image_width, image_height, QImage.Format_RGB888)
#             pixmap2 = QPixmap.fromImage(q_image2)
#             self.video_label2.setPixmap(pixmap2.scaled(self.video_label2.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     player = VideoPlayer()
#     player.show()
#     sys.exit(app.exec_())
import shutil
shutil.rmtree(".temp")