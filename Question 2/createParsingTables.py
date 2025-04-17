import pandas as pd


class action:
    def __init__(self, type=None, new_state=None):
        self.type = type
        self.new_state = new_state

    def __str__(self):
        return str(f"{self.type}, {self.new_state}")

    def __int__(self):
        return self.new_state

    def __repr__(self):
        return str(self.type)


shift_1 = action("SHIFT", 1)
shift_2 = action("SHIFT", 2)
shift_3 = action("SHIFT", 3)
shift_4 = action("SHIFT", 4)
shift_5 = action("SHIFT", 5)
shift_6 = action("SHIFT", 6)
shift_7 = action("SHIFT", 7)
shift_8 = action("SHIFT", 8)
shift_9 = action("SHIFT", 9)
shift_10 = action("SHIFT", 10)
shift_11 = action("SHIFT", 11)
shift_12 = action("SHIFT", 12)
shift_13 = action("SHIFT", 13)
shift_14 = action("SHIFT", 14)
shift_15 = action("SHIFT", 15)
shift_16 = action("SHIFT", 16)

reduce_1 = action("REDUCE", 1)
reduce_2 = action("REDUCE", 2)
reduce_3 = action("REDUCE", 3)
reduce_4 = action("REDUCE", 4)
reduce_5 = action("REDUCE", 5)
reduce_6 = action("REDUCE", 6)
reduce_7 = action("REDUCE", 7)
reduce_8 = action("REDUCE", 8)
reduce_9 = action("REDUCE", 9)
reduce_10 = action("REDUCE", 10)
reduce_11 = action("REDUCE", 11)
reduce_12 = action("REDUCE", 12)
reduce_13 = action("REDUCE", 13)
reduce_14 = action("REDUCE", 14)
reduce_15 = action("REDUCE", 15)
reduce_16 = action("REDUCE", 16)

jump_1 = action("MOVE", 1)
jump_2 = action("MOVE", 2)
jump_3 = action("MOVE", 3)
jump_4 = action("MOVE", 4)
jump_5 = action("MOVE", 5)
jump_6 = action("MOVE", 6)
jump_7 = action("MOVE", 7)
jump_8 = action("MOVE", 8)
jump_9 = action("MOVE", 9)
jump_10 = action("MOVE", 10)
jump_11 = action("MOVE", 11)
jump_12 = action("MOVE", 12)
jump_13 = action("MOVE", 13)
jump_14 = action("MOVE", 14)
jump_15 = action("MOVE", 15)
jump_16 = action("MOVE", 16)

accept = action("ACCEPT")

data = [[None, None, shift_5, shift_6, None, shift_7, shift_8, None, None],
        [None, None, None, None, None, None, None, None, accept],
        [shift_10, None, None, None, None, None, None, shift_9, None],
        [reduce_3, shift_11, None, None, reduce_3, None, None, reduce_3, None],
        [reduce_5, reduce_5, None, None, reduce_5, None, None, reduce_5, None],
        [None, None, shift_5, shift_6, None, shift_7, shift_8, None, None],
        [None, None, shift_5, shift_6, None, shift_7, shift_8, None, None],
        [reduce_8, reduce_8, None, None, reduce_8, None, None, reduce_8, None],
        [reduce_9, reduce_9, None, None, reduce_9, None, None, reduce_9, None],
        [None, None, None, None, None, None, None, None, reduce_1],
        [None, None, shift_5, shift_6, None, shift_7, shift_8, None, None],
        [None, None, shift_5, shift_6, None, shift_7, shift_8, None, None],
        [reduce_6, reduce_6, None, None, reduce_6, None, None, reduce_6, None],
        [shift_10, None, None, None, shift_16, None, None, None, None],
        [reduce_2, shift_11, None, None, reduce_2, None, None, reduce_2, None],
        [reduce_4, reduce_4, None, None, reduce_4, None, None, reduce_4, None],
        [reduce_7, reduce_7, None, None, reduce_7, None, None, reduce_7, None]]

action_parsing_table = pd.DataFrame(data, columns=['or', 'and', 'not', '(', ')', 'true', 'false', ';', '#'])

data = [[jump_1, jump_2, jump_3, jump_4], [None, None, None, None], [None, None, None, None], [None, None, None, None],
        [None, None, None, None], [None, None, None, jump_12], [None, jump_13, jump_3, jump_4],
        [None, None, None, None],
        [None, None, None, None], [None, None, None, None], [None, None, jump_14, jump_4], [None, None, None, jump_15],
        [None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None],
        [None, None, None, None]]
goto_parsing_table = pd.DataFrame(data, columns=['S', 'EXPR', 'TERM', 'FACTOR'])

if __name__ == '__main__':
    filename = "action_parsing_table.xlsx"
    action_parsing_table.to_excel(filename)

    filename = "goto_parsing_table.xlsx"
    goto_parsing_table.to_excel(filename)
