import sys
from PyQt5 import QtWidgets, QtCore
from gui_qt import MainWindow, WinOverlay

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()

    # Trigger overlay after a short delay to demo the zoom + blur
    def show_demo():
        WinOverlay(w, '🎉 Demo: Player 0 wins!', winner_index=0)

    QtCore.QTimer.singleShot(800, show_demo)
    # Quit after a while to allow manual clicks during demo
    QtCore.QTimer.singleShot(12000, app.quit)

    sys.exit(app.exec_())
