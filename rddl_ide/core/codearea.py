from tkinter import Text, Scrollbar, \
    LEFT, RIGHT, BOTH, NONE, HORIZONTAL, VERTICAL, BOTTOM, X, Y, END, font

from core.highlighting import assign_highlighting_rddl, assign_highlighting_python


class TextLineNumbers(Text):

    def __init__(self, master, text_widget, **kwargs):
        super().__init__(master, **kwargs)
 
        self.text_widget = text_widget
        for tag in ['<KeyRelease>', '<FocusIn>', '<MouseWheel>', '<Configure>', '<<Modified>>']:
            self.text_widget.bind(tag, self.on_key_release)
        self.configure(state='disabled')
 
    def on_key_release(self, event=None):
        p, _ = self.text_widget.index("@0,0").split('.')
        p = int(p)
        final_index = str(self.text_widget.index(END))
        num_of_lines = final_index.split('.')[0]
        line_numbers_string = "\n".join(str(p + no) for no in range(int(num_of_lines)))
        width = len(str(num_of_lines))
 
        self.configure(state='normal', width=width)
        self.delete(1.0, END)
        self.insert(1.0, line_numbers_string)
        self.configure(state='disabled')


class CodeEditor:
    
    def __init__(self, window, rddl=True):
        if 'Consolas' in font.names() or 'Consolas' in font.families():
            my_font = 'Consolas'
        else:
            my_font = 'Courier'
        text_area = Text(window, font=(my_font, 12), wrap=NONE)
        self.text = text_area
        
        ln = TextLineNumbers(window, text_area, width=3, font=(my_font, 12))
        ln.pack(side=LEFT, fill=BOTH)
        text_area.pack(expand=True, fill=BOTH)
        
        horizontal = Scrollbar(text_area, orient=VERTICAL)
        horizontal.pack(side=RIGHT, fill=Y)
        horizontal.config(command=text_area.yview)
        
        vertical = Scrollbar(text_area, orient=HORIZONTAL)
        vertical.pack(side=BOTTOM, fill=X)
        vertical.config(command=text_area.xview)
        
        text_area.config(yscrollcommand=horizontal.set, xscrollcommand=vertical.set) 
        if rddl:
            assign_highlighting_rddl(text_area)
        else:
            assign_highlighting_python(text_area)
        
