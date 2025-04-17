import os


def createPath():
    """Create New Folder for project in Logs"""
    #Get users documents location using the userpaths library
    cfilepath = os.path.join('log')

    #Create the directory if not existing, else continue
    try:
        os.makedirs(cfilepath, exist_ok=True)
        #print("Directory Created Successfully")
    except OSError as error:
        print("Directory already Exists and Not Created")
    return cfilepath


def createlogfiles(log_path):
    # Client training Average Loss File
    log_path = os.path.join('log', log_path)
    os.makedirs(log_path, exist_ok=True)

    input_log_file = os.path.join(log_path, 'source.txt')
    lexical_log_file = os.path.join(log_path, 'lexicals.txt')
    variable_table_log_file = os.path.join(log_path, 'variable table.txt')
    constant_table_log_file = os.path.join(log_path, 'constant table.txt')
    productions_list_log_file = os.path.join(log_path, 'productions list.txt')
    action_table_log_file = os.path.join(log_path, 'action table.xlsx')
    goto_table_log_file = os.path.join(log_path, 'goto table.xlsx')
    parsing_stack_log_file = os.path.join(log_path, 'parsing stack.xlsx')

    input_log_file_obj = open(input_log_file, 'w')
    lexical_log_file_obj = open(lexical_log_file, 'w')
    variable_table_file_obj = open(variable_table_log_file, 'w')
    constant_table_file_obj = open(constant_table_log_file, 'w')
    productions_list_file_obj = open(productions_list_log_file, 'w')

    return (input_log_file_obj, lexical_log_file_obj, variable_table_file_obj, constant_table_file_obj,
            productions_list_file_obj, action_table_log_file, goto_table_log_file, parsing_stack_log_file)
