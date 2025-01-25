# WIN10ACT - Windows 10 Activation Utility
# Author: Nick Roussis
# GitHub: @nrxss (aka neek - @neek8044)
# License: Apache 2.0

DEBUG_MODE = False


from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

import sys, ctypes, os, time
from threading import Thread
import utils.act as act


def print(*args, **kwargs):

    if "-d" in sys.argv or DEBUG_MODE == True:

        return __builtins__.print(*args, **kwargs)

print("\n[ Win10Act Debug Output ]\n")

ext = os.path.splitext(sys.argv[0])[1]
print(ext)
is_compiled = True if "exe" in ext else False


def admin_status():

    try:

        return ctypes.windll.shell32.IsUserAnAdmin()
    except:

        return False


if not admin_status():

    print("> Elevating process privileges.")
    ctypes.windll.shell32.ShellExecuteW(
            None, 
            "runas", 
            sys.executable, 
            " ".join(sys.argv[1:] if is_compiled else sys.argv), 
            None, 
            1
        )

    if not admin_status():

        print("> Failed to elevate process privileges.")
        sys.exit(1)

    else:

        print("> Process privileges elevated.")

else:

    print("> Elevated privileges detected.")


class MainWindow(QMainWindow):

    done = pyqtSignal()

    def __init__(self):

        super().__init__()

        print("> Initializing Fullscreen Window.")

        self.setWindowTitle("Windows 10 Activation Utility")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet("background-color: black;")
        self.showFullScreen()

        print("> Setting up layout.")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)
        self.label = QLabel("Activating Windows", self.central_widget)
        self.label.setStyleSheet("color: white;")
        self.label.setFont(QFont("Calibri", 50))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)

        self.loading_label = QLabel(self.central_widget)
        self.loading_movie = QMovie("resources/loading_64.gif")
        self.loading_label.setMovie(self.loading_movie)
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the GIF
        self.loading_movie.start()
        self.layout.addWidget(self.loading_label)

        if DEBUG_MODE == True:
            self.debug_textbox = QTextEdit(self.central_widget)
            self.debug_textbox.setReadOnly(True)
            self.debug_textbox.setStyleSheet("color: white; background-color: black;")
            self.debug_textbox.setFixedHeight(100)
            self.layout.addWidget(self.debug_textbox)

            # Redirect print to the textbox
            class TextBoxStream:
                def write(self, text):
                    self.debug_textbox.append(text)
                def flush(self):
                    pass

            sys.stdout = TextBoxStream()

        self.done.connect(self.close) # close pyqt window upon signal emit


    def showEvent(self, event):

        super().showEvent(event)

        t = Thread(target=self.run_tasks).start()


    def run_tasks(self):

        print("> Calling activation script.")

        act.run()

        while act.t.is_alive(): # wait until all commands have been executed by checking the thread status

            pass
        
        print("> Command sequence completed.")

        # Display subprocess outputs
        if hasattr(self, 'debug_textbox'):
            for output in act.outputs:
                self.debug_textbox.append(f"Command output:\n{output}\n")
    
        self.label.setText("Activation Completed")
        self.loading_movie.stop()
        self.loading_label.hide()
        time.sleep(2)

        print("> Exiting application.")

        self.done.emit() # call close event signal


print("> Starting application.")

app = QApplication(sys.argv)
window = MainWindow()
window.show()

sys.exit(app.exec())
