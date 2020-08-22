from toolkit.modules.make_follow_sets import follow_sets
from toolkit.modules.make_first_sets import first_sets
from toolkit.modules.grammar import is_terminal
from tabulate import tabulate


def parsing_table(pgrammar, fs, fls, error_recovery=True):
    """
    Input:
        pgrammar: parsed grammar
        fs: first sets
        fls: follow sets
        error_recovery: fill parsing table with pop/scan values for error cells
    """

    # nonterminals with eps in their first sets
    nullables = [k for k in pgrammar.keys() if "eps" in fs[k]]

    # TODO: rewrite this loop better
    terminals = set()
    for prod in pgrammar.values():
        for rule in prod:
            for sym in rule.split():
                if is_terminal(sym, pgrammar) and sym != "eps":
                    terminals.add(sym)

    if not terminals:
        return

    terminals = list(terminals)
    terminals.append("$")

    table = []
    for nt, prod in pgrammar.items():
        row = [None] * len(terminals)
        for rule in prod:
            for sym in rule.split():
                eps = False
                if sym == "eps":
                    eps = True
                else:
                    if is_terminal(sym, pgrammar):
                        row[terminals.index(sym)] = "{} -> {}".format(nt, rule)
                    else:
                        for fse in fs[sym]:
                            if fse == "eps":
                                eps = True
                            else:
                                row[terminals.index(fse)] = "{} -> {}".format(nt, rule)

                if eps:
                    for flse in fls[nt]:
                        row[terminals.index(flse)] = "{} -> {}".format(nt, rule)

                if not eps and sym not in nullables:
                    break

        table.append([nt] + row)

    if error_recovery:
        for row in table:
            # row[0] is the non-terminal
            for flse in fls[row[0]]:
                # + 1 because we also added a non-terminal
                ix = terminals.index(flse) + 1
                if row[ix] is None:
                    row[ix] = "Pop({})".format(row[0])

            # fill remaining values with 'scan'
            for i in range(1, len(row)):
                if row[i] is None:
                    row[i] = "scan"

    return tabulate(table, headers=["input"] + terminals)


# if __name__ == "__main__":
#     import grammar as gm

#     # grammar = """
#     # X -> a X | g | Y Z | eps
#     # Y -> d | u Y | eps
#     # Z -> i | eps
#     # """

#     grammar = """
#     E -> T E'
#     E' -> + T E' | eps
#     T -> F T'
#     T' -> * F T' | eps
#     F -> id | ( E )
#     """

#     pgrammar = gm.parse(grammar)

#     fs = first_sets(pgrammar)
#     fls = follow_sets("E", pgrammar, fs)

#     # print("first sets:")
#     # gm.set_print(fs)
#     # print("follow sets:")
#     # gm.set_print(fls)

#     make_parsing_table(pgrammar, fs, fls)
