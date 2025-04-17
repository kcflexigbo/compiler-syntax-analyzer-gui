from tkinter import filedialog
import pandas as pd
from analyzer import *
from tkinter import simpledialog, messagebox
import tkinter as tk

INTEGER = 'INTEGER'
IDENTIFIER = 'ID'


class Grammar:
    def __init__(self, filename):
        self.conflicts: list[list[int | list[Closure]]] | None = None
        self.error = False
        self.follow_sets: dict | None = None
        self.first_sets: dict | None = None
        self.columns_goto_table = None
        self.columns_action_table = None
        self.goto_table = None
        self.action_table = None
        self.allclosures: dict | None = None
        self.filename = filename
        self.nonTerminals = None
        self.terminals = None
        self.productions = None
        self.slrtable: list[list[action | None]] | None = None
        self.productionslist: list[production] | None = None
        self.enable_integers = False
        self.enable_identifiers = False
        self.keywordList: list[str] = []
        self.symbolList: list[str] = []
        self.readproductionsfromfile()
        self.get_keyword_and_symbol_lists()
        self.constructslrtable()
        self.action_parsing_table = pd.DataFrame(self.action_table, columns=self.columns_action_table)
        self.goto_parsing_table = pd.DataFrame(self.goto_table, columns=self.columns_goto_table)

    def readproductionsfromfile(self, filename: str | None=None):
        if filename:
            if not filename.endswith(".txt"):
                return NameError("Please Ensure that the file is a text file")
        else:
            if not self.filename.endswith(".txt"):
                return NameError("Please Ensure that the file is a text file")
            filename = self.filename
        try:
            production_file = open(filename, 'r')
            productionfilelist = production_file.readlines()
            production_file.close()
            productionslist = [prod.strip().split("->") for prod in productionfilelist]
            productionslist = [[x, y.strip().split(" ")] for x, y in productionslist]
        except Exception as e:
            return Exception(e)

        self.nonTerminals = set()
        for head, body in productionslist:
            self.nonTerminals.add(head)
        self.nonTerminals: list[str] = list(self.nonTerminals)

        self.terminals = set()
        for head, body in productionslist:
            for term in body:
                if term not in self.nonTerminals:
                    self.terminals.add(term)
        self.terminals: list[str] = list(self.terminals)

        if IDENTIFIER in self.terminals:
            self.enable_identifiers = True
        if INTEGER in self.terminals:
            self.enable_integers = True

        nonTerminalsDict = dict()
        for nonTerminal in self.nonTerminals:
            nonTerminalsDict[nonTerminal] = production(nonTerminal)

        TerminalsDict = dict()
        for terminal in self.terminals:
            TerminalsDict[terminal] = Terminal(terminal)

        self.productions = dict()
        self.productionslist = []
        for head, body in productionslist:
            if head not in self.productions:
                self.productions[head] = []

            new_list = []
            for term in body:
                if term in self.nonTerminals:
                    new_list.append(nonTerminalsDict[term])
                elif term in self.terminals:
                    new_list.append(TerminalsDict[term])
                else:
                    return Exception(f"{term} not in the grammar. "
                                     f"This should be a programming error."
                                     "Please Report Immediately")
            new_prod = production(head, pr_body=new_list)
            self.productionslist.append(new_prod)
            self.productions[head].append(new_prod)

    def get_keyword_and_symbol_lists(self):
        for terminal in self.terminals:
            if terminal != INTEGER and terminal != IDENTIFIER:
                if terminal.isalpha():
                    self.keywordList.append(terminal)
                else:
                    self.symbolList.append(terminal)

    def printallproductions(self):
        for key in self.productions.keys():
            for prod in self.productions[key]:
                print(prod)

    def findallclosures(self):
        closures = dict()
        for key in self.productions.keys():
            closures[key] = []
            for prod in self.productions[key]:
                newlist = []
                dotPosition = 0
                while dotPosition < len(prod.body) + 1:
                    if dotPosition == len(prod.body):
                        newlist.append([Closure(prod, dotPosition)])
                    else:
                        newlist.append(self.findclosure(prod, dotPosition))
                    dotPosition += 1
                closures[key].append(newlist)
        self.allclosures = closures
        return closures

    def findclosure(self, prod: production, current: int):
        closure = []
        if isinstance(prod.body[current], Terminal):
            closure.append(Closure(prod, current))
            return closure
        if isinstance(prod.body[current], production):
            closure.append(Closure(prod, current))
            for product in self.productions[repr(prod.body[current])]:
                if repr(product.body[0]) == product.head:
                    if str(Closure(product, 0)) not in [str(x) for x in closure]:
                        closure.append(Closure(product, 0))
                    pass
                else:
                    closure.append(self.findclosure(product, 0))
            closure = flatten_list(closure)
            return closure

    def searchclosure(self):
        production_key = list(self.productions.keys())[0]
        prod = self.productions[production_key][0]
        closure = self.allclosures[repr(prod)][0][0]
        print(closure)

    def findallfirst(self):
        first_sets = dict()
        for key in self.productions.keys():
            first_sets[key] = []
            for prod in self.productions[key]:
                first_sets[key].append(self.findfirst(prod))
            first_sets[key] = flatten_list(first_sets[key])
            first_sets[key] = list(set(first_sets[key]))
        self.first_sets = first_sets
        return first_sets

    def findfirst(self, prod: production) -> list[str] | list[list[str]]:
        firstset = list()
        if isinstance(prod.body[0], Terminal):
            firstset.append(str(prod.body[0]))
            return firstset
        if isinstance(prod.body[0], production):
            for product in self.productions[repr(prod.body[0])]:
                if repr(product.body[0]) == product.head:
                    pass
                else:
                    firstset.append(self.findfirst(product))
            firstset = flatten_list(firstset)
            firstset = list(set(firstset))
            return firstset

    def findallfollow(self):
        self.follow_sets = dict()
        for key in self.productions.keys():
            self.follow_sets[key] = []
            prod_to_check = self.findallcontains(key)
            if key == self.productions[list(self.productions.keys())[0]][0].head:
                self.follow_sets[key].append("#")
            else:
                for each_follow_help in prod_to_check:
                    self.follow_sets[key].append(self.findfollow(each_follow_help))
                self.follow_sets[key] = flatten_list(self.follow_sets[key])
                self.follow_sets[key] = list(set(self.follow_sets[key]))
        return self.follow_sets

    def findallcontains(self, prod_head: str) -> list[follow_helper] | list:
        prod_to_check = []
        for key in self.productions.keys():
            for prod in self.productions[key]:
                if prod.checkcontains(prod_head) is not None:
                    prod_to_check.append(follow_helper(prod, prod.checkcontains(prod_head)))
        return prod_to_check

    def findfollow(self, follow_help: follow_helper) -> list[str]:
        if isinstance(follow_help.getafter(), Terminal):
            return [str(follow_help.getafter())]
        if isinstance(follow_help.getafter(), str):
            if follow_help.prod.head == repr(follow_help):
                return []
            elif follow_help.prod.head in self.follow_sets.keys():
                return self.follow_sets[follow_help.prod.head]
            else:
                key = follow_help.prod.head
                self.follow_sets[key] = []
                prod_to_check = self.findallcontains(key)
                for each_follow_help in prod_to_check:
                    self.follow_sets[key].append(self.findfollow(each_follow_help))
                return []
        if isinstance(follow_help.getafter(), production):
            return self.findfirst(follow_help.getafter())

    def constructslrtable(self):
        self.action_table = []
        self.goto_table = []
        done_closures = []
        self.columns_action_table = self.terminals + ["#"]
        self.columns_goto_table: list[str] = self.nonTerminals
        self.columns_goto_table.remove(self.productions[
                                           list(self.productions.keys())[0]][0].head)
        self.findallclosures()
        self.findallfirst()
        self.findallfollow()
        production_key = list(self.productions.keys())[0]
        prod = self.productions[production_key][0]
        closure = self.allclosures[repr(prod)][0][0]
        conflicts = []
        self.construct(closure, done_closures, conflicts)
        self.conflicts = conflicts

    def construct(self, closurelist: list[Closure], done_closures: list[list[Closure]],
                  conflicts: list[list[int | list[Closure]]]):
        try:
            return done_closures.index(closurelist)
        except ValueError:
            done_closures.append(closurelist)

        state_no = len(self.action_table)
        action_table = []
        for _ in self.columns_action_table:
            action_table.append(None)
        self.action_table.append(action_table)

        goto_table = []
        for _ in self.columns_goto_table:
            goto_table.append(None)
        self.goto_table.append(goto_table)

        all_branches = set()
        for closure in closurelist:
            all_branches.add(closure.getcurrent())
        all_branches_dict = dict()
        for branch in all_branches:
            all_branches_dict[branch] = []

        if "END" in list(all_branches_dict.keys()) and len(all_branches_dict.keys()) > 1:
            conflicts.append([state_no, closurelist])
            result = self.verify_slr_capable([state_no, closurelist])
            conflicts[-1].append(result[1])
            if not result[0]:
                messagebox.showerror(title=f"Grammar Error",
                                     message=f"CANNOT CONSTRUCT SLR TABLE AS THERE IS UNRESOLVABLE CONFLICT AT STATE "
                                             f" {state_no}:\n{closurelist}.\n{result[1]}\nPLEASE CHANGE GRAMMAR")
                self.error = True

        for closure in closurelist:
            all_branches_dict[closure.getcurrent()].append(closure)

        for key in all_branches_dict.keys():
            if key == "END":
                for closure in all_branches_dict[key]:
                    if closure.prod.head == self.productions[list(self.productions.keys())[0]][0].head:
                        action_index = self.columns_action_table.index("#")
                        self.action_table[state_no][action_index] = action("ACCEPT")
                    else:
                        indexes_to_insert_str = self.follow_sets[repr(closure.prod)]
                        indexes_to_insert = []
                        for terminal in indexes_to_insert_str:
                            indexes_to_insert.append(self.columns_action_table.index(terminal))
                        prod_index = self.productionslist.index(closure.prod)
                        for index_to_use in indexes_to_insert:
                            self.action_table[state_no][index_to_use] = action("REDUCE", prod_index)
            else:
                current_closures = []
                for closure in all_branches_dict[key]:
                    prod_index = self.productions[closure.prod.head].index(closure.prod)
                    prod = self.productions[closure.prod.head][prod_index]
                    cur_closure = self.allclosures[repr(prod)][prod_index][closure.dotPos + 1]
                    for close in cur_closure:
                        if str(close) not in [str(x) for x in current_closures]:
                            current_closures.append(close)

                if key in self.nonTerminals:
                    key_index = self.columns_goto_table.index(key)
                    self.goto_table[state_no][key_index] = action("MOVE", self.construct(current_closures,
                                                                                         done_closures, conflicts))
                elif key in self.terminals:
                    key_index = self.columns_action_table.index(key)
                    self.action_table[state_no][key_index] = action("SHIFT", self.construct(current_closures,
                                                                                            done_closures, conflicts))
                else:
                    return ValueError
        return state_no

    def verify_slr_capable(self, conflict: list[int | list[Closure]]) -> list[bool | str]:
        all_branches = set()
        for closure in conflict[1]:
            all_branches.add(closure.getcurrent())
        assert all_branches.__contains__("END")
        all_branches_dict = dict()
        for branch in all_branches:
            all_branches_dict[branch] = []
        for closure in conflict[1]:
            all_branches_dict[closure.getcurrent()].append(closure)
        follow_end, first_others = [], []
        for key in all_branches_dict.keys():
            if key == "END":
                follow_end = self.follow_sets[repr(all_branches_dict[key][0].prod)]
            else:
                for closure in all_branches_dict[key]:
                    # print(closure.getcurrent())
                    if isinstance(closure.getcurrentclass(), Terminal):
                        first_others.append(closure.getcurrent())
                    elif isinstance(closure.getcurrentclass(), production):
                        first_others.append(self.first_sets[repr(closure.getcurrent())])
        follow_end = set(flatten_list(follow_end))
        first_others = set((flatten_list(first_others)))
        intersect = follow_end & first_others
        if len(intersect) > 0:
            return [False, f"FOLLOW: {follow_end}, FIRST:{first_others}"]
        # else:
        #     print("Resolved Conflict")
        return [True, f"FOLLOW: {follow_end}, FIRST:{first_others}"]

    def get_conflicts_string(self) -> str:
        conflicts_str = ""
        for conflict in self.conflicts:
            conflicts_str += f"STATE {conflict[0]}: Closures:{conflict[1]}.\n {conflict[2]}" + "\n\n"
        return conflicts_str


def flatten_list(nested_list) -> list:
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result


if __name__ == "__main__":
    grammar = Grammar(filedialog.askopenfilename())
    grammar.readproductionsfromfile()
    allclosures = grammar.findallclosures()
    # print(allclosures.keys())
    # for key in allclosures.keys():
    #     print(f"{key}: ///")
    #     for closure in allclosures[key]:
    #         print(closure)
    #     print("///\n\n")
    # grammar.searchclosure()
    # grammar.constructslrtable()
    # print(grammar.findallfirst())
    # print(grammar.findallfollow())
    action_parsing_table = pd.DataFrame(grammar.action_table, columns=grammar.columns_action_table)
    goto_parsing_table = pd.DataFrame(grammar.goto_table, columns=grammar.columns_goto_table)
    filename = "action_parsing_table.xlsx"
    action_parsing_table.to_excel(filename)

    filename = "goto_parsing_table.xlsx"
    goto_parsing_table.to_excel(filename)
