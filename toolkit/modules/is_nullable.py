def is_nullable(non_ter, pgrammar, parents=[]):
    prods = pgrammar[non_ter]
    non_ters = pgrammar.keys()

    # if its production directly contains an "eps"
    if "eps" in prods:
        return True

    # filter out
    # 1. self rules (to prevent self loop and also saves needless calls)
    # 2. parents (to prevent infinite recursion)
    # 3. non-terminal anywhere in the rule

    prods = list(
        filter(
            lambda x: non_ter not in x
            and all(parent not in x for parent in parents)
            and all(t in non_ters for t in x.split()),
            prods,
        )
    )

    res_list = []
    for rule in prods:
        for sym in rule.split():
            res = True
            parents.append(non_ter)
            res = is_nullable(sym, pgrammar, parents)
            parents.pop()

            # early break if any of the sym in the rule was not nullable
            if not res:
                break

        res_list.append(res)

    return any(res_list) if res_list else False
