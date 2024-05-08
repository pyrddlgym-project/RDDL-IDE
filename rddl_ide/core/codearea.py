import customtkinter
from tkinter import font
from pygments import token
from pygments.styles import get_style_by_name
import re

PYTHON_GRAMMAR = [
    (token.Keyword, (r"\b(?P<KEYWORD>False|None|True|and|as|assert|async|await|"
                     r"break|class|continue|def|del|elif|else|except|finally|for|"
                     r"from|global|if|import|in|is|lambda|nonlocal|not|or|pass|"
                     r"raise|return|try|while|with|yield)\b")),
    (token.Keyword, r"\b(?P<INSTANCE>super|self|cls)\b"),
    (token.Keyword.Type, r"\b(?P<TYPES>bool|bytearray|bytes|dict|float|int|list|str|tuple|object)\b"),
    (token.Name.Builtin, (r"([^.'\"\\#]\b|^)(?P<BUILTIN>abs|all|any|ascii|bin|"
                          r"breakpoint|callable|chr|classmethod|compile|complex|"
                          r"copyright|credits|delattr|dir|divmod|enumerate|eval|"
                          r"exec|exit|filter|format|frozenset|getattr|globals|"
                          r"hasattr|hash|help|hex|id|input|isinstance|issubclass|"
                          r"iter|len|license|locals|map|max|memoryview|min|next|"
                          r"oct|open|ord|pow|print|quit|range|repr|reversed|"
                          r"round|set|setattr|slice|sorted|staticmethod|sum|"
                          r"type|vars|zip)\b")),
    (token.Name.Decorator, r"(^[ \t]*(?P<DECORATOR>@[\w\d\.]+))"),
    (token.String, (r"(?P<STRING>(?i:r|u|f|fr|rf|b|br|rb)?'[^'\\\n]*"
                    r"(\\.[^'\\\n]*)*'?|(?i:r|u|f|fr|rf|b|br|rb)?\"[^\"\\\n]*"
                    r"(\\.[^\"\\\n]*)*\"?)")),
    (token.String.Doc, (r"(?P<DOCSTRING>(?i:r|u|f|fr|rf|b|br|rb)?'''[^'\\]*((\\.|'"
                        r"(?!''))[^'\\]*)*(''')?|(?i:r|u|f|fr|rf|b|br|rb)?\"\"\""
                        r"[^\"\\]*((\\.|\"(?!\"\"))[^\"\\]*)*(\"\"\")?)")),
    (token.Number, r"\b(?P<NUMBER>((0x|0b|0o|#)[\da-fA-F]+)|((\d*\.)?\d+))\b"),
    (token.Comment, r"(?P<COMMENT>#[^\n]*)")
]

RDDL_GRAMMAR = [
    (token.Keyword, r'\b(?P<KEYWORD>if|then|else|switch|case|default)\b'),
    (token.Keyword, (r'\b(?P<COMPONENT>domain|requirements|types|objects|pvariables|cpfs|reward|'
                     r'action-preconditions|state-invariants|termination|'
                     r'instance|init-state|non-fluents|max-nondef-actions|horizon|discount)\b')),
    (token.Keyword, (r'\b(?P<FTYPES>state-fluent|action-fluent|observ-fluent|'
                     r'interm-fluent|derived-fluent|non-fluent)\b')),
    (token.Keyword.Type, r'\b(?P<TYPES>bool|int|real|object)\b'),
    (token.Name.Builtin, r"([^.'\"\\#]\b|^)(?P<BUILTIN>exp|log|sin|cos|tan|min|max|pow)\b"),
    (token.Name.Builtin, r'\b(?P<AGGREGATION>sum|prod|minimum|maximum|exists|forall|argmax|argmin)'),
    (token.Name.Builtin, r'\b(?P<RANDOM>KronDelta|DiracDelta|Bernoulli|Normal|Gamma|Uniform)'),
    (token.Name.Variable, r"\?([^,:;+\-\*\/\s}\)\]]+)"),
    (token.Literal, r"\@([^,:;+\-\*\/\s}\)\]]+)"),
    (token.Number, r"\b(?P<NUMBER>((0x|0b|0o|#)[\da-fA-F]+)|((\d*\.)?\d+))\b"),
    (token.Comment, r'(?P<COMMENT>//[^\n]*)')
]
        

class CTkCodeViewer(customtkinter.CTkTextbox):

    def __init__(self, *args,
                 width: int=100,
                 height: int=32,
                 language="python",
                 theme="monokai",
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self._monokai_style = get_style_by_name(theme)
        self._style_parsed = self._monokai_style.list_styles()
        for key in self._style_parsed:
            if key[1]["color"] != "" and key[1]["color"] != None:
                tag_name = str(key[0])
                color = "#" + key[1]["color"]
                self.tag_config(tag_name, foreground=color)
        if language == 'python':
            self.patterns = PYTHON_GRAMMAR
        else:
            self.patterns = RDDL_GRAMMAR
        self.bind("<KeyRelease>", lambda *args: self.apply())
        
    def apply(self):
        for tag, pattern in self.patterns:
            text = self.get('0.0', 'end').splitlines()
            for (i, line) in enumerate(text):
                for found in re.finditer(pattern, line):
                    self.tag_add(
                        str(tag), f"{i + 1}.{found.start()}", f"{i + 1}.{found.end()}")


class TextLineNumbers(customtkinter.CTkTextbox):

    def __init__(self, master, text_widget, **kwargs):
        super().__init__(master, **kwargs)
 
        self.text_widget = text_widget
        for tag in ['<KeyRelease>', '<FocusIn>', '<MouseWheel>', '<Configure>', '<<Modified>>']:
            self.text_widget.bind(tag, self.on_key_release)
        self.configure(state='disabled', width=55)
        
    def on_key_release(self, event=None):
        p, _ = self.text_widget.index("@0,0").split('.')
        p = int(p)
        final_index = str(self.text_widget.index('end'))
        num_of_lines = final_index.split('.')[0]
        line_numbers_string = "\n".join(str(p + no) for no in range(int(num_of_lines)))
                
        self.configure(state='normal')
        self.delete(0.0, 'end')
        self.insert(0.0, line_numbers_string)
        self.configure(state='disabled')
            

class CodeEditor:
    
    def __init__(self, window, language, theme='monokai'):
        if 'Consolas' in font.names() or 'Consolas' in font.families():
            my_font = 'Consolas'
        else:
            my_font = 'Courier'
        text_area = CTkCodeViewer(
            window, font=(my_font, 12), language=language, theme=theme, wrap='none')
        self.text = text_area
        
        ln = TextLineNumbers(window, text_area, width=3, font=(my_font, 12))
        ln.pack(side='left', fill='both')
        text_area.pack(expand=True, fill='both')
        
        _ = customtkinter.CTkScrollbar(window, command=text_area.xview)
        _ = customtkinter.CTkScrollbar(window, command=text_area.yview)
        
