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
    # parsing_steps_table = ttk.Treeview(parsing_steps_frame)
    # parsing_steps_table['columns'] = ('Number', "Current Stack", "Current Input Token", "Current Action")
    #
    # parsing_steps_table.column("#0", width=0, stretch=tk.NO)
    # parsing_steps_table.column("Number", anchor=tk.CENTER, width=50, stretch=tk.NO)
    # parsing_steps_table.column("Current Stack", anchor=tk.CENTER, width=30)
    # parsing_steps_table.column("Current Input Token", anchor=tk.CENTER, width=30)
    # parsing_steps_table.column("Current Action", anchor=tk.CENTER, width=30)
    #
    # parsing_steps_table.heading("#0", text="", anchor=tk.CENTER)
    # parsing_steps_table.heading("Number", text="No", anchor=tk.CENTER)
    # parsing_steps_table.heading("Current Stack", text="Current Stack Contents", anchor=tk.CENTER)
    # parsing_steps_table.heading("Current Input Token", text="Current Pointed Token", anchor=tk.CENTER)
    # parsing_steps_table.heading("Current Action", text="Current Action Taken", anchor=tk.CENTER)
    #
    # parsing_vert_sb = tk.Scrollbar(parsing_steps_frame)
    # parsing_vert_sb.pack(side=tk.RIGHT, fill=tk.BOTH)
    # parsing_steps_table.config(yscrollcommand=parsing_vert_sb.set)
    # parsing_vert_sb.config(command=parsing_steps_table.yview)
    #
    # parsing_horiz_sb = tk.Scrollbar(parsing_steps_frame, orient="horizontal")
    # parsing_horiz_sb.pack(side=tk.BOTTOM, fill=tk.BOTH)
    # parsing_steps_table.config(xscrollcommand=parsing_horiz_sb.set)
    # parsing_horiz_sb.config(command=parsing_steps_table.xview)
    # parsing_steps_table.pack(fill="both", expand=True)

    parsing_steps_table = pdt.Table(parsing_steps_frame, dataframe=output_table)
    parsing_steps_table.show()

    global display_parsing_trees_btn
    display_parsing_trees_btn = tk.Button(root, text="Display Parsing Trees", font=('Arial', 14), command=display_trees)
    display_parsing_trees_btn.place(relx=0.63, rely=0.96)

    global display_productions_btn
    display_productions_btn = tk.Button(root, text="Display Productions", font=('Arial', 14), command=display_prods)
    display_productions_btn.place(relx=0.75, rely=0.96)
    # parsing_steps_table.insert(parent='', index='end', iid=i, text='',
    #                            values=(f"{i}", 'Stack Values', 'Current Input Token', 'Action Taken'))


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
            else:
                goto_table_window.focus_set()
                goto_table_window.bell()
            return
    display_parsing_trees_btn.config(state="normal")
    trees_window.destroy()


def display_trees():
    global trees_window
    display_parsing_trees_btn.config(state="disabled")
    trees_window = tk.Toplevel(root)
    trees_window.title("Select Tree: ")
    trees_window.geometry("250x200")
    trees_window.protocol("WM_DELETE_WINDOW", lambda: trees_window_on_closing(archaic_list))
    archaic_list = [0, 0]

    global display_action_table_btn, display_goto_table_btn
    display_action_table_btn = tk.Button(trees_window, text="Display Action Table", font=('Arial', 14),
                                         command=lambda: display_action_table(archaic_list))
    display_goto_table_btn = tk.Button(trees_window, text="Display Goto Table", font=('Arial', 14),
                                       command=lambda: display_goto_table(archaic_list))

    display_action_table_btn.place(relx=0.1, rely=0.1, relheight=0.35, relwidth=0.8)
    display_goto_table_btn.place(relx=0.1, rely=0.55, relheight=0.35, relwidth=0.8)


def display_prods():
    global prods_window
    display_productions_btn.config(state="disabled")
    prods_window = tk.Toplevel(root)
    prods_window.title("All Productions: ")
    prods_window.geometry("300x350")
    prods_window.protocol("WM_DELETE_WINDOW", lambda: prods_window_on_closing())

    prod_str = ""
    for i in production_Lists:
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

    action_table = pdt.Table(action_table_window, dataframe=action_parsing_table)
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

    goto_table = pdt.Table(goto_table_window, dataframe=goto_parsing_table)
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


def saveFiles_process_create(project_name):
    saveFiles_process = threading.Thread(target=saveFiles, args=(project_name, ))
    saveFiles_process.start()


def saveFiles(project_name):
    global output_table
    if project_name == "":
        messagebox.showerror(title="Error", message="Project name can not be blank")
        return
    (input_obj, lexical_obj, variable_obj, constant_obj, productions_obj,
     action_table_log_file, goto_table_log_file, parsing_stack_log_file) = createlogfiles(project_name)
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
    for prod in production_Lists:
        to_write = to_write + str(prod) + "\n"
    productions_obj.write(to_write)
    productions_obj.close()
    try:
        while new_proc.is_alive():
            time.sleep(2)
            pass
            # new_proc.kill()
    except Exception as e:
        pass
    try:
        action_parsing_table.to_excel(action_table_log_file)
        goto_parsing_table.to_excel(goto_table_log_file)
        output_table.to_excel(parsing_stack_log_file)
    except:
        messagebox.showerror(title="未创建存储文件", message="请先点击“创新文件”创建一个文件来存放数据")
        return
    output_textbox.config(state="disabled")
    variable_textbox.config(state="disabled")
    constant_textbox.config(state="disabled")
    input_textbox.config(state="normal")
    new_window_on_closing()


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
    global new_proc, prev_token_list
    analyzed_text = ""
    lexer = Lexer(text + "\n")
    error_flag = False
    try:
        token = lexer.get_next_token(symbol_Table)
        if token.type != EOF:
            token_list.append(token)
    except Exception as e:
        analyzed_text += f"Error at {str(e)[18:]} \n"
        token = Token(EOF, "")
        error_flag = True

    while token.type != EOF:
        analyzed_text += str(token) + "\n"
        try:
            token = lexer.get_next_token(symbol_Table)
            if token.type != EOF:
                token_list.append(token)
            if repr(token) == ";":
                token_list.append(hash_token)
        except Exception as e:
            error_flag = True
            analyzed_text += f"Error at {str(e)[18:]} \n"
            break
    if not error_flag and token_list != prev_token_list:
        prev_token_list = token_list
        try:
            if new_proc.is_alive():
                new_proc.kill()
        except Exception as e:
            pass
        new_proc = mp.Process(target=syntax_analysis, args=(token_list, output_table, client_queue))
        new_proc.start()
    return analyzed_text


def clear_table(output_table):
    output_table.drop(output_table.index, inplace=True)


# parsing_steps_table.insert(parent='', index='end', iid=counter, text='',
#                            values=(f"{counter}", f"{parse_stack.get_all()}",
#                                    f"{repr(input_token)}",
#                                    f"Error At {repr(input_token)}, state= {int(current_state)}"))

def syntax_analysis(token_list, output_table, client_queue):
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
        action = action_parsing_table.at[int(current_state), repr(input_token)]
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
            c_prod = production_Lists[int(action)]
            last_elem = parse_stack.pop(int(c_prod))
            temp_state = parse_stack.peek()
            action = goto_parsing_table.at[int(temp_state), repr(c_prod)]
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
    if repr(action) != "None" and repr(action) != "ACCEPT":
        new_row_to_insert = [f"{parse_stack.get_all()}", f"{repr(input_token)}",
                             f"Error At {repr(input_token)}, state= {int(current_state)}"]
        output_table.loc[len(output_table.index)] = new_row_to_insert
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
