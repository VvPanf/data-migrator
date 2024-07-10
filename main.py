import logging

from gui.gui import Gui


def main():
    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')
    gui = Gui()
    gui.mainloop()


if __name__ == '__main__':
    main()
