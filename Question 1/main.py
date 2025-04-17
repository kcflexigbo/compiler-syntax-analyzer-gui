# import tkinter as tk
from mttkinter import mtTkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import queue
from analyzer import *
from filesbrowser import *


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
    input_frame.place(relx=0.02, rely=0.05, relheight=0.9, relwidth=0.47)

    global input_textbox
    input_textbox = tk.Text(input_frame, font=("Helvetica", 15))
    input_vert_sb = tk.Scrollbar(input_frame)
    input_vert_sb.pack(side=tk.RIGHT, fill=tk.BOTH)
    input_textbox.config(yscrollcommand=input_vert_sb.set)
    input_vert_sb.config(command=input_textbox.yview)

    input_textbox.pack(fill="both", expand=True)

    vsep_1 = ttk.Separator(root, orient='vertical', style='blue.TSeparator')
    vsep_1.place(relx=0.51, rely=0, relheight=1, relwidth=0.005)

    lb2 = tk.Label(root, text="Output Tokens:", font=('Arial', 14))
    lb2.place(relx=0.53, rely=0.02)
    lb2.configure(background="grey")

    output_frame = tk.Frame(root)
    output_frame.place(relx=0.53, rely=0.05, relheight=0.9, relwidth=0.21)

    global output_textbox
    output_textbox = tk.Text(output_frame, font=("Comic Sans MS", 15))
    output_vert_sb = tk.Scrollbar(output_frame)
    output_vert_sb.pack(side=tk.RIGHT, fill=tk.BOTH)
    output_textbox.config(yscrollcommand=output_vert_sb.set)
    output_vert_sb.config(command=output_textbox.yview)

    output_textbox.pack(fill="both", expand=True)
    output_textbox.config(state="disabled")

    vsep_2 = ttk.Separator(root, orient='vertical', style='yellow.TSeparator')
    vsep_2.place(relx=0.765, rely=0, relheight=1, relwidth=0.005)

    lb3 = tk.Label(root, text="Symbol Tables:", font=('Arial', 14))
    lb3.place(relx=0.78, rely=0.02, relheight=0.025)
    lb3.configure(background="grey")

    lb4 = tk.Label(root, text="Variable / Identifier Table:", font=('Arial', 14))
    lb4.place(relx=0.78, rely=0.075, relheight=0.025)
    lb4.configure(background="grey")

    variable_frame = tk.Frame(root)
    variable_frame.place(relx=0.78, rely=0.105, relheight=0.4, relwidth=0.20)

    global variable_textbox
    variable_textbox = tk.Text(variable_frame, font=("Comic Sans MS", 15))
    variable_vert_sb = tk.Scrollbar(variable_frame)
    variable_vert_sb.pack(side=tk.RIGHT, fill=tk.BOTH)
    variable_textbox.config(yscrollcommand=variable_vert_sb.set)
    variable_vert_sb.config(command=variable_textbox.yview)

    variable_textbox.pack(fill="both", expand=True)
    variable_textbox.config(state="disabled")

    lb5 = tk.Label(root, text="Constant Table:", font=('Arial', 14))
    lb5.place(relx=0.78, rely=0.52, relheight=0.025)
    lb5.configure(background="grey")

    constant_frame = tk.Frame(root)
    constant_frame.place(relx=0.78, rely=0.55, relheight=0.4, relwidth=0.20)

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
    pausebtn.place(relx=0.45, rely=0.96)

    global savebtn
    savebtn = tk.Button(root, text="Save Files", font=('Arial', 14), command=saveWindow)
    savebtn.place(relx=0.7, rely=0.96)


def pauseDetection():
    global paused
    if not paused:
        insert_event = event.wait
        instruction_queue.put(insert_event)
    else:
        event.set()
        event.clear()
    paused = not paused


def on_closing():
    savebtn.config(state="normal")
    new_window.destroy()


def saveWindow():
    global new_window
    savebtn.config(state="disabled")
    new_window = tk.Toplevel()
    new_window.title("Save Files")
    new_window.geometry("250x80")
    new_window.protocol("WM_DELETE_WINDOW", on_closing)

    lb1 = tk.Label(new_window, text="Enter the Name of the project to be saved as", font=('Arial', 10))
    lb1.place(relx=0.02, rely=0.02)

    inp1 = tk.StringVar()
    inp1_entry = tk.Entry(new_window, textvariable=inp1)
    inp1_entry.place(relx=0.1, rely=0.3, relwidth=0.8)

    confirmbtn = tk.Button(new_window, text="Save", command=lambda: saveFiles(inp1.get().strip()))
    confirmbtn.place(relx=0.2, rely=0.6, relwidth=0.6)


def saveFiles(project_name):
    if project_name == "":
        messagebox.showerror(title="Error", message="Project name can not be blank")
        return
    input_obj, lexical_obj,variable_obj, constant_obj = createlogfiles(project_name)
    input_textbox.config(state="normal")
    output_textbox.config(state="normal")
    variable_textbox.config(state="normal")
    constant_textbox.config(state="normal")
    input_obj.write(input_textbox.get(1.0, "end-1c")+"\n")
    input_obj.close()
    lexical_obj.write(output_textbox.get(1.0, "end-1c")+"\n")
    lexical_obj.close()
    variable_obj.write(variable_textbox.get(1.0, "end-1c")+"\n")
    variable_obj.close()
    constant_obj.write(constant_textbox.get(1.0, "end-1c")+"\n")
    constant_obj.close()
    input_textbox.config(state="disabled")
    output_textbox.config(state="disabled")
    variable_textbox.config(state="disabled")
    constant_textbox.config(state="disabled")
    on_closing()

def detection():
    global det_thread
    det_thread = threading.Thread(target=detection_thread)
    det_thread.daemon = True
    det_thread.start()


def detection_thread():
    global output_textbox, input_textbox
    textbox_string = ""
    while True:
        check_queue()
        if textbox_string != input_textbox.get(1.0, "end-1c"):
            symbol_Table = SymbolTables()
            textbox_string = input_textbox.get(1.0, "end-1c")
            output_textbox.config(state="normal")
            output_textbox.delete(1.0, "end")
            output_textbox.insert(1.0, f"{analyze(textbox_string, symbol_Table)}")
            output_textbox.config(state="disabled")
            variable_textbox.config(state="normal")
            variable_textbox.delete(1.0, "end")
            variable_textbox.insert(1.0, f"{get_variable_table_text(symbol_Table)}")
            variable_textbox.config(state="disabled")
            constant_textbox.config(state="normal")
            constant_textbox.delete(1.0, "end")
            constant_textbox.insert(1.0, f"{get_constant_table_text(symbol_Table)}")
            constant_textbox.config(state="disabled")


def analyze(text, symbol_Table):
    analyzed_text = ""
    lexer = Lexer(text + "\n")
    try:
        token = lexer.get_next_token(symbol_Table)
    except Exception as e:
        analyzed_text += f"Error at {str(e)[18:]} \n"
        token = Token(EOF, "")

    while token.type != EOF:
        analyzed_text += str(token) + "\n"
        try:
            token = lexer.get_next_token(symbol_Table)
        except Exception as e:
            analyzed_text += f"Error at {str(e)[18:]} \n"
            break
    return analyzed_text


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
    try:
        instruction = instruction_queue.get_nowait()
        instruction()
    except queue.Empty:
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
