from toolkit.modules.is_nullable import is_nullable
from toolkit.modules.grammar import is_terminal


def first_set(non_ter, pgrammar, nullables, parents=[]):
    """
    Makes first set of the given non_terminal.
    terminals are not allowed :)

    Input:
        non_ter: Non Terminal for which you want to create a first set for
        pgrammar: parsed grammar. bring it on.
        nullable: list of nullabes (precomputed)
        parents: Please leave it as is. Or provide if you know what's up.
    Output:
        first set (set)
    """

    ret = set()
    prods = pgrammar[non_ter].copy()
    nullable = False

    if "eps" in prods:
        nullable = True
        prods.remove("eps")

    null_list = []
    for rule in prods:
        r_null_list = []
        for sym in rule.split():
            if is_terminal(sym, pgrammar):
                ret.add(sym)
                r_null_list.append(False)  # terminal is not a nullable
                break  # break on a terminal
            else:
                isn = sym in nullables
                r_null_list.append(isn)

                if sym == non_ter:
                    if not isn:
                        break
                    else:
                        # prevent self loop but still
                        # explore next symbol
                        continue

                if sym not in parents:
                    parents.append(non_ter)
                    ret |= first_set(sym, pgrammar, nullables)
                    parents.pop()

                if not isn:
                    # break on a non-nullable non-terminal
                    break

        null_list.append(all(r_null_list))

    if not any(null_list):
        if "eps" in ret:
            ret.remove("eps")

    if nullable:
        ret.add("eps")

    return ret


def first_sets(pgrammar):
    """
    returns first sets of all the non-terminals in the grammar
    """
    nullables = [k for k in pgrammar.keys() if is_nullable(k, pgrammar)]
    return {k: first_set(k, pgrammar, nullables) for k in pgrammar.keys()}
