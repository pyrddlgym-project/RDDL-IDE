from tkinter import Tk

from core.codearea import CodeEditor
from core.menubar import assign_menubar_functions


def main():
    
    # domain window
    domain_window = Tk()
    domain_window.title('[Domain] Untitled')
    w, h = domain_window.maxsize() 
    w = int(w * 0.99)
    h = int(h * 0.95)
    domain_window.geometry(f'{w // 2}x{h}+0+0')
    domain_window.resizable(height=None, width=None)
    domain_window.columnconfigure(0, weight=1)
    domain_window.rowconfigure(0, weight=1)
    
    # instance window
    inst_window = Tk()
    inst_window.title('[Instance] Untitled')
    inst_window.geometry(f'{w // 2}x{h // 2}+{w // 2}+0')
    inst_window.resizable(height=None, width=None)
    inst_window.columnconfigure(0, weight=1)
    inst_window.rowconfigure(0, weight=1)
    
    # policy window
    policy_window = Tk()
    policy_window.title('[Policy] Policy')
    o = 50
    policy_window.geometry(f'{w // 2}x{h // 2 - o}+{w // 2}+{h // 2 + o}')
    policy_window.resizable(height=None, width=None)
    policy_window.columnconfigure(0, weight=1)
    policy_window.rowconfigure(0, weight=1)
    
    # text editors
    domain_editor = CodeEditor(domain_window)
    inst_editor = CodeEditor(inst_window)
    policy_editor = CodeEditor(policy_window, rddl=False)
    
    # menu bars
    assign_menubar_functions(domain_window, inst_window, policy_window, 
                             domain_editor.text, inst_editor.text, policy_editor.text)
    
    # finalize
    domain_window.update()
    domain_window.mainloop()
    inst_window.update()
    inst_window.mainloop()
    policy_window.update()
    policy_window.mainloop()


if __name__ == '__main__':
    main()
