from difflib import SequenceMatcher
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
    TAGDEFS['NUMBER'] = {'foreground': 'brown4', 'background': None}
    TAGDEFS['LITERAL'] = {'foreground': 'brown4', 'background': None}
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


def closest_substring(corpus, query, case_sensitive=True):
    step = min(4, max(1, len(query) * 3 // 4 - 1))
    flex = max(1, len(query) // 3 - 1)
    
    def _match(a, b):
        return SequenceMatcher(None, a, b).ratio()

    def scan_corpus(step):
        match_values, m = [], 0
        while m + qlen - step <= len(corpus):
            match_values.append(_match(query, corpus[m: m - 1 + qlen]))
            m += step
        return match_values

    def adjust_left_right_positions():
        p_l, bp_l = [pos] * 2
        p_r, bp_r = [pos + qlen] * 2
        bmv_l = match_values[p_l // step]
        bmv_r = match_values[p_l // step]
        for f in range(flex):
            ll = _match(query, corpus[p_l - f: p_r])
            if ll > bmv_l:
                bmv_l, bp_l = ll, p_l - f
            lr = _match(query, corpus[p_l + f: p_r])
            if lr > bmv_l:
                bmv_l, bp_l = lr, p_l + f
            rl = _match(query, corpus[p_l: p_r - f])
            if rl > bmv_r:
                bmv_r, bp_r = rl, p_r - f
            rr = _match(query, corpus[p_l: p_r + f])
            if rr > bmv_r:
                bmv_r, bp_r = rr, p_r + f
        return bp_l, bp_r

    if not case_sensitive:
        query, corpus = query.lower(), corpus.lower()
    qlen = len(query)
    if flex >= qlen / 2: flex = 3
    match_values = scan_corpus(step)    
    pos = max(range(len(match_values)), key=match_values.__getitem__) * step
    return adjust_left_right_positions()
