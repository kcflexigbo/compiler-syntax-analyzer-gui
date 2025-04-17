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
    closures_log_file = os.path.join(log_path, 'Closures.txt')
    terminals_log_file = os.path.join(log_path, 'Terminals.txt')
    non_terminals_log_file = os.path.join(log_path, 'Non Terminals.txt')
    first_log_file = os.path.join(log_path, 'First Sets.txt')
    follow_log_file = os.path.join(log_path, 'Follow Sets.txt')
    conflicts_log_file = os.path.join(log_path, 'Conflicts.txt')

    input_log_file_obj = open(input_log_file, 'w')
    lexical_log_file_obj = open(lexical_log_file, 'w')
    variable_table_file_obj = open(variable_table_log_file, 'w')
    constant_table_file_obj = open(constant_table_log_file, 'w')
    productions_list_file_obj = open(productions_list_log_file, 'w')
    closures_log_file_obj = open(closures_log_file, 'w')
    terminals_log_file_obj = open(terminals_log_file, 'w')
    non_terminals_log_file_obj = open(non_terminals_log_file, 'w')
    first_log_file_obj = open(first_log_file, 'w')
    follow_log_file_obj = open(follow_log_file, 'w')
    conflicts_log_file_obj = open(conflicts_log_file, 'w')

    return (input_log_file_obj, lexical_log_file_obj, variable_table_file_obj, constant_table_file_obj,
            productions_list_file_obj, action_table_log_file, goto_table_log_file, parsing_stack_log_file,
            closures_log_file_obj, terminals_log_file_obj, non_terminals_log_file_obj, first_log_file_obj,
            follow_log_file_obj, conflicts_log_file_obj)
