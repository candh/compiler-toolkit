#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# MIT License
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Usage: compilertk FILE [-o FILE]

Compiler Toolkit

-h --help    show this
-o FILE      specify output file [default: ./output.txt]
"""

BANNER = """
                   _ _            _           _ _   _ _
 ___ ___ _____ ___|_| |___ ___   | |_ ___ ___| | |_|_| |_
|  _| . |     | . | | | -_|  _|  |  _| . | . | | '_| |  _|
|___|___|_|_|_|  _|_|_|___|_|    |_| |___|___|_|_,_|_|_|
              |_|
"""

from docopt import docopt
import colorful as cf

from PyInquirer import prompt, Separator
import os
import sys

# toolkit imports
import toolkit.modules.grammar as gm
from toolkit.modules.elim_null import elim_null
from toolkit.modules.elim_unit import elim_unit, remove_same_rules
from toolkit.modules.elim_left_recursion import elim_lr
from toolkit.modules.make_first_sets import first_sets
from toolkit.modules.make_follow_sets import follow_sets
from toolkit.modules.make_parsing_table import parsing_table


def clear():
    os.system("clear || cls")


def write_to_output(of, header, content):
    """
    writes logs to the output file
    of: output file name
    header: first line to write
    content: subsequent lines
    """
    f = open(of, "a")  # In append mode
    f.write(header + ":\n")
    f.write(content + "\n")
    f.close()


def main():
    args = docopt(__doc__)

    # check if file exits
    if not os.path.exists(args["FILE"]):
        print(cf.red("{} doesn't exist\n".format(args["FILE"])))
        exit(1)

    # create the output file
    of = args["-o"]
    open(of, "w").close()

    f = open(args["FILE"])
    grammar = f.read()
    f.close()

    # clear console
    clear()

    # print banner
    print(cf.yellow_bold(BANNER))

    print(cf.bold_white("Input Grammar:\n"))
    pgrammar = gm.parse(grammar)
    orignal = pgrammar
    gm.pprint(pgrammar)
    print()

    write_to_output(of, "Input Grammar", gm.str_pgrammar(pgrammar))

    choices = [
        "Remove Null Productions",
        "Remove Unit Productions",
        "Remove Left Recursion",
        "First Sets",
        "Follow Sets",
        "Parsing Table",
    ]

    misc_choices = [
        "Restore Original Grammar",
        "Print Current Grammar",
        "Clear",
        "Exit",
    ]

    question = {
        "type": "list",
        "name": "ops",
        "message": "Which operation would you like to perform?",
        "choices": choices + [Separator()] + misc_choices,
    }

    reuse_confirm = {
        "type": "confirm",
        "name": "last_grammar",
        "message": "Use this grammar output for subsequent operations?",
        "default": True,
    }

    reverse_confirm = {
        "type": "confirm",
        "name": "reverse_grammar",
        "message": "Reverse Non-Terminal ordering?",
        "default": True,
    }

    start_input = {
        "type": "input",
        "name": "start_sym",
        "message": "Enter Start Symbol:",
    }

    # will contain the last output
    output = None
    # if last output was a grammar (as opposed to follow sets)
    output_grammar = False

    while True:
        answer = prompt(question)
        choice = answer["ops"]

        if choice == misc_choices[0]:
            pgrammar = orignal
            print(cf.white_bold("\nRestored\n"))
            gm.pprint(pgrammar)
            print()
            write_to_output(of, choice, gm.str_pgrammar(pgrammar))
            continue

        elif choice == misc_choices[1]:
            print()
            gm.pprint(pgrammar)
            print()
            continue

        elif choice == misc_choices[2]:
            clear()
            continue

        if choice == misc_choices[3]:
            print(cf.cyan("Bye!"))
            print("Remember! Logs are saved in", of)
            print()
            break

        # --------

        if choice == choices[0]:
            output = elim_null(pgrammar)

        elif choice == choices[1]:
            output = elim_unit(pgrammar)
            output = remove_same_rules(output, False, False)

        elif choice == choices[2]:
            answer = prompt(reverse_confirm)
            reverse = answer["reverse_grammar"]
            if reverse:
                print(
                    "\nReversing the order of non-terminals for Left Recursion Removal."
                )

                ng = gm.reverse_grammar(pgrammar)
            else:
                ng = pgrammar

            ng = elim_lr(ng)
            if reverse:
                ng = gm.reverse_grammar(ng)
            output = ng

        elif choice == choices[3]:
            fs = first_sets(pgrammar)
            output = fs

        elif choice == choices[4]:
            start_input["validate"] = lambda x: x in pgrammar.keys()
            answer = prompt(start_input)
            fs = first_sets(pgrammar)
            fls = follow_sets(answer["start_sym"], pgrammar, fs)
            output = fls

        elif choice == choices[5]:
            start_input["validate"] = lambda x: x in pgrammar.keys()
            answer = prompt(start_input)
            fs = first_sets(pgrammar)
            fls = follow_sets(answer["start_sym"], pgrammar, fs)

            output = parsing_table(pgrammar, fs, fls)

        if choice != choices[5]:

            # flag to check if the last operation output a pgrammar
            # only the first 3 operations output a grammar
            output_grammar = choices.index(choice) in range(3)

            # print output
            print(cf.bold_green("\n=>\n"))

            (gm.pprint if output_grammar else gm.set_print)(output)

            # log to the output file
            write_to_output(
                of, choice, (gm.str_pgrammar if output_grammar else gm.str_set)(output),
            )

            print()

            # ask to use grammar from last operation
            if output_grammar:
                answer = prompt(reuse_confirm)
                if answer["last_grammar"]:
                    pgrammar = output

        else:
            # print parsing table
            print("\n" + output + "\n")
            write_to_output(
                of, choice, output,
            )


if __name__ == "__main__":
    main()
