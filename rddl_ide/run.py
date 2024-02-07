from tkinter import Tk

from core.codearea import CodeEditor
from core.menubar import assign_menubar_functions


def main():
    
    # main windows
    domain_window = Tk()
    domain_window.title('[Domain] Untitled.rddl')         
    domain_window.geometry('%dx%d+%d+%d' % (domain_window.winfo_screenwidth() / 2,
                                            domain_window.winfo_screenheight() * 0.9,
                                            0, 0))
    domain_window.resizable(height=None, width=None)
    domain_window.columnconfigure(0, weight=1)
    domain_window.rowconfigure(0, weight=1)
    
    inst_window = Tk()
    inst_window.title('[Instance] Untitled.rddl')
    inst_window.geometry('%dx%d+%d+%d' % (inst_window.winfo_screenwidth() / 2,
                                          inst_window.winfo_screenheight() / 2,
                                          domain_window.winfo_screenwidth() / 2,
                                          0))
    inst_window.resizable(height=None, width=None)
    inst_window.columnconfigure(0, weight=1)
    inst_window.rowconfigure(0, weight=1)
    
    # text editors
    domain_editor = CodeEditor(domain_window)
    inst_editor = CodeEditor(inst_window)
    
    # menu bars
    assign_menubar_functions(domain_window, inst_window, domain_editor.text, inst_editor.text)
    
    # finalize
    domain_window.update()
    domain_window.mainloop()
    inst_window.update()
    inst_window.mainloop()


if __name__ == '__main__':
    main()