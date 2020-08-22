from collections import defaultdict


def remove_imm(xi, new_grammar, pgrammar):
    if len(new_grammar[xi]) == 0:
        rules = pgrammar[xi]
    else:
        # copy rules from new grammar
        rules = new_grammar[xi].copy()
        new_grammar[xi].clear()

    # if any of the rules start with the same nonterminal as the xi
    new_nt = xi + "'"
    if any(x.startswith(xi) for x in rules):
        for rule in rules:
            if rule.startswith(xi):
                # [2:] to also remove the space after the NT
                new_grammar[new_nt].add(rule[2:] + " " + new_nt)
            else:
                new_grammar[xi].add(rule + " " + new_nt)
        new_grammar[new_nt].add("eps")
    else:
        # keep the same rules
        new_grammar[xi] = rules


def remove_ind(xi, xj, new_grammar, pgrammar):
    if len(new_grammar[xi]) == 0:
        rules = pgrammar[xi]
    else:
        rules = new_grammar[xi].copy()
        new_grammar[xi].clear()

    if any(x.startswith(xj) for x in rules):
        for rule in rules:
            if rule.startswith(xj):
                new_grammar[xi] |= set(
                    map(lambda x: rule.replace(xj, x), new_grammar[xj])
                )
            else:
                new_grammar[xi].add(rule)


def elim_lr(pgrammar):
    """
    Input: parsed grammar with no cycles or eps productions.
    Output: An equivalent grammar with no left productions.
    """

    new_grammar = defaultdict(set)

    for i, xi in enumerate(pgrammar.keys()):
        for xj in list(pgrammar.keys())[:i]:
            # eliminate indirect left recursion
            remove_ind(xi, xj, new_grammar, pgrammar)

        # eliminate immediate left recursion
        remove_imm(xi, new_grammar, pgrammar)

    return dict(new_grammar)  # convert
