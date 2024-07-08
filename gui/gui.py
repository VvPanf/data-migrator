import logging
import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import app.processor as processor
from app.file_reader import get_folder_files
from tkinter import DISABLED, END, EXTENDED
from tkinter.messagebox import showwarning

from gui.log import TextHandler


class Gui(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Data Migrator')

        self.rowconfigure(0, minsize=400, weight=1)
        self.columnconfigure(1, minsize=300, weight=1)

        # Левая часть
        frame = tk.Frame(self)
        label_mode = tk.Label(frame, text='Выберите режим:')
        self.dev_mode = tk.BooleanVar(value=True)
        self.ift_mode = tk.BooleanVar(value=True)
        self.check_dev = tk.Checkbutton(frame, text='DEV', variable=self.dev_mode)
        self.check_ift = tk.Checkbutton(frame, text='IFT', variable=self.ift_mode)

        label_reports = tk.Label(frame, text='Выберите отчёты для миграции:')
        self.list_reports = tk.Listbox(frame, selectmode=EXTENDED)
        label_hint = tk.Label(frame, text='(Для выбора нескольких элементов зажмите Сtrl)', font=('TkDefaultFont', 7))
        btn_start = tk.Button(frame, text='Начать', command=self.start)

        for item in get_folder_files():
            self.list_reports.insert(END, item[0:-4])

        label_mode.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.check_dev.grid(row=1, column=0, sticky='w', padx=5)
        self.check_ift.grid(row=2, column=0, sticky='w', padx=5)
        label_reports.grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.list_reports.grid(row=4, column=0, sticky='ew', padx=5, pady=5)
        label_hint.grid(row=5, column=0, sticky='w', padx=5)
        btn_start.grid(row=6, column=0, sticky='ew', padx=5, pady=5)

        frame.grid(row=0, column=0, sticky='ns')

        # Правая часть
        self.txt_logs = scrolledtext.ScrolledText(self, state=DISABLED)
        self.txt_logs.grid(row=0, column=1, sticky='nsew')
        self.handler = TextHandler(self.txt_logs)

        # Добавляем вывод логов на форму
        logging.getLogger().addHandler(self.handler)

        # Поток для обработки
        self.process = None

    def start(self):
        if not self.dev_mode.get() and not self.ift_mode.get():
            showwarning(message='Выберите режим DEV и(или) IFT')
            return
        if len(self.list_reports.curselection()) == 0:
            showwarning(message='Выберите хотя бы один из отчётов')
            return
        all_items = self.list_reports.get(0, END)
        selected_items = [all_items[item] for item in self.list_reports.curselection()]
        self.process = processor.get_start_process_thread(selected_items, self.dev_mode.get(), self.ift_mode.get())
        self.process.start()

    def ctrl_event(self, event):
        # Обработка Ctrl + C
        if event.state == 4 and event.keysym == 'c':
            content = self.txt_logs.selection_get()
            self.clipboard_clear()
            self.clipboard_append(content)
            return 'break'
        else:
            return 'break'
