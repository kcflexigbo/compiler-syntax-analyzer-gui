# import tkinter as tk
import time

from mttkinter import mtTkinter as tk
from tkinter import ttk, Text
from tkinter import messagebox
import threading
import queue
from analyzer import *
from filesbrowser import *
import pandastable as pdt
import multiprocessing as mp
from slrgenerator import *


def initGUI(root):
    style = ttk.Style()
    style.configure('blue.TSeparator', background='blue')
    style.configure('yellow.TSeparator', background='yellow')
    style.configure('red.TSeparator', background='red')

    root.geometry('1620x920')
    # root.attributes("-zoomed", True)
    root.state("zoomed")
    root.title("Lexical Analyzer")
    root.configure(bg="grey")

    lb1 = tk.Label(root, text="Editor:", font=('Arial', 14))
    lb1.place(relx=0.02, rely=0.02)
    lb1.configure(background="grey")

    input_frame = tk.Frame(root)
    input_frame.place(relx=0.02, rely=0.05, relheight=0.9, relwidth=0.15)

    global input_textbox
    input_textbox = tk.Text(input_frame, font=("Helvetica", 15))
    input_vert_sb = tk.Scrollbar(input_frame)
    input_vert_sb.pack(side=tk.RIGHT, fill=tk.BOTH)
    input_textbox.config(yscrollcommand=input_vert_sb.set)
    input_vert_sb.config(command=input_textbox.yview)

    input_textbox.pack(fill="both", expand=True)

    vsep_1 = ttk.Separator(root, orient='vertical', style='blue.TSeparator')
    vsep_1.place(relx=0.194, rely=0, relheight=1, relwidth=0.005)

    lb2 = tk.Label(root, text="Output Lexemes:", font=('Arial', 14))
    lb2.place(relx=0.22, rely=0.02)
    lb2.configure(background="grey")

    output_frame = tk.Frame(root)
    output_frame.place(relx=0.22, rely=0.05, relheight=0.9, relwidth=0.1)

    global output_textbox
    output_textbox = tk.Text(output_frame, font=("Comic Sans MS", 15))
    output_vert_sb = tk.Scrollbar(output_frame)
    output_vert_sb.pack(side=tk.RIGHT, fill=tk.BOTH)
    output_textbox.config(yscrollcommand=output_vert_sb.set)
    output_vert_sb.config(command=output_textbox.yview)

    output_textbox.pack(fill="both", expand=True)
    output_textbox.config(state="disabled")

    vsep_2 = ttk.Separator(root, orient='vertical', style='yellow.TSeparator')
    vsep_2.place(relx=0.34, rely=0, relheight=1, relwidth=0.005)

    lb3 = tk.Label(root, text="Symbol Tables:", font=('Arial', 14))
    lb3.place(relx=0.36, rely=0.02, relheight=0.025)
    lb3.configure(background="grey")

    lb4 = tk.Label(root, text="Variable / Identifier Table:", font=('Arial', 14))
    lb4.place(relx=0.36, rely=0.075, relheight=0.025)
    lb4.configure(background="grey")

    variable_frame = tk.Frame(root)
    variable_frame.place(relx=0.36, rely=0.105, relheight=0.4, relwidth=0.15)

    global variable_textbox
    variable_textbox = tk.Text(variable_frame, font=("Comic Sans MS", 15))
    variable_vert_sb = tk.Scrollbar(variable_frame)
    variable_vert_sb.pack(side=tk.RIGHT, fill=tk.BOTH)
    variable_textbox.config(yscrollcommand=variable_vert_sb.set)
    variable_vert_sb.config(command=variable_textbox.yview)

    variable_textbox.pack(fill="both", expand=True)
    variable_textbox.config(state="disabled")

    lb5 = tk.Label(root, text="Constant Table:", font=('Arial', 14))
    lb5.place(relx=0.36, rely=0.52, relheight=0.025)
    lb5.configure(background="grey")

    constant_frame = tk.Frame(root)
    constant_frame.place(relx=0.36, rely=0.55, relheight=0.4, relwidth=0.15)

    global constant_textbox
    constant_textbox = tk.Text(constant_frame, font=("Comic Sans MS", 15))
    constant_vert_sb = tk.Scrollbar(constant_frame)
    constant_vert_sb.pack(side=tk.RIGHT, fill=tk.BOTH)
    constant_textbox.config(yscrollcommand=constant_vert_sb.set)
    constant_vert_sb.config(command=constant_textbox.yview)

    constant_textbox.pack(fill="both", expand=True)
    constant_textbox.config(state="disabled")

    pausebtn = tk.Button(root, text="Pause Detection and Analysis", font=('Arial', 14),
                         command=pauseDetection)
    pausebtn.place(relx=0.36, rely=0.96)

    global savebtn
    savebtn = tk.Button(root, text="Save Files", font=('Arial', 14), command=saveWindow)
    savebtn.place(relx=0.56, rely=0.96)

    vsep_2 = ttk.Separator(root, orient='vertical', style='red.TSeparator')
    vsep_2.place(relx=0.53, rely=0, relheight=1, relwidth=0.005)

    lb6 = tk.Label(root, text="Parsing Steps:", font=('Arial', 14))
    lb6.place(relx=0.55, rely=0.02, relheight=0.025)
    lb6.configure(background="grey")

    parsing_steps_frame = tk.Frame(root)
    parsing_steps_frame.place(relx=0.55, rely=0.05, relheight=0.9, relwidth=0.44)

    global parsing_steps_table
    parsing_steps_table = pdt.Table(parsing_steps_frame, dataframe=output_table)
    parsing_steps_table.show()

    global grammar
    grammar = None

    global display_parsing_trees_btn
    display_parsing_trees_btn = tk.Button(root, text="Display Grammar Properties", font=('Arial', 14),
                                          command=display_trees)
    display_parsing_trees_btn.place(relx=0.68, rely=0.96)

    global display_productions_btn
    display_productions_btn = tk.Button(root, text="Display Productions", font=('Arial', 14), command=display_prods)
    display_productions_btn.place(relx=0.2, rely=0.96)
    start_select_grammar_thread()

    global select_grammar_btn
    select_grammar_btn = tk.Button(root, text="Select Grammar", font=('Arial', 14), command=start_select_grammar_thread)
    select_grammar_btn.place(relx=0.05, rely=0.96)


def pauseDetection():
    global paused
    if not paused:
        insert_event = event.wait
        instruction_queue.put(insert_event)
    else:
        event.set()
        event.clear()
    paused = not paused


def new_window_on_closing():
    savebtn.config(state="normal")
    new_window.destroy()


def trees_window_on_closing(archaic_list):
    for iter in range(len(archaic_list)):
        if archaic_list[iter] == 1:
            if iter == 0:
                action_table_window.focus_set()
                action_table_window.bell()
            elif iter == 1:
                goto_table_window.focus_set()
                goto_table_window.bell()
            elif iter == 2:
                closure_sets_window.focus_set()
                closure_sets_window.bell()
            elif iter == 3:
                terminals_window.focus_set()
                terminals_window.bell()
            elif iter == 4:
                non_terminals_window.focus_set()
                non_terminals_window.bell()
            elif iter == 5:
                first_sets_window.focus_set()
                first_sets_window.bell()
            elif iter == 6:
                follow_sets_window.focus_set()
                follow_sets_window.bell()
            elif iter == 7:
                conflicts_window.focus_set()
                conflicts_window.bell()
            return
    display_parsing_trees_btn.config(state="normal")
    trees_window.destroy()


def display_trees():
    global trees_window, display_closures_btn, display_terminals_btn, display_non_terminals_btn, display_first_btn
    display_parsing_trees_btn.config(state="disabled")
    trees_window = tk.Toplevel(root)
    trees_window.title("Select Option: ")
    trees_window.geometry("250x600")
    trees_window.protocol("WM_DELETE_WINDOW", lambda: trees_window_on_closing(archaic_list))
    archaic_list = [0, 0, 0, 0, 0, 0, 0, 0]

    global display_action_table_btn, display_goto_table_btn, display_follow_btn, display_conflicts_btn
    display_action_table_btn = tk.Button(trees_window, text="Display Action Table", font=('Arial', 14),
                                         command=lambda: display_action_table(archaic_list))
    display_goto_table_btn = tk.Button(trees_window, text="Display Goto Table", font=('Arial', 14),
                                       command=lambda: display_goto_table(archaic_list))
    display_closures_btn = tk.Button(trees_window, text="Display Closures",
                                     font=('Arial', 14), command=lambda: display_closure_sets(archaic_list))
    display_terminals_btn = tk.Button(trees_window, text="Display Terminals", font=('Arial', 14),
                                      command=lambda: display_terminals(archaic_list))
    display_non_terminals_btn = tk.Button(trees_window, text="Display Non Terminals", font=('Arial', 14),
                                          command=lambda: display_non_terminals(archaic_list))
    display_first_btn = tk.Button(trees_window, text="Display First Sets", font=('Arial', 14),
                                  command=lambda: display_first_sets(archaic_list))
    display_follow_btn = tk.Button(trees_window, text="Display Follow Sets", font=('Arial', 14),
                                   command=lambda: display_follow_sets(archaic_list))
    display_conflicts_btn = tk.Button(trees_window, text="Display Conflicts", font=('Arial', 14),
                                   command=lambda: display_conflicts(archaic_list))

    display_action_table_btn.place(relx=0.1, rely=0.02, relheight=0.1, relwidth=0.8)
    display_goto_table_btn.place(relx=0.1, rely=0.14, relheight=0.1, relwidth=0.8)
    display_closures_btn.place(relx=0.1, rely=0.26, relheight=0.1, relwidth=0.8)
    display_terminals_btn.place(relx=0.1, rely=0.38, relheight=0.1, relwidth=0.8)
    display_non_terminals_btn.place(relx=0.1, rely=0.50, relheight=0.1, relwidth=0.8)
    display_first_btn.place(relx=0.1, rely=0.62, relheight=0.1, relwidth=0.8)
    display_follow_btn.place(relx=0.1, rely=0.74, relheight=0.1, relwidth=0.8)
    display_conflicts_btn.place(relx=0.1, rely=0.86, relheight=0.1, relwidth=0.8)


def display_terminals(archaic_list):
    global terminals_window, grammar
    display_terminals_btn.config(state="disabled")
    terminals_window = tk.Toplevel(root)
    terminals_window.title("All Terminals: ")
    terminals_window.geometry("300x350")
    terminals_window.protocol("WM_DELETE_WINDOW", lambda: terminals_window_on_closing(archaic_list))
    archaic_list[3] = 1
    terminals_str = get_terminals_string()

    terminals_frame = tk.Frame(terminals_window)
    terminals_frame.place(relx=0, rely=0, relheight=1, relwidth=1)

    global terminals_textbox
    terminals_textbox = tk.Text(terminals_frame, font=("Comic Sans MS", 15))
    terminals_vert_sb = tk.Scrollbar(terminals_frame)
    terminals_vert_sb.pack(side=tk.RIGHT, fill=tk.BOTH)
    terminals_textbox.config(yscrollcommand=terminals_vert_sb.set)
    terminals_vert_sb.config(command=terminals_textbox.yview)

    terminals_textbox.pack(fill="both", expand=True)
    terminals_textbox.insert(tk.END, terminals_str)
    terminals_textbox.config(state="disabled")


def terminals_window_on_closing(archaic_list):
    display_terminals_btn.config(state="normal")
    archaic_list[3] = 0
    terminals_window.destroy()


def display_non_terminals(archaic_list):
    global non_terminals_window, grammar
    display_non_terminals_btn.config(state="disabled")
    non_terminals_window = tk.Toplevel(root)
    non_terminals_window.title("All Non Terminals: ")
    non_terminals_window.geometry("300x350")
    non_terminals_window.protocol("WM_DELETE_WINDOW", lambda: non_terminals_window_on_closing(archaic_list))
    archaic_list[4] = 1
    non_terminals_str = get_non_terminals_string()

    non_terminals_frame = tk.Frame(non_terminals_window)
    non_terminals_frame.place(relx=0, rely=0, relheight=1, relwidth=1)

    global non_terminals_textbox
    non_terminals_textbox = tk.Text(non_terminals_frame, font=("Comic Sans MS", 15))
    non_terminals_vert_sb = tk.Scrollbar(non_terminals_frame)
    non_terminals_vert_sb.pack(side=tk.RIGHT, fill=tk.BOTH)
    non_terminals_textbox.config(yscrollcommand=non_terminals_vert_sb.set)
    non_terminals_vert_sb.config(command=non_terminals_textbox.yview)

    non_terminals_textbox.pack(fill="both", expand=True)
    non_terminals_textbox.insert(tk.END, non_terminals_str)
    non_terminals_textbox.config(state="disabled")


def non_terminals_window_on_closing(archaic_list):
    display_non_terminals_btn.config(state="normal")
    archaic_list[4] = 0
    non_terminals_window.destroy()


def display_first_sets(archaic_list):
    global first_sets_window, grammar
    display_first_btn.config(state="disabled")
    first_sets_window = tk.Toplevel(root)
    first_sets_window.title("All First Sets: ")
    first_sets_window.geometry("500x350")
    first_sets_window.protocol("WM_DELETE_WINDOW", lambda: first_sets_window_on_closing(archaic_list))
    archaic_list[5] = 1
    first_str = get_first_set_string()

    first_frame = tk.Frame(first_sets_window)
    first_frame.place(relx=0, rely=0, relheight=1, relwidth=1)

    global first_textbox
    first_textbox = tk.Text(first_frame, font=("Comic Sans MS", 15))
    first_vert_sb = tk.Scrollbar(first_frame)
    first_vert_sb.pack(side=tk.RIGHT, fill=tk.BOTH)
    first_textbox.config(yscrollcommand=first_vert_sb.set)
    first_vert_sb.config(command=first_textbox.yview)

    first_textbox.pack(fill="both", expand=True)
    first_textbox.insert(tk.END, first_str)
    first_textbox.config(state="disabled")


def first_sets_window_on_closing(archaic_list):
    display_first_btn.config(state="normal")
    archaic_list[5] = 0
    first_sets_window.destroy()


def display_follow_sets(archaic_list):
    global follow_sets_window, grammar
    display_follow_btn.config(state="disabled")
    follow_sets_window = tk.Toplevel(root)
    follow_sets_window.title("All Follow Sets: ")
    follow_sets_window.geometry("500x350")
    follow_sets_window.protocol("WM_DELETE_WINDOW", lambda: follow_sets_window_on_closing(archaic_list))
    archaic_list[6] = 1
    follow_str = get_follow_sets_str()

    follow_frame = tk.Frame(follow_sets_window)
    follow_frame.place(relx=0, rely=0, relheight=1, relwidth=1)

    global follow_textbox
    follow_textbox = tk.Text(follow_frame, font=("Comic Sans MS", 15))
    follow_vert_sb = tk.Scrollbar(follow_frame)
    follow_vert_sb.pack(side=tk.RIGHT, fill=tk.BOTH)
    follow_textbox.config(yscrollcommand=follow_vert_sb.set)
    follow_vert_sb.config(command=follow_textbox.yview)

    follow_textbox.pack(fill="both", expand=True)
    follow_textbox.insert(tk.END, follow_str)
    follow_textbox.config(state="disabled")


def follow_sets_window_on_closing(archaic_list):
    display_follow_btn.config(state="normal")
    archaic_list[6] = 0
    follow_sets_window.destroy()


def display_closure_sets(archaic_list):
    global closure_sets_window, grammar
    display_closures_btn.config(state="disabled")
    closure_sets_window = tk.Toplevel(root)
    closure_sets_window.title("All Closure Sets: ")
    closure_sets_window.geometry("500x350")
    closure_sets_window.protocol("WM_DELETE_WINDOW", lambda: closure_window_on_closing(archaic_list))
    archaic_list[2] = 1
    closure_str = get_closure_string()

    closure_frame = tk.Frame(closure_sets_window)
    closure_frame.place(relx=0, rely=0, relheight=1, relwidth=1)

    global closure_textbox
    closure_textbox = tk.Text(closure_frame, font=("Comic Sans MS", 15))
    closure_vert_sb = tk.Scrollbar(closure_frame)
    closure_vert_sb.pack(side=tk.RIGHT, fill=tk.BOTH)
    closure_textbox.config(yscrollcommand=closure_vert_sb.set)
    closure_vert_sb.config(command=closure_textbox.yview)

    closure_textbox.pack(fill="both", expand=True)
    closure_textbox.insert(tk.END, closure_str)
    closure_textbox.config(state="disabled")


def closure_window_on_closing(archaic_list):
    display_closures_btn.config(state="normal")
    archaic_list[2] = 0
    closure_sets_window.destroy()


def display_prods():
    global prods_window, grammar
    display_productions_btn.config(state="disabled")
    prods_window = tk.Toplevel(root)
    prods_window.title("All Productions: ")
    prods_window.geometry("300x350")
    prods_window.protocol("WM_DELETE_WINDOW", lambda: prods_window_on_closing())
    prod_str = ""
    for i in grammar.productionslist:
        prod_str += str(i) + "\n"

    productions_frame = tk.Frame(prods_window)
    productions_frame.place(relx=0, rely=0, relheight=1, relwidth=1)

    global productions_textbox
    productions_textbox = tk.Text(productions_frame, font=("Comic Sans MS", 15))
    productions_vert_sb = tk.Scrollbar(productions_frame)
    productions_vert_sb.pack(side=tk.RIGHT, fill=tk.BOTH)
    productions_textbox.config(yscrollcommand=productions_vert_sb.set)
    productions_vert_sb.config(command=productions_textbox.yview)

    productions_textbox.pack(fill="both", expand=True)
    productions_textbox.insert(tk.END, prod_str)
    productions_textbox.config(state="disabled")


def prods_window_on_closing():
    display_productions_btn.config(state="normal")
    prods_window.destroy()


def display_conflicts(archaic_list):
    global conflicts_window, grammar
    display_conflicts_btn.config(state="disabled")
    conflicts_window = tk.Toplevel(root)
    conflicts_window.title("All Conflicts: ")
    conflicts_window.geometry("500x350")
    conflicts_window.protocol("WM_DELETE_WINDOW", lambda: conflicts_window_on_closing(archaic_list))
    archaic_list[7] = 1
    conflicts_str = grammar.get_conflicts_string()

    conflicts_frame = tk.Frame(conflicts_window)
    conflicts_frame.place(relx=0, rely=0, relheight=1, relwidth=1)

    global conflicts_textbox
    conflicts_textbox = tk.Text(conflicts_frame, font=("Comic Sans MS", 15))
    conflicts_vert_sb = tk.Scrollbar(conflicts_frame)
    conflicts_vert_sb.pack(side=tk.RIGHT, fill=tk.BOTH)
    conflicts_textbox.config(yscrollcommand=conflicts_vert_sb.set)
    conflicts_vert_sb.config(command=conflicts_textbox.yview)

    conflicts_textbox.pack(fill="both", expand=True)
    conflicts_textbox.insert(tk.END, conflicts_str)
    conflicts_textbox.config(state="disabled")


def conflicts_window_on_closing(archaic_list):
    display_conflicts_btn.config(state="normal")
    archaic_list[7] = 0
    conflicts_window.destroy()

def action_table_window_on_closing(archaic_list):
    display_action_table_btn.config(state="normal")
    archaic_list[0] = 0
    action_table_window.destroy()


def goto_table_window_on_closing(archaic_list):
    display_goto_table_btn.config(state="normal")
    archaic_list[1] = 0
    goto_table_window.destroy()


def display_action_table(archaic_list):
    display_action_table_btn.config(state="disabled")
    archaic_list[0] = 1
    global action_table_window
    display_action_table_btn.config(state="disabled")
    action_table_window = tk.Toplevel(root)
    action_table_window.title("Action Table")
    action_table_window.geometry("1050x450")
    action_table_window.protocol("WM_DELETE_WINDOW", lambda: action_table_window_on_closing(archaic_list))

    action_table = pdt.Table(action_table_window, dataframe=grammar.action_parsing_table)
    action_table.show()


def display_goto_table(archaic_list):
    display_goto_table_btn.config(state="disabled")
    archaic_list[1] = 1
    global goto_table_window
    display_goto_table_btn.config(state="disabled")
    goto_table_window = tk.Toplevel(root)
    goto_table_window.title("Goto Table")
    goto_table_window.geometry("500x450")
    goto_table_window.protocol("WM_DELETE_WINDOW", lambda: goto_table_window_on_closing(archaic_list))

    goto_table = pdt.Table(goto_table_window, dataframe=grammar.goto_parsing_table)
    goto_table.show()


def saveWindow():
    global new_window
    savebtn.config(state="disabled")
    new_window = tk.Toplevel()
    new_window.title("Save Files")
    new_window.geometry("250x80")
    new_window.protocol("WM_DELETE_WINDOW", new_window_on_closing)

    lb1 = tk.Label(new_window, text="Enter the Name of the project to be saved as", font=('Arial', 10))
    lb1.place(relx=0.02, rely=0.02)

    inp1 = tk.StringVar()
    inp1_entry = tk.Entry(new_window, textvariable=inp1)
    inp1_entry.place(relx=0.1, rely=0.3, relwidth=0.8)

    confirmbtn = tk.Button(new_window, text="Save", command=lambda: saveFiles_process_create(inp1.get().strip()))
    confirmbtn.place(relx=0.2, rely=0.6, relwidth=0.6)


def get_closure_string() -> str:
    global grammar
    closure_str = ""
    for key in grammar.allclosures.keys():
        closure_str += f"Closure({key}): < \n"
        for eachList in grammar.allclosures[key]:
            index = grammar.allclosures[key].index(eachList)
            closure_str += f"Grammar {index}: [ "
            for List in eachList:
                index2 = eachList.index(List)
                closure_str += f"\nPos {index2}: " + "{ "
                for term in List:
                    closure_str += str(term) + ", "
                closure_str += "} \n"
            closure_str += "] \n"
        closure_str += " >\n\n"
    return closure_str


def get_terminals_string()-> str:
    global grammar
    terminals_str=""
    for terminal in grammar.terminals:
        terminals_str += str(terminal) + "\n"
    return  terminals_str

def get_non_terminals_string() ->str:
    global grammar
    non_terminals_str = ""
    for non_terminal in grammar.nonTerminals:
        non_terminals_str += str(non_terminal) + "\n"
    return non_terminals_str

def get_first_set_string() -> str:
    global grammar
    first_str = ""
    for key in grammar.first_sets.keys():
        first_str += f"First({key}): < "
        for term in grammar.first_sets[key]:
            first_str += str(term) + ", "
        first_str += " >\n\n"
    return first_str

def get_follow_sets_str() -> str:
    global grammar
    follow_str = ""
    for key in grammar.follow_sets.keys():
        follow_str += f"Follow({key}): < "
        for term in grammar.follow_sets[key]:
            follow_str += str(term) + ", "
        follow_str += " >\n\n"
    return follow_str


def saveFiles_process_create(project_name):
    saveFiles_process = threading.Thread(target=saveFiles, args=(project_name,))
    saveFiles_process.start()


def saveFiles(project_name):
    global output_table, grammar
    if project_name == "":
        messagebox.showerror(title="Error", message="Project name can not be blank")
        return
    (input_obj, lexical_obj, variable_obj, constant_obj, productions_obj, action_table_log_file,
     goto_table_log_file, parsing_stack_log_file, closures_log_file_obj, terminals_log_file_obj,
     non_terminals_log_file_obj, first_log_file_obj, follow_log_file_obj,
     conflicts_log_file_obj) = createlogfiles(project_name)
    input_textbox.config(state="disabled")
    output_textbox.config(state="normal")
    variable_textbox.config(state="normal")
    constant_textbox.config(state="normal")
    input_obj.write(input_textbox.get(1.0, "end-1c") + "\n")
    input_obj.close()
    lexical_obj.write(output_textbox.get(1.0, "end-1c") + "\n")
    lexical_obj.close()
    variable_obj.write(variable_textbox.get(1.0, "end-1c") + "\n")
    variable_obj.close()
    constant_obj.write(constant_textbox.get(1.0, "end-1c") + "\n")
    constant_obj.close()
    to_write = ""
    for prod in grammar.productionslist:
        to_write = to_write + str(prod) + "\n"
    productions_obj.write(to_write)
    productions_obj.close()

    closure_str = get_closure_string()
    closures_log_file_obj.write(closure_str)
    closures_log_file_obj.close()

    terminals_str = get_terminals_string()
    terminals_log_file_obj.write(terminals_str)
    terminals_log_file_obj.close()

    non_terminals_str = get_non_terminals_string()
    non_terminals_log_file_obj.write(non_terminals_str)
    non_terminals_log_file_obj.close()

    first_set_str = get_first_set_string()
    first_log_file_obj.write(first_set_str)
    first_log_file_obj.close()

    follow_set_str = get_follow_sets_str()
    follow_log_file_obj.write(follow_set_str)
    follow_log_file_obj.close()

    conflicts_str = grammar.get_conflicts_string()
    conflicts_log_file_obj.write(conflicts_str)
    conflicts_log_file_obj.close()

    try:
        while new_proc.is_alive():
            time.sleep(2)
            pass
            # new_proc.kill()
    except Exception as e:
        pass
    try:
        grammar.action_parsing_table.to_excel(action_table_log_file)
        grammar.goto_parsing_table.to_excel(goto_table_log_file)
        output_table.to_excel(parsing_stack_log_file)
    except:
        messagebox.showerror(title="未创建存储文件", message="请先点击“创新文件”创建一个文件来存放数据")
        return
    output_textbox.config(state="disabled")
    variable_textbox.config(state="disabled")
    constant_textbox.config(state="disabled")
    input_textbox.config(state="normal")
    new_window_on_closing()


def start_select_grammar_thread():
    select_grammar_thread = threading.Thread(target=select_grammar)
    select_grammar_thread.daemon = True
    select_grammar_thread.start()


def select_grammar():
    global grammar
    productionList_filename = filedialog.askopenfilename(filetypes=(("Text Files", ".txt"),),
                                                         title="Select your Production Lists")
    if productionList_filename != "":
        temp = Grammar(productionList_filename)
        if not temp.error:
            grammar = temp

    while not grammar:
        messagebox.showerror(title="No Grammar Selected",
                             message="Cannot start without any grammar. Please select Grammar first.;")
        productionList_filename = filedialog.askopenfilename(filetypes=(("Text Files", ".txt"),),
                                                             title="Select your Production Lists")
        if productionList_filename != "":
            temp = Grammar(productionList_filename)
            if not temp.error:
                grammar = temp


def detection():
    global det_thread, new_proc
    # try:
    #     if det_thread.is_alive():
    det_thread = threading.Thread(target=detection_thread)
    det_thread.daemon = True
    det_thread.start()
    new_proc = mp.Process(target=syntax_analysis, args=(None,))


def detection_thread():
    global output_textbox, input_textbox, client_queue
    textbox_string = ""
    client_queue = mp.Queue()
    global prev_token_list
    prev_token_list = []
    while True:
        check_queue()
        if textbox_string != input_textbox.get(1.0, "end-1c"):
            symbol_Table = SymbolTables()
            token_list = []
            textbox_string = input_textbox.get(1.0, "end-1c")
            output_textbox.config(state="normal")
            output_textbox.delete(1.0, "end")
            output_textbox.insert(1.0, f"{analyze(textbox_string, symbol_Table, token_list)}")
            output_textbox.config(state="disabled")
            variable_textbox.config(state="normal")
            variable_textbox.delete(1.0, "end")
            variable_textbox.insert(1.0, f"{get_variable_table_text(symbol_Table)}")
            variable_textbox.config(state="disabled")
            constant_textbox.config(state="normal")
            constant_textbox.delete(1.0, "end")
            constant_textbox.insert(1.0, f"{get_constant_table_text(symbol_Table)}")
            constant_textbox.config(state="disabled")


def analyze(text, symbol_Table, token_list):
    global new_proc, prev_token_list, grammar
    analyzed_text = ""
    lexer = Lexer(text + "\n")
    error_flag = False
    try:
        token = lexer.get_next_token(symbol_Table, grammar)
        if token.type != EOF:
            token_list.append(token)
    except Exception as e:
        analyzed_text += f"Error at {str(e)[18:]} \n"
        # analyzed_text += f"Error at {str(e)} \n"
        token = Token(EOF, "")
        error_flag = True

    while token.type != EOF:
        analyzed_text += str(token) + "\n"
        try:
            token = lexer.get_next_token(symbol_Table, grammar)
            if token.type != EOF:
                token_list.append(token)
            if repr(token) == ";":
                token_list.append(hash_token)
        except Exception as e:
            error_flag = True
            analyzed_text += f"Error at {str(e)[18:]} \n"
            # analyzed_text += f"Error at {e} \n"
            break
    if not error_flag and token_list != prev_token_list:
        prev_token_list = token_list
        try:
            if new_proc.is_alive():
                new_proc.kill()
        except Exception as e:
            pass
        new_proc = mp.Process(target=syntax_analysis,
                              args=(token_list, output_table, client_queue, grammar))
        new_proc.start()
    return analyzed_text


def clear_table(output_table):
    output_table.drop(output_table.index, inplace=True)


# parsing_steps_table.insert(parent='', index='end', iid=counter, text='',
#                            values=(f"{counter}", f"{parse_stack.get_all()}",
#                                    f"{repr(input_token)}",
#                                    f"Error At {repr(input_token)}, state= {int(current_state)}"))

def syntax_analysis(token_list, output_table, client_queue, grammar):
    global parsing_steps_table
    parse_stack = parsing_stack()
    c_point = 0
    counter = 1
    try:
        clear_table(output_table)
    except Exception as e:
        pass
    action = "None"
    while c_point < len(token_list) and token_list[c_point] is not None:
        current_state = parse_stack.peek()
        input_token = token_list[c_point]
        # try:
        action = grammar.action_parsing_table.at[int(current_state), repr(input_token)]
        # except KeyError as e:
        #     analyzed_text += f"repr{input_token} not allowed"
        #     exit()
        new_row_to_insert = []
        if repr(action) == "None":
            new_row_to_insert = [f"{parse_stack.get_all()}", f"{repr(input_token)}",
                                 f"Error At {repr(input_token)}, state= {int(current_state)}"]
            output_table.loc[len(output_table.index)] = new_row_to_insert
            break
        elif repr(action) == "SHIFT":
            prev_token = input_token
            parse_stack.push(input_token)
            c_point += 1
            parse_stack.push(states(int(action)))
            new_row_to_insert = [f"{parse_stack.get_all()}", f"{repr(input_token)}",
                                 f"Shifted to state {int(action)} "
                                 f"due to input {repr(prev_token)}"]
            output_table.loc[len(output_table.index)] = new_row_to_insert

        elif repr(action) == "REDUCE":
            prev_token = input_token
            c_prod = grammar.productionslist[int(action)]
            last_elem = parse_stack.pop(int(c_prod))
            temp_state = parse_stack.peek()
            action = grammar.goto_parsing_table.at[int(temp_state), repr(c_prod)]
            parse_stack.push(c_prod)
            parse_stack.push(states(int(action)))
            new_row_to_insert = [f"{parse_stack.get_all()}", f"{repr(input_token)}",
                                 f"Reduced {str(c_prod)} and new state is "
                                 f"{int(action)} due to input {repr(prev_token)}"]
            output_table.loc[len(output_table.index)] = new_row_to_insert
        elif repr(action) == "ACCEPT":
            parse_stack.clear()
            new_row_to_insert = [f"{parse_stack.get_all()}",
                                 f"{repr(input_token)}", f"Accepted Current String"]
            output_table.loc[len(output_table.index)] = new_row_to_insert
            parse_stack.original_stack()
            c_point += 1
        counter += 1
    try:
        if repr(action) != "None" and repr(action) != "ACCEPT":
            new_row_to_insert = [f"{parse_stack.get_all()}", f"{repr(input_token)}",
                                 f"Error At {repr(input_token)}, state= {int(current_state)}"]
            output_table.loc[len(output_table.index)] = new_row_to_insert
    except UnboundLocalError as e:
        pass
    client_queue.put(output_table)


def get_variable_table_text(symbol_Table):
    text = "Pos  Variable Names\n"
    for i in symbol_Table.variable_table:
        text += f"{i[0]:3d}   {i[1]}" + "\n"
    return text


def get_constant_table_text(symbol_Table):
    text = "Pos   Constant Values\n"
    for i in symbol_Table.constant_table:
        text += f"{i[0]:3d}       {i[1]}" + "\n"
    return text


def check_queue():
    global output_table
    try:
        instruction = instruction_queue.get_nowait()
        instruction()
    except queue.Empty:
        pass
    try:
        temp_table = client_queue.get_nowait()
        # print(temp_table)
        output_table = temp_table
        parsing_steps_table.model.df = output_table
        parsing_steps_table.redraw()
    except Exception as e:
        pass


if "__main__" == __name__:
    createPath()
    global event, instruction_queue, paused
    event = threading.Event()
    instruction_queue = queue.Queue()
    paused = False
    root = tk.Tk()
    initGUI(root)
    detection()
    root.mainloop()
