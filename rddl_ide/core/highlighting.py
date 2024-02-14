import re
import idlelib.colorizer as ic
import idlelib.percolator as ip


def assign_highlighting_rddl(text_area):
    
    # syntax
    COMMENT = r'(?P<COMMENT>//[^\n]*)'
    COMPONENT = (r'\b(?P<COMPONENT>domain|requirements|types|objects|pvariables|cpfs|reward|'
                 r'action-preconditions|state-invariants|termination|'
                 r'instance|init-state|non-fluents|max-nondef-actions|horizon|discount)\b')
    KEYWORD = r'\b(?P<KEYWORD>if|then|else|switch|case|default)\b'
    FTYPES = (r'\b(?P<FTYPES>state-fluent|action-fluent|observ-fluent|'
              r'interm-fluent|derived-fluent|non-fluent)\b')
    TYPES = r'\b(?P<TYPES>bool|int|real|object)\b'
    NUMBER = r"\b(?P<NUMBER>((0x|0b|0o|#)[\da-fA-F]+)|((\d*\.)?\d+))\b"
    LITERAL = r'\b(?P<LITERAL>true|false|pos-inf)\b'
    BUILTIN = r"([^.'\"\\#]\b|^)(?P<BUILTIN>exp|log|sin|cos|tan|min|max|pow)\b"
    AGGREGATION = r'\b(?P<AGGREGATION>sum|prod|minimum|maximum|exists|forall|argmax|argmin)'
    RANDOM = r'\b(?P<RANDOM>KronDelta|DiracDelta|Bernoulli|Normal)'
    
    PROG = rf'{COMMENT}|{COMPONENT}|{KEYWORD}|{FTYPES}|{TYPES}|{NUMBER}|{LITERAL}|{BUILTIN}|{AGGREGATION}|{RANDOM}'
    IDPROG = r"(?<!class)\s+(\w+)"
    
    # coloring
    TAGDEFS = {}
    TAGDEFS['COMMENT'] = {'foreground': 'green', 'background': None}
    TAGDEFS['COMPONENT'] = {'foreground': 'navy', 'background': None, 'font': ('Courier New', 12, 'bold')}
    TAGDEFS['KEYWORD'] = {'foreground': 'navy', 'background': None, 'font': ('Courier New', 12, 'bold')}
    TAGDEFS['FTYPES'] = {'foreground': 'navy', 'background': None}
    TAGDEFS['TYPES'] = {'foreground': 'navy', 'background': None}
    TAGDEFS['NUMBER'] = {'foreground': 'gray10', 'background': None}
    TAGDEFS['LITERAL'] = {'foreground': 'gray10', 'background': None}
    TAGDEFS['BUILTIN'] = {'foreground': 'blue2', 'background': None}
    TAGDEFS['AGGREGATION'] = {'foreground': 'blue2', 'background': None}
    TAGDEFS['RANDOM'] = {'foreground': 'blue2', 'background': None}
    
    # assign syntax highlighter to text_area
    cd = ic.ColorDelegator()
    cd.prog = re.compile(PROG, re.S | re.M)
    cd.idprog = re.compile(IDPROG, re.S)
    cd.tagdefs = {**cd.tagdefs, **TAGDEFS}
    ip.Percolator(text_area).insertfilter(cd)


def assign_highlighting_python(text_area):
    cd = ic.ColorDelegator()
    ip.Percolator(text_area).insertfilter(cd)
    
