def parse(grammar, ulta=False):
    """ Parses the grammar """
    if not grammar:
        return None

    rules = grammar.strip().split("\n")
    productions_l = map(lambda x: map(lambda x: x.strip(), x.split("->")), rules)
    productions_l = [
        [x, set(map(lambda x: x.strip(), y.split("|")))] for x, y in productions_l
    ]
    pgrammar = dict(productions_l)
    return pgrammar


def is_terminal(sym, pgrammar):
    return sym not in pgrammar.keys()


def reverse_grammar(pgrammar):
    """reverses the order of the keys appearing in the parsed grammar."""
    pgrammar = dict(reversed(list(pgrammar.items())))
    return pgrammar


def pprint(pgrammar):
    if not pgrammar:
        return None
    for nt, rules in pgrammar.items():
        print(nt, "->", " | ".join(sorted(rules, key=len, reverse=True)))


def str_pgrammar(pgrammar):
    if not pgrammar:
        return None
    return "\n".join(
        [
            nt + " -> " + " | ".join(sorted(rules, key=len, reverse=True))
            for nt, rules in pgrammar.items()
        ]
    )


def set_print(fset):
    if not fset:
        return None
    for nt, items in fset.items():
        print(nt, "= {", ", ".join(sorted(items)), "}")


def str_set(fset):
    if not fset:
        return None
    return "\n".join(
        [nt + " = { " + ", ".join(sorted(items)) + " }" for nt, items in fset.items()]
    )
