import copy


def get_unit_prods(non_ter, pgrammar):
    """
    Input: non_terminal, new_grammar
    Ouput: unit productions of a non terminal if they exist else None
    """
    unit_prods = None
    all_non_terms = list(pgrammar.keys())

    # remove the given non_ter from list of all non terms
    all_non_terms.remove(non_ter)
    # if there are other non terminals at all other than this
    if all_non_terms:
        prod = pgrammar[non_ter]
        # if any of the non terminals appear as a unit in the productions
        if any(x in prod for x in all_non_terms):
            # filter out the unit prods
            unit_prods = list(filter(lambda x: x in all_non_terms, prod))

    return unit_prods


def elim_unit(pgrammar):
    new_grammar = copy.deepcopy(pgrammar)  # make a copy
    flag = True
    while flag:
        flag = False
        for non_ter, prod in new_grammar.items():
            unit_prods = get_unit_prods(non_ter, new_grammar)
            if unit_prods:
                flag = True
                for rule in prod.copy():
                    if rule in unit_prods:
                        new_grammar[non_ter].remove(rule)  # remove that rule
                        new_grammar[non_ter] |= new_grammar[rule]

                    if non_ter in new_grammar[non_ter]:  # remove things like B -> B
                        new_grammar[non_ter].remove(non_ter)

    return new_grammar


def replace_in_grammar(nt1, nt2, pgrammar):
    """
    replaces nonterminal2 with nonterminal1 in the entire grammar
    """

    for non_ter, prod in pgrammar.items():
        # don't need to replace any non_ter because we have already removed that rule.
        # because we change rules in the loop (we need to make a copy)
        for rule in prod.copy():
            if nt2 in rule.split():
                nr = rule.replace(nt2, nt1)
                pgrammar[non_ter].remove(rule)
                pgrammar[non_ter].add(nr)


def remove_same_rules(pgrammar_, ask=True, verbose=True):
    """
    removes the same productions from the grammar.
    A -> a
    B -> a
    Just becomes A -> a (or B -> a if you choose to keep B, i.e: ask is True)

    If ask is false, it just replaces all the similar production non-terminals
    with the first non-terminal that appears in the grammar provided.

    very dumb. very expensive. should work. i did't wanna make an adjacency graph
    """

    pgrammar = copy.deepcopy(pgrammar_)

    same_list = None
    for non_ter_i, prod_i in pgrammar.copy().items():

        if same_list:
            if non_ter_i in same_list:
                continue  # skip this. we have dealt with this

        same_list = [non_ter_i]
        if non_ter_i not in pgrammar:
            # if it has already been replaced
            continue

        for non_ter_j, prod_j in pgrammar.items():
            if non_ter_i == non_ter_j:
                continue
            else:
                if prod_j == prod_i:
                    same_list.append(non_ter_j)

        if len(same_list) > 1:
            if verbose:
                print(", ".join(same_list), "production are the same.")
            if ask:
                pick = input("pick a non_terminal to replace all of them: ")
            else:
                # if in test mode. just pick the first non-terminal to replace the others
                pick = same_list[0]
                if verbose:
                    print("picking", pick, "for same list", same_list)

            if pick in same_list:
                slc = same_list.copy()
                slc.remove(pick)
                # remove all rules but that pick
                for non_ter in slc:
                    del pgrammar[non_ter]
                    replace_in_grammar(pick, non_ter, pgrammar)
            else:
                print("wrong choice")
                exit(1)
    return pgrammar
