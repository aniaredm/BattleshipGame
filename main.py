import sys

from PyQt5.QtWidgets import QApplication

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

def main():
    # Initialize GUI
    if 'gtk' in sys.argv:
        from src.interfaces.gui_pygtk import MyWindow
        win = MyWindow()
        win.show_all()
        Gtk.main()
    elif 'qt' in sys.argv:
        app = QApplication([])
        from src.interfaces.gui_pyqt import GUIPyQt
        gui = GUIPyQt()
        gui.show()
        app.exec_()
    else:
        sys.exit("No valid GUI framework provided. Type gtk or qt to choose valid framework.")

if __name__ == "__main__":
    main()
