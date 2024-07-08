import logging

from gui.gui import Gui


def main():
    logging.getLogger().addHandler(logging.StreamHandler())
    gui = Gui()
    gui.mainloop()


if __name__ == '__main__':
    main()
