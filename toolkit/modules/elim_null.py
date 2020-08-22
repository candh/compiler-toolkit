import copy


def replace_in_grammar(non_ter, new_grammar):
    for nt, prod in new_grammar.items():
        for rule in prod.copy():
            if non_ter in rule:
                rule = list(rule.split())
                rule.remove(non_ter)
                if len(rule):
                    new_grammar[nt].add(" ".join(rule))


def elim_null(pgrammar):
    new_grammar = copy.deepcopy(pgrammar)  # make a copy
    for non_ter, prod in new_grammar.items():
        if "eps" in prod:
            new_grammar[non_ter].remove("eps")
            replace_in_grammar(non_ter, new_grammar)
    return new_grammar
