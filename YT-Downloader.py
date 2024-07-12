import yt_dlp, sys, threading, urllib.request, os, json

from PyQt5 import QtWidgets, QtCore, QtGui
from youtubesearchpython import VideosSearch
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not os.path.exists("./_internal/cfg"):
            f = open("./_internal/cfg", "w")
            f.write(os.path.join(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents'), "YT-Downloader"))
            f.close()

        if os.path.exists("./_internal/cfg"):
            f = open("./_internal/cfg", "r")
            self.location = f.read()

        # Variables
        self.results = 10
        self.titles = []
        self.durations = []
        self.links = []
        self.thumbnailURLs = []

        # Fonts
        self.baseFont = QtGui.QFont()
        self.baseFont.setFamily("Bahnschrift SemiBold")
        self.baseFont.setPointSize(12)

        self.secondaryFont = QtGui.QFont()
        self.secondaryFont.setFamily("Bahnschrift SemiBold")
        self.secondaryFont.setPointSize(20)
        self.secondaryFont.setBold(True)
        self.secondaryFont.setWeight(75)

        self.versionFont = QtGui.QFont()
        self.versionFont.setFamily("Bahnschrift SemiBold")
        self.versionFont.setPointSize(10)
        self.versionFont.setBold(True)
        self.versionFont.setWeight(75)

        self.progressFont = QtGui.QFont()
        self.progressFont.setFamily("Bahnschrift SemiBold")
        self.progressFont.setPointSize(12)
        self.progressFont.setBold(True)
        self.progressFont.setWeight(75)

        # Pixmaps
        self.windowIcon = QtGui.QIcon()
        self.windowIcon.addPixmap(QtGui.QPixmap("./_internal/[50X50] logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.logo = QtGui.QPixmap("./_internal/[200x100] logo-text.png")

        # Layouts
        self.layout = QVBoxLayout()

        # Main Window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(801, 641)
        MainWindow.setMinimumSize(QtCore.QSize(801, 641))
        MainWindow.setMaximumSize(QtCore.QSize(801, 641))
        MainWindow.setWindowIcon(self.windowIcon)
        MainWindow.setStyleSheet("background-color: rgb(25, 25, 25);")
        MainWindow.setWindowTitle("YT-Downloader")

        # Central Widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        # Icon Group
        self.iconGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.iconGroup.setGeometry(QtCore.QRect(10, 10, 221, 111))
        self.iconGroup.setTitle("")
        self.iconGroup.setObjectName("iconGroup")

        # Icon Group - Label
        self.iconLabel = QtWidgets.QLabel(self.iconGroup)
        self.iconLabel.setGeometry(QtCore.QRect(10, 10, 201, 91))
        self.iconLabel.setStyleSheet("")
        self.iconLabel.setText("")
        self.iconLabel.setPixmap(self.logo)
        self.iconLabel.setObjectName("iconLabel")

        # Input Group
        self.inputGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.inputGroup.setGeometry(QtCore.QRect(240, 10, 471, 51))
        self.inputGroup.setTitle("")
        self.inputGroup.setObjectName("inputGroup")

        # Input Group - Line Edit
        self.inputLineEdit = QtWidgets.QLineEdit(self.inputGroup)
        self.inputLineEdit.setGeometry(QtCore.QRect(10, 9, 451, 31))
        self.inputLineEdit.setFont(self.baseFont)
        self.inputLineEdit.setStyleSheet("color: rgb(255, 255, 255);")
        self.inputLineEdit.setText("")
        self.inputLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.inputLineEdit.setObjectName("inputLineEdit")
        self.inputLineEdit.setPlaceholderText("Search Term")

        # Search Group
        self.searchGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.searchGroup.setGeometry(QtCore.QRect(710, 10, 81, 51))
        self.searchGroup.setTitle("")
        self.searchGroup.setObjectName("searchGroup")

        # Search Group - Button
        self.searchButton = QtWidgets.QPushButton(self.searchGroup)
        self.searchButton.setGeometry(QtCore.QRect(10, 10, 61, 31))
        self.searchButton.setFont(self.baseFont)
        self.searchButton.setStyleSheet("color: rgb(255, 255, 255);")
        self.searchButton.setCheckable(False)
        self.searchButton.setDefault(False)
        self.searchButton.setFlat(False)
        self.searchButton.setObjectName("searchButton")
        self.searchButton.setText("Search")
        self.searchButton.clicked.connect(self.getSearchResults)

        # Format Group
        self.formatGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.formatGroup.setGeometry(QtCore.QRect(10, 130, 221, 71))
        self.formatGroup.setTitle("")
        self.formatGroup.setObjectName("formatGroup")

        # Format Group - Label
        self.formatLabel = QtWidgets.QLabel(self.formatGroup)
        self.formatLabel.setGeometry(QtCore.QRect(50, 10, 111, 31))
        self.formatLabel.setFont(self.secondaryFont)
        self.formatLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.formatLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.formatLabel.setObjectName("formatLabel")
        self.formatLabel.setText("FORMAT")

        # Format Group - Audio Radio
        self.formatAudio = QtWidgets.QRadioButton(self.formatGroup)
        self.formatAudio.setGeometry(QtCore.QRect(30, 40, 71, 21))
        self.formatAudio.setFont(self.baseFont)
        self.formatAudio.setStyleSheet("color: rgb(255, 255, 255);")
        self.formatAudio.setChecked(True)
        self.formatAudio.setObjectName("formatAudio")
        self.formatAudio.setText("AUDIO")

        # Format Group - Video Radio
        self.formatVideo = QtWidgets.QRadioButton(self.formatGroup)
        self.formatVideo.setGeometry(QtCore.QRect(110, 40, 71, 21))
        self.formatVideo.setFont(self.baseFont)
        self.formatVideo.setStyleSheet("color: rgb(255, 255, 255);")
        self.formatVideo.setObjectName("formatVideo")
        self.formatVideo.setText("VIDEO")

        # Status Group
        self.statusGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.statusGroup.setGeometry(QtCore.QRect(10, 210, 221, 71))
        self.statusGroup.setTitle("")
        self.statusGroup.setObjectName("statusGroup")

        # Status Group - Label
        self.label = QtWidgets.QLabel(self.statusGroup)
        self.label.setGeometry(QtCore.QRect(10, 10, 201, 31))
        self.label.setFont(self.secondaryFont)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label.setText("STATUS")

        # Status Group - Status Label
        self.statusLabel = QtWidgets.QLabel(self.statusGroup)
        self.statusLabel.setGeometry(QtCore.QRect(10, 40, 201, 21))
        self.statusLabel.setFont(self.progressFont)
        self.statusLabel.setStyleSheet("color: rgb(255, 0, 0)")
        self.statusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.statusLabel.setObjectName("statusLabel")
        self.statusLabel.setText("IDLE")

        # Video Group
        self.videoGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.videoGroup.setGeometry(QtCore.QRect(240, 70, 551, 351))
        self.videoGroup.setTitle("")
        self.videoGroup.setObjectName("videoGroup")

        # Video Group - Scroll Area
        self.videoScrollArea = QtWidgets.QScrollArea(self.videoGroup)
        self.videoScrollArea.setGeometry(QtCore.QRect(9, 9, 531, 331))
        self.videoScrollArea.setWidgetResizable(True)
        self.videoScrollArea.setObjectName("videoScrollArea")

        # Video Group - Scroll Area - Contents
        self.videoScrollAreaContents = QtWidgets.QWidget()
        self.videoScrollAreaContents.setGeometry(QtCore.QRect(0, 0, 529, 329))
        self.videoScrollAreaContents.setObjectName("videoScrollAreaContents")
        self.videoScrollAreaContents.setLayout(self.layout)
        self.videoScrollArea.setWidget(self.videoScrollAreaContents)

        # Location Group
        self.locationGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.locationGroup.setGeometry(QtCore.QRect(240, 430, 471, 51))
        self.locationGroup.setTitle("")
        self.locationGroup.setObjectName("locationGroup")

        # Location Group - Line Edit
        self.locationLineEdit = QtWidgets.QLineEdit(self.locationGroup)
        self.locationLineEdit.setEnabled(False)
        self.locationLineEdit.setGeometry(QtCore.QRect(10, 9, 451, 31))
        self.locationLineEdit.setFont(self.baseFont)
        self.locationLineEdit.setStyleSheet("color: rgb(255, 255, 255);")
        self.locationLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.locationLineEdit.setObjectName("locationLineEdit")
        self.locationLineEdit.setText(self.location)

        # Change Group
        self.changeGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.changeGroup.setGeometry(QtCore.QRect(710, 430, 81, 51))
        self.changeGroup.setTitle("")
        self.changeGroup.setObjectName("changeGroup")

        # Change Group - Button
        self.changeButton = QtWidgets.QPushButton(self.changeGroup)
        self.changeButton.setGeometry(QtCore.QRect(10, 10, 61, 31))
        self.changeButton.setFont(self.baseFont)
        self.changeButton.setStyleSheet("color: rgb(255, 255, 255);")
        self.changeButton.setCheckable(False)
        self.changeButton.setDefault(False)
        self.changeButton.setFlat(False)
        self.changeButton.setObjectName("changeButton")
        self.changeButton.setText("Change")
        self.changeButton.clicked.connect(self.changeLocation)

        # Quality Group [Hopefully Coming Soon]
        self.qualityGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.qualityGroup.setEnabled(False)
        self.qualityGroup.setGeometry(QtCore.QRect(10, 290, 221, 191))
        self.qualityGroup.setTitle("")
        self.qualityGroup.setFlat(False)
        self.qualityGroup.setCheckable(False)
        self.qualityGroup.setObjectName("qualityGroup")

        # Quality Group - Label
        self.qualityLabel = QtWidgets.QLabel(self.qualityGroup)
        self.qualityLabel.setGeometry(QtCore.QRect(50, 10, 111, 31))
        self.qualityLabel.setFont(self.secondaryFont)
        self.qualityLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.qualityLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.qualityLabel.setObjectName("qualityLabel")
        self.qualityLabel.setText("QUALITY")

        # Progress Group
        self.progressGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.progressGroup.setGeometry(QtCore.QRect(10, 490, 781, 81))
        self.progressGroup.setTitle("")
        self.progressGroup.setObjectName("progressGroup")

        # Progress Group - Label
        self.progressLabel = QtWidgets.QLabel(self.progressGroup)
        self.progressLabel.setGeometry(QtCore.QRect(10, 10, 761, 31))
        self.progressLabel.setFont(self.secondaryFont)
        self.progressLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.progressLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.progressLabel.setObjectName("progressLabel")
        self.progressLabel.setText("DOWNLOAD PROGRESS")

        # Progress Group - Progress Bar
        self.progressBar = QtWidgets.QProgressBar(self.progressGroup)
        self.progressBar.setGeometry(QtCore.QRect(10, 50, 761, 21))
        self.progressBar.setFont(self.progressFont)
        self.progressBar.setStyleSheet("border-color: rgb(25, 25, 25); color: rgb(255, 255, 255);")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")

        # Author Group
        self.authorGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.authorGroup.setGeometry(QtCore.QRect(10, 580, 781, 51))
        self.authorGroup.setTitle("")
        self.authorGroup.setObjectName("authorGroup")

        # Author Group - Author Label
        self.authorLabel = QtWidgets.QLabel(self.authorGroup)
        self.authorLabel.setGeometry(QtCore.QRect(10, 10, 761, 31))
        self.authorLabel.setFont(self.secondaryFont)
        self.authorLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.authorLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.authorLabel.setObjectName("authorLabel")
        self.authorLabel.setText("CREATED BY: CraigLee247")

        # Author Group - Version Label
        self.versionLabel = QtWidgets.QLabel(self.authorGroup)
        self.versionLabel.setGeometry(QtCore.QRect(740, 10, 31, 31))
        self.versionLabel.setFont(self.versionFont)
        self.versionLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.versionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.versionLabel.setObjectName("versionLabel")
        self.versionLabel.setText("v1.0.0")


        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def getSearchResults(self):
        videosSearch = VideosSearch(self.inputLineEdit.text(), limit=self.results)
        videos = videosSearch.result()

        while self.layout.count():
            item = self.layout.itemAt(0)
            self.layout.removeItem(item)

        self.titles.clear()
        self.durations.clear()
        self.links.clear()
        self.thumbnailURLs.clear()

        # Get Video Info
        for video in videos["result"]:
            self.titles.append(video['title'])
            self.durations.append(video['duration'])
            self.links.append(video['link'])
            self.thumbnailURLs.append(f"https://img.youtube.com/vi/{video['id']}/hqdefault.jpg")

        # Create Search Results
        for i in range(self.results):
            self.addGroup(i, self.titles[i], self.durations[i])

    def addGroup(self, i, title, duration):
        # Get Thumbnail
        urllib.request.urlretrieve(self.thumbnailURLs[i], f"./_internal/video{i}Thumbnail.jpg")
        pixmap = QPixmap(f"./_internal/video{i}Thumbnail.jpg")

        # Main Font
        mainFont = QtGui.QFont()
        mainFont.setFamily("Bahnschrift SemiBold")
        mainFont.setPointSize(12)
        mainFont.setBold(True)
        mainFont.setWeight(75)

        # Secondary Font
        secondaryFont = QtGui.QFont()
        secondaryFont.setFamily("Bahnschrift SemiBold")
        secondaryFont.setPointSize(12)

        # Video Group
        self.videoGroup = QtWidgets.QGroupBox()
        self.videoGroup.setFixedSize(491, 141)
        self.videoGroup.setTitle("")
        self.videoGroup.setCheckable(False)
        self.videoGroup.setObjectName(title)

        # Video Thumbnail
        self.videoLabel = QtWidgets.QLabel(self.videoGroup)
        self.videoLabel.setGeometry(QtCore.QRect(10, 10, 161, 121))
        self.videoLabel.setFont(mainFont)
        self.videoLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.videoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.videoLabel.setObjectName(f"video{i}Label")
        self.videoLabel.setPixmap(pixmap)
        self.videoLabel.setScaledContents(True)

        # Info Group
        self.videoInfoGroup = QtWidgets.QGroupBox(self.videoGroup)
        self.videoInfoGroup.setGeometry(QtCore.QRect(180, 10, 301, 71))
        self.videoInfoGroup.setTitle("")
        self.videoInfoGroup.setObjectName(f"video{i}InfoGroup")

        # Video Title
        self.videoTitleLabel = QtWidgets.QLabel(self.videoInfoGroup)
        self.videoTitleLabel.setGeometry(QtCore.QRect(10, 10, 201, 20))
        self.videoTitleLabel.setFont(mainFont)
        self.videoTitleLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.videoTitleLabel.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft)
        self.videoTitleLabel.setObjectName(f"video{i}TitleLabel")
        self.videoTitleLabel.setText(title)

        # Video Duration
        self.videoDurationLabel = QtWidgets.QLabel(self.videoInfoGroup)
        self.videoDurationLabel.setGeometry(QtCore.QRect(10, 40, 201, 20))
        self.videoDurationLabel.setFont(mainFont)
        self.videoDurationLabel.setStyleSheet("color: rgb(255, 255, 255);")
        self.videoDurationLabel.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft)
        self.videoDurationLabel.setObjectName(f"video{i}DurationLabel")
        self.videoDurationLabel.setText(duration)

        # Download Group
        self.videoDownloadGroup = QtWidgets.QGroupBox(self.videoGroup)
        self.videoDownloadGroup.setGeometry(QtCore.QRect(370, 90, 111, 41))
        self.videoDownloadGroup.setTitle("")
        self.videoDownloadGroup.setObjectName(f"video{i}DownloadGroup")

        # Download Button
        self.videoDownloadButton = QtWidgets.QPushButton(self.videoDownloadGroup)
        self.videoDownloadButton.setGeometry(QtCore.QRect(10, 10, 91, 21))
        self.videoDownloadButton.setFont(secondaryFont)
        self.videoDownloadButton.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(25, 25, 25)")
        self.videoDownloadButton.setCheckable(False)
        self.videoDownloadButton.setDefault(False)
        self.videoDownloadButton.setFlat(False)
        self.videoDownloadButton.setObjectName(f"video{i}DownloadButton")
        self.videoDownloadButton.setText("Download")
        self.videoDownloadButton.clicked.connect(lambda: self.download(self.links[i]))

        self.layout.addWidget(self.videoGroup)

    def my_hook(self, d):
        if d['status'] == 'downloading':
            try:
                percentage = round(float(d['downloaded_bytes']) / float(d['total_bytes']) * 100, 1)
                self.progressBar.setValue(round(percentage))
            except:
                percentage = round(float(d['downloaded_bytes']) / float(d['total_bytes_estimate']) * 100, 1)
                self.progressBar.setValue(round(percentage))

        if d['status'] == 'finished':
            self.progressBar.setValue(0)

    def download(self, url):
        self.downloadStatus(True)
        if self.formatAudio.isChecked(): self.ydl_opts = {
                'noplaylist': True,
                'cachedir': False,
                'progress_hooks': [self.my_hook],
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    # 'preferredcodec': 'wav',
                    'preferredquality': '0'
                }],
                'prefer_ffmpeg': True,
                'keepvideo': False,
                'outtmpl': f'{self.location}/Audio/%(title)s.%(ext)s'
            }
        elif self.formatVideo.isChecked(): self.ydl_opts ={
                'noplaylist': True,
                'cachedir': False,
                'progress_hooks': [self.my_hook],
                'outtmpl': f'{self.location}/Video/%(title)s.%(ext)s'
            }
        thread = threading.Thread(target=self.start_download, args={url})
        thread.daemon = True
        thread.start()

    def start_download(self, video_url):
        try: yt_dlp.YoutubeDL(self.ydl_opts).download(video_url)
        except: self.errorMessage("Error Downloading Video! Please Try Again.")

        self.downloadStatus(False)

    def changeLocation(self):
        folder = str(QFileDialog.getExistingDirectory(QFileDialog(), "Select Directory", str(os.path.join(os.environ['USERPROFILE']))))
        file = f"{folder}/YT-Downloader"
        f = open("./_internal/cfg", "w")
        f.seek(0)
        f.write(file)
        f.truncate()
        f.close()
        self.location = file
        self.locationLineEdit.setText(file)

    def downloadStatus(self, status):
        if status == True:
            self.videoScrollArea.setStyleSheet("background-color: rgb(15, 15, 15);")
            self.videoScrollArea.setEnabled(False)
            self.inputLineEdit.setEnabled(False)
            self.searchButton.setEnabled(False)
            self.formatGroup.setEnabled(False)
            self.statusLabel.setText("DOWNLOADING")
            self.statusLabel.setStyleSheet("color: rgb(0, 255, 0)")

        if status == False:
            self.videoScrollArea.setStyleSheet("background-color: rgb(25, 25, 25);")
            self.videoScrollArea.setEnabled(True)
            self.inputLineEdit.setEnabled(True)
            self.searchButton.setEnabled(True)
            self.formatGroup.setEnabled(True)
            self.statusLabel.setText("IDLE")
            self.statusLabel.setStyleSheet("color: rgb(255, 0, 0)")

    def errorMessage(self, message): # Error Message
        msg = QMessageBox()
        msg.setWindowIcon(self.windowIcon)
        msg.setWindowTitle("Error Message")
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        x = msg.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
