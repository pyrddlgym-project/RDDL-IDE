import re
import idlelib.colorizer as ic
import idlelib.percolator as ip


def assign_highlighting_rddl(text_area):
    TAGDEFS = {}
    
    # comments
    COMMENT = (r'(?P<COMMENT>//[^\n]*)')
    TAGDEFS['COMMENT'] = {'foreground': 'green', 'background': None}
    
    # code blocks and RDDL components
    COMPONENT = (r'\b(?P<COMPONENT>domain|requirements|types|objects|pvariables|cpfs|reward|'
                 r'action-preconditions|state-invariants|termination|'
                 r'instance|init-state|non-fluents|max-nondef-actions|horizon|discount)\b')
    TAGDEFS['COMPONENT'] = {'foreground': 'navy', 'background': None, 'font': ('Courier New', 12, 'bold')}
    
    # keywords
    KEYWORD = (r'\b(?P<KEYWORD>if|then|else|switch|case|default)\b')
    TAGDEFS['KEYWORD'] = {'foreground': 'navy', 'background': None}
    
    # fluent types
    FTYPES = (r'\b(?P<FTYPES>state-fluent|action-fluent|observ-fluent|'
              r'interm-fluent|derived-fluent|non-fluent)\b')
    TAGDEFS['FTYPES'] = {'foreground': 'navy', 'background': None}
    
    # data types
    TYPES = (r'\b(?P<TYPES>bool|int|real|object)\b')
    TAGDEFS['TYPES'] = {'foreground': 'navy', 'background': None}
    
    # numbers
    NUMBER = (r"\b(?P<NUMBER>((0x|0b|0o|#)[\da-fA-F]+)|((\d*\.)?\d+))\b")
    TAGDEFS['NUMBER'] = {'foreground': 'black', 'background': None}
    
    # literals
    LITERAL = (r'\b(?P<LITERAL>true|false|pos-inf)\b')
    TAGDEFS['LITERAL'] = {'foreground': 'navy', 'background': None}
    
    # functions
    BUILTIN = (r"([^.'\"\\#]\b|^)(?P<BUILTIN>exp|log|sin|cos|tan|min|max|pow)\b")
    TAGDEFS['BUILTIN'] = {'foreground': 'darkblue', 'background': None}
    
    AGGREGATION = (r'\b(?P<AGGREGATION>sum|prod|minimum|maximum|exists|forall|argmax|argmin)')
    TAGDEFS['AGGREGATION'] = {'foreground': 'darkblue', 'background': None}
    
    RANDOM = (r'\b(?P<RANDOM>KronDelta|DiracDelta|Bernoulli|Normal)')
    TAGDEFS['RANDOM'] = {'foreground': 'darkblue', 'background': None}
    
    # combine all rules
    PROG = rf'{COMMENT}|{COMPONENT}|{KEYWORD}|{FTYPES}|{TYPES}|{NUMBER}|{LITERAL}|{BUILTIN}|{AGGREGATION}|{RANDOM}'
    IDPROG = r"(?<!class)\s+(\w+)"
    
    # assign syntax highlighter to text_area
    cd = ic.ColorDelegator()
    cd.prog = re.compile(PROG, re.S | re.M)
    cd.idprog = re.compile(IDPROG, re.S)
    cd.tagdefs = {**cd.tagdefs, **TAGDEFS}
    ip.Percolator(text_area).insertfilter(cd)
