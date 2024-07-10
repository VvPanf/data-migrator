import logging
from tkinter import END


class TextHandler(logging.Handler):
    # This class allows logging messages to be sent to a Tkinter Text widget
    def __init__(self, text):
        # Initialize the instance of the class
        logging.Handler.__init__(self)
        self.text = text
        self.formatter = logging.Formatter('[%(levelname)s] %(message)s')

    def emit(self, record):
        # Emit a message to the Text widget
        msg = self.format(record)

        def append():
            self.text.configure(state='normal')
            self.text.insert(END, msg + '\n')
            self.text.configure(state='disabled')
            self.text.yview(END)

        self.text.after(0, append)
