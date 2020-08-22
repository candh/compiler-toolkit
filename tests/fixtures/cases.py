# test cases for paser
parser_test_cases = [
    """
    A -> B A
    """,
    """
    A ->   a B a
    """,
    """
    A ->a B a |   x D
    """,
    """
    A ->V a|X a|eps
    """,
    """
    B ->V | V a |V
    """,
    """
    B -> V | V a | V
    A -> A
    """,
    """
    X -> a X | g | Y Z | eps
    Y -> d | u Y | eps
    Z -> i | eps
    """,
    """
    E -> T X
    X -> + E | eps
    T -> i Y | ( E )
    Y -> * T | eps
    """,
    """
    C -> P F class id X Y
    P -> public | eps
    F -> final | eps
    X -> extends id | eps
    Y -> implements I | eps
    I -> id J
    J -> , I | eps
    """,
    """
    PROG -> STMT
    STMT -> if EXPR then BLOCK | while EXPR do BLOCK | EXPR ;
    EXPR -> TERM => id | isZero? TERM | not EXPR | ++ id | -- id
    TERM -> id | const
    BLOCK -> STMT | { STMTS }
    STMTS -> STMT STMTS | eps
    """,
]

# parser test cases targets
parser_test_cases_targets = [
    {"A": set(["B A"])},
    {"A": set(["a B a"])},
    {"A": set(["a B a", "x D"])},
    {"A": set(["V a", "X a", "eps"])},
    {"B": set(["V a", "V"])},
    {"B": set(["V a", "V"]), "A": set(["A"])},
    {
        "X": set(["a X", "g", "Y Z", "eps"]),
        "Y": set(["d", "u Y", "eps"]),
        "Z": set(["i", "eps"]),
    },
    {
        "E": set(["T X"]),
        "X": set(["+ E", "eps"]),
        "T": set(["i Y", "( E )"]),
        "Y": set(["* T", "eps"]),
    },
    {
        "C": set(["P F class id X Y"]),
        "P": set(["public", "eps"]),
        "F": set(["final", "eps"]),
        "X": set(["extends id", "eps"]),
        "Y": set(["implements I", "eps"]),
        "I": set(["id J"]),
        "J": set([", I", "eps"]),
    },
    {
        "PROG": set(["STMT"]),
        "STMT": set(["if EXPR then BLOCK", "while EXPR do BLOCK", "EXPR ;"]),
        "EXPR": set(["TERM => id", "isZero? TERM", "not EXPR", "++ id", "-- id"]),
        "TERM": set(["id", "const"]),
        "BLOCK": set(["STMT", "{ STMTS }"]),
        "STMTS": set(["STMT STMTS", "eps"]),
    },
]

# left recursion elimination test cases
# False to order non-terminals in the order they appear in the grammar.
# True to order non-terminals in the opposite order they appear in the grammar (reversed).

elim_lr_test_cases = [
    (
        """
        A -> A a | b
        """,
        False,
    ),
    (
        """
        E -> E + T | T
        T -> T * F | F
        F -> id | ( E )
        """,
        False,
    ),
    (
        """
        X -> X a | X d | Y e
        Y -> X i | u
        """,
        True,
    ),
    (
        """
        X -> e X a | d | Y e
        Y -> X i | u
        """,
        False,
    ),
    (
        """
        X -> X a | X d | Y e
        Y -> X i | Y u | h
        """,
        False,
    ),
    (
        """
        X -> X a | X d | Y e
        Y -> Z i | u
        Z -> X j | e
        """,
        True,
    ),
    (
        """
        A -> A b | a C
        B -> B a B B | b
        C -> b C | B A
        """,
        True,
    ),
    (
        """
        A -> A b d | B d
        B -> A e | d
        """,
        True,
    ),
    # this is not left recursive
    (
        """
        D -> g
        C -> e
        B -> D B | f
        S -> B h | C B h | C h | a | a D | h
        """,
        True,
    ),
    (
        """
        A -> B x y | x
        B -> C D
        C -> A | c
        D -> d
        """,
        True,
    ),
    (
        """
        A -> B a | b
        B -> C d | e
        C -> D f | g
        D -> D f | A a | C g
        """,
        False,
    ),
]

elim_lr_test_cases_targets = [
    """
    A -> b A'
    A' -> a A' | eps
    """,
    """
    E -> T E'
    E' -> + T E' | eps
    T -> F T'
    T' -> * F T' | eps
    F -> id | ( E )
    """,
    """
    X -> u e X'
    X' -> a X' | d X' | i e X' | eps
    Y -> X i | u
    """,
    """
    X -> e X a | d | Y e
    Y -> e X a i Y' | d i Y' | u Y'
    Y' -> e i Y' | eps
    """,
    """
    X -> Y e X'
    X' -> a X' | d X' | eps
    Y ->  h Y'
    Y' -> e X' i Y' | u Y' | eps
    """,
    """
    X -> e i e X' | u e X'
    X' -> a X' | d X' | j i e X' | eps
    Y -> X j i | e i | u
    Z -> X j | e
    """,
    """
    A -> a C A'
    A' -> b A' | eps
    B -> b B'
    B' -> a B B B' | eps
    C -> b C | B A
    """,
    """
    A -> d d A'
    A' -> b d A' | e d A' | eps
    B -> A e | d
    """,
    """
    D -> g
    C -> e
    B -> D B | f
    S -> B h | C B h | C h | a | a D | h
    """,
    """
    A -> x A' | c D x y A'
    A' -> D x y A' | eps
    B -> A D | c D
    C -> A | c
    D -> d
    """,
    """
    A -> B a | b
    B -> C d | e
    C -> D f | g
    D -> g g D' | b a D' | e a a D' | g d a a D'
    D' -> f D' | f d a a D' | f g D' | eps
    """,
]

# null production elimnination tests cases
elim_null_test_cases = [
    """
    S -> S a | eps
    """,
    """
    S -> S d | a | X e
    X -> X y | g X | d | eps
    """,
    """
    X -> X Y | X e | a | eps
    Y -> X Z | d | i Y | eps
    Z -> g | Y X | eps
    """,
    """
    A -> B D | e | B g
    B -> i D | j | B u | eps
    D -> a D | B | eps
    """,
    """
    S -> X Y | Y
    X -> a X b | eps
    Y -> a Y b | Z
    Z -> b Z a | eps
    """,
    """
    S -> X Z
    X -> a X b | eps
    Z -> a Z | Z X | eps
    """,
    """
    S -> A B a b
    A -> B
    B -> A | eps
    """,
]

elim_null_test_cases_targets = [
    """
    S -> S a | a
    """,
    """
    S -> S d | a | X e | e
    X -> X y | g X | d | y | g
    """,
    """
    X -> X Y | X | Y | X e | e | a
    Y -> X Z | X | Z | d | i Y | i
    Z -> g | Y X | Y | X
    """,
    """
    A -> B D | B | D | e | B g | g
    B -> i D | i | j | B u | u
    D -> a D | B | a
    """,
    """
    S -> X Y | Y
    X -> a X b | a b
    Y -> a Y b | Z
    Z -> b Z a | b a
    """,
    """
    S -> X Z | X | Z
    X -> a X b | a b
    Z -> a Z | a | Z X | Z | X
    """,
    """
    S -> A B a b | A a b
    A -> B
    B -> A
    """,
]

elim_unit_test_cases = [
    """
    A -> A a | b | B
    B -> e | u B
    """,
    """
    A -> B d | a A | B
    B -> a | d B | C
    C -> e | A | g C
    """,
    """
    A -> a D | e | B | i
    B -> j | u B | A | C
    C -> i | h C | D
    D -> e | C
    """,
    """
    S -> A
    A -> B | a b
    B -> C | A B a
    C -> S
    """,
    """
    S -> A | a b
    A -> B | C | b a
    B -> S
    C -> D | A B c
    D -> A
    """,
    """
    S -> A | A A
    A -> B | D
    B -> C | a A
    D -> E | b A B
    E -> D | B c
    C -> S
    """,
    """
    B -> D B | f | D
    C -> e B | i | e
    D -> g C | g
    """,
    """
    S -> X Y
    X -> a
    Y -> Z | b
    Z -> M
    M -> N
    N -> a
    """,
    """
    S -> S + T | T
    T -> T * F | F
    F -> ( S ) | a
    """,
    """
    S -> A a | B
    A -> b | B
    B -> A | a
    """,
    """
    S -> X A | a | c
    Y -> a | c | X A
    X -> c | X A
    A -> b
    """,
]

elim_unit_test_cases_targets = [
    """
    A -> A a | b | e | u B
    B -> e | u B
    """,
    """
    A -> A d | a A | a | d A | e | g A
    """,
    """
    A -> a C | e | i | j | u A | h C
    C -> i | h C | e
    """,
    """
    S -> a b | S S a
    """,
    """
    S -> a b | b a | S S c
    """,
    """
    S -> S S | a S | b S S | S c
    D -> b S S | S c
    """,
    """
    B -> D B | f | g C | g
    C -> e B | i | e
    D -> g C | g
    """,
    """
    S -> X Y
    X -> a
    Y -> a | b
    """,
    """
    S -> S + T | T * F | ( S ) | a
    T -> T * F | ( S ) | a
    F -> ( S ) | a
    """,
    """
    S -> A a | b | a
    A -> b | a
    """,
    """
    S -> X A | a | c
    X -> c | X A
    A -> b
    """,
]

# is_nullable tests cases which checks if the non-terminal is nullable
# all the test cases check for the nullability of S

is_nullable_test_cases = [
    """
    S -> a | eps
    """,
    """
    S -> A
    A -> a | eps
    """,
    """
    S -> A S e | eps
    A -> eps
    """,
    """
    S -> A S
    A -> eps
    """,
    """
    S -> A
    A -> B
    B -> C
    C -> A | S
    """,
    """
    S -> A
    A -> F
    F -> eps
    """,
    """
    S -> A
    A -> F X
    F -> e
    X -> eps
    """,
    """
    S -> A
    A -> F X
    F -> e | eps
    X -> eps
    """,
    """
    S -> A
    A -> A | F
    F -> d | F
    """,
    """
    S -> A
    A -> X
    X -> S | L F
    L -> L | eps
    F -> eps
    """,
    """
    S -> A S e | F L
    F -> S
    L -> X
    X -> L | eps
    """,
    """
    S -> a b A
    A -> b c | eps
    """,
    """
    S -> F G | S
    F -> F | G a
    G -> F | S | G | eps
    """,
]


is_nullable_test_cases_targets = [
    True,
    True,
    True,
    False,
    False,
    True,
    False,
    True,
    False,
    True,
    False,
    False,
    False,
]

# --
# first & follow set compute tests cases
# The first symbol appearing the grammar is the start symbol for follow_sets compute

first_follow_set_test_cases = [
    """
    S -> a
    """,
    """
    S -> A
    A -> a
    """,
    """
    S -> A | eps
    A -> a
    """,
    """
    S -> A | eps
    A -> a A
    """,
    """
    S -> A b | eps
    A -> a | eps
    """,
    """
    S -> A B c | eps
    A -> a | eps
    B -> b | eps
    """,
    """
    S -> A B | eps
    A -> a | eps
    B -> b | eps
    """,
    """
    S -> A B | B c
    A -> a | eps
    B -> b | eps
    """,
    """
    S -> A B | B c
    A -> B | B a | eps
    B -> b | eps
    """,
    """
    S -> A B | B c
    A -> B a | B
    B -> b | eps
    """,
    """
    S -> A B | B c
    A -> B a
    B -> b | eps
    """,
    """
    S -> A b C | B C | C
    A -> a b C | B C | eps
    B -> b c
    C -> c | eps
    """,
    """
    S -> A b C | B C | C
    A -> a b S | S B C | eps
    B -> b c S
    C -> c S | eps
    """,
    """
    S -> b A S B | b A
    A -> d S c a | e
    B -> c A a | c
    """,
    """
    E -> T E_
    E_ -> + T E_ | eps
    T -> P T_
    T_ -> * P T_ | eps
    P -> ( E ) | a
    """,
    """
    E -> T X
    X -> + E | eps
    T -> i Y | ( E )
    Y -> * T | eps
    """,
    """
    X -> a X | g | Y Z | eps
    Y -> d | u Y | eps
    Z -> i | eps
    """,
    """
    S -> C B h | a D
    B -> D B | f | eps
    C -> e B | i | eps
    D -> g C | eps
    """,
    """
    E -> T E'
    E' -> + T E' | eps
    T -> F T'
    T' -> * F T' | eps
    F -> ( E ) | id
    """,
    """
    S -> A a
    A -> B D
    B -> b | eps
    D -> d | eps
    """,
    """
    C -> P F class id X Y
    P -> public | eps
    F -> final | eps
    X -> extends id | eps
    Y -> implements I | eps
    I -> id J
    J -> , I | eps
    """,
    """
    PROG -> STMT
    STMT -> if EXPR then BLOCK | while EXPR do BLOCK | EXPR ;
    EXPR -> TERM => id | iszero? TERM | not EXPR | ++ id | -- id
    TERM -> id | const
    BLOCK -> STMT | { STMTS }
    STMTS -> STMT STMTS | eps
    """,
    """
    S -> b A S B | b A
    A -> d S c a | e
    B -> c A a | c
    """,
    """
    S -> A b C | B C | C
    A -> a B S | S B C | C S
    B -> B a C | eps
    C -> c S | eps
    """,
]

first_set_test_cases_targets = [
    {"S": set(["a"])},
    {"S": set(["a"]), "A": set(["a"])},
    {"S": set(["a", "eps"]), "A": set(["a"])},
    {"S": set(["a", "eps"]), "A": set(["a"])},
    {"S": set(["a", "b", "eps"]), "A": set(["a", "eps"])},
    {"S": set(["a", "b", "c", "eps"]), "A": set(["a", "eps"]), "B": set(["b", "eps"])},
    {"S": set(["a", "b", "eps"]), "A": set(["a", "eps"]), "B": set(["b", "eps"])},
    {"S": set(["a", "b", "c", "eps"]), "A": set(["a", "eps"]), "B": set(["b", "eps"])},
    {
        "S": set(["a", "b", "c", "eps"]),
        "A": set(["a", "b", "eps"]),
        "B": set(["b", "eps"]),
    },
    {
        "S": set(["a", "b", "c", "eps"]),
        "A": set(["a", "b", "eps"]),
        "B": set(["b", "eps"]),
    },
    {"S": set(["a", "b", "c"]), "A": set(["a", "b"]), "B": set(["b", "eps"])},
    {
        "S": set(["a", "b", "c", "eps"]),
        "A": set(["a", "b", "eps"]),
        "B": set(["b"]),
        "C": set(["c", "eps"]),
    },
    {
        "S": set(["a", "b", "c", "eps"]),
        "A": set(["a", "b", "c", "eps"]),
        "B": set(["b"]),
        "C": set(["c", "eps"]),
    },
    {"S": set(["b"]), "A": set(["d", "e"]), "B": set(["c"])},
    {
        "E_": set(["+", "eps"]),
        "T_": set(["*", "eps"]),
        "P": set(["(", "a"]),
        "T": set(["(", "a"]),
        "E": set(["(", "a"]),
    },
    {
        "X": set(["+", "eps"]),
        "T": set(["i", "("]),
        "Y": set(["*", "eps"]),
        "E": set(["i", "("]),
    },
    {
        "X": set(["a", "g", "eps", "d", "u", "i"]),
        "Y": set(["d", "u", "eps"]),
        "Z": set(["i", "eps"]),
    },
    {
        "S": set(["a", "e", "i", "f", "h", "g"]),
        "B": set(["f", "eps", "g"]),
        "C": set(["e", "i", "eps"]),
        "D": set(["g", "eps"]),
    },
    {
        "E'": set(["+", "eps"]),
        "T'": set(["*", "eps"]),
        "F": set(["(", "id"]),
        "T": set(["(", "id"]),
        "E": set(["(", "id"]),
    },
    {
        "S": set(["b", "d", "a"]),
        "A": set(["b", "d", "eps"]),
        "B": set(["b", "eps"]),
        "D": set(["d", "eps"]),
    },
    {
        "C": set(["public", "final", "class"]),
        "P": set(["public", "eps"]),
        "F": set(["final", "eps"]),
        "X": set(["extends", "eps"]),
        "Y": set(["implements", "eps"]),
        "I": set(["id"]),
        "J": set([",", "eps"]),
    },
    {
        "PROG": set(["if", "while", "id", "const", "iszero?", "not", "++", "--"]),
        "STMT": set(["if", "while", "id", "const", "iszero?", "not", "++", "--"]),
        "EXPR": set(["id", "const", "iszero?", "not", "++", "--"]),
        "TERM": set(["id", "const"]),
        "BLOCK": set(["if", "while", "id", "const", "iszero?", "not", "++", "--", "{"]),
        "STMTS": set(
            ["if", "while", "id", "const", "iszero?", "not", "++", "--", "eps"]
        ),
    },
    {"S": set(["b"]), "A": set(["d", "e"]), "B": set(["c"])},
    {
        "S": set(["a", "c", "b", "eps"]),
        "A": set(["a", "c", "b", "eps"]),
        "B": set(["a", "eps"]),
        "C": set(["c", "eps"]),
    },
]

follow_set_test_cases_targets = [
    {"S": set(["$"])},
    {"S": set(["$"]), "A": set(["$"])},
    {"S": set(["$"]), "A": set(["$"])},
    {"S": set(["$"]), "A": set(["$"])},
    {"S": set(["$"]), "A": set(["b"])},
    {"S": set(["$"]), "A": set(["b", "c"]), "B": set(["c"])},
    {"S": set(["$"]), "A": set(["$", "b"]), "B": set(["$"])},
    {"S": set(["$"]), "A": set(["b", "$"]), "B": set(["$", "c"])},
    {"S": set(["$"]), "A": set(["b", "$"]), "B": set(["$", "c", "b", "a"])},
    {"S": set(["$"]), "A": set(["b", "$"]), "B": set(["$", "c", "b", "a"])},
    {"S": set(["$"]), "A": set(["b", "$"]), "B": set(["$", "c", "a"])},
    {"S": set(["$"]), "A": set(["b"]), "B": set(["$", "c", "b"]), "C": set(["$", "b"])},
    {
        "S": set(["$", "c", "b"]),
        "A": set(["b"]),
        "B": set(["$", "c", "b"]),
        "C": set(["$", "b", "c"]),
    },
    {"S": set(["$", "c"]), "A": set(["b", "$", "c", "a"]), "B": set(["$", "c"]),},
    # TODO: solve more test cases from
    # first_follow_set_test_cases
]
