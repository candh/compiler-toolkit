from toolkit.modules.grammar import is_terminal


def is_terminal(sym, pgrammar):
    return sym not in pgrammar.keys()


def follow_set(start, non_ter, first_sets, pgrammar, parents=[]):

    """
    makes follow set of the provided non-terminal
    input:
        start: start symbol.
        symbol: which symbol to make a follow set for.
        pgrammar: parsed grammar.
        parents: Please leave it as is. Or provide if you know what's up.
    """

    ret = set()

    if non_ter == start:
        ret.add("$")

    # go thru the productions
    for nt, prods in pgrammar.items():
        for rule in prods.copy():
            rule = rule.split()
            if non_ter in rule:
                ri = rule.index(non_ter)
                recurse = False
                next_nullable = False

                if ri < len(rule) - 1:
                    for i in range(1, len(rule) - ri):
                        next_sym = rule[ri + i]
                        if not is_terminal(next_sym, pgrammar):
                            fs = first_sets[next_sym].copy()
                            next_nullable = "eps" in fs
                            fs -= {"eps"}
                            ret |= fs
                            if not next_nullable:
                                break  # it's non-nullable
                        else:
                            next_nullable = False
                            ret.add(next_sym)
                            break

                if ri == len(rule) - 1 or next_nullable:
                    if nt != non_ter and nt not in parents:
                        recurse = True

                if recurse:
                    parents.append(non_ter)
                    ret |= follow_set(start, nt, first_sets, pgrammar, parents)
                    parents.pop()

    return ret


def follow_sets(start, pgrammar, first_sets):
    """make follow sets of all the non-terminals in the pgrammar

    Input:
        start: start non-terminal
        pgrammar: parsed grammar
        first_sets: pre-computed first sets
    """

    if start not in first_sets.keys():
        raise "start doesn't have first set"

    return {k: follow_set(start, k, first_sets, pgrammar) for k in first_sets.keys()}
