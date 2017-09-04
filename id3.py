import math
from models import Id3Tree


def id3_main(in_data, logging):
    root = Id3Tree()
    create_node(in_data, root, logging)

    return root

def create_node(in_data, node, logging):
    col_name = prepare_tree(in_data, logging)
    dict_res = create_sub_data(in_data, col_name, logging)
    node.name = col_name

    flag_write_log = False
    for key, val in dict_res.items():
        if type(val) == str:
            if not flag_write_log:
                logging.append("leaf node found")
                logging.row += 1
                logging.col = 1

            logging.append(col_name + ":" + key)
            logging.col += 1
            logging.append(val)
            logging.row += 1
            logging.col = 1
            flag_write_log = True

    if not flag_write_log:
        logging.append("non-leaf node found")
        logging.row += 1
        logging.col = 1

    logging.row += 1
    logging.col = 1

    for key, val in dict_res.items():
        if type(val) == str:
            node.type_table[key] = val
        elif type(val) == list:
            node.type_table[key] = Id3Tree()
            logging.append(col_name + ":" + key)
            logging.row += 1
            logging.col = 1
            create_node(val, node.type_table[key], logging)

    return


def create_sub_data(in_data, col_name, logging):
    dict_type = {}
    lst_col_name = [name for name in in_data[0] if name != col_name]
    current_type = ""

    for rowIndex in range(1, len(in_data)):
        lst_temp = []
        for colIndex in range(len(in_data[rowIndex])):
            name = in_data[0][colIndex]
            val = in_data[rowIndex][colIndex]

            if name == col_name:
                if val not in dict_type:
                    dict_type[val] = [lst_col_name]
                current_type = val
            else:
                lst_temp.append(val)

        dict_type[current_type].append(lst_temp)

    for key, val in dict_type.items():
        if is_just_one_class(val):
            dict_type[key] = val[1][-1]

    return dict_type

def is_just_one_class(in_data):
    is_one = True
    val = in_data[1][-1]

    for index in range(1, len(in_data)):
        if val != in_data[index][-1]:
            is_one = False
            break

    return is_one

def prepare_tree(in_data, logging):
    dict_type = {}
    for name in in_data[0]:
        logging.append(name)
        logging.col += 1

        dict_type[name] = {}

    logging.row += 1
    logging.col = 1

    for rowIndex in range(1, len(in_data)):
        for colIndex in range(len(in_data[rowIndex])):
            name = in_data[0][colIndex]
            val = in_data[rowIndex][colIndex]

            logging.append(val)
            logging.col += 1

            if val in dict_type[name]:
                dict_type[name][val] += 1
            else:
                dict_type[name][val] = 1

        logging.row += 1
        logging.col = 1

    n = len(in_data) - 1
    info_gaind = sum((-val / n) * math.log2(val / n) for _, val in dict_type[in_data[0][-1]].items())
    max_gain = 0
    max_col = ""

    logging.append("Infomation Gain")
    logging.row += 1
    logging.col = 1

    for colName, dictVal in dict_type.items():
        if colName == in_data[0][-1]:
            continue

        info_gain = 0
        for type, quan in dictVal.items():
            info_gain += (quan / n) * calc_info_gain(in_data, colName, type, quan)

        logging.append(colName)
        logging.row += 1
        logging.append(info_gaind - info_gain)
        logging.row -= 1
        logging.col += 1

        if max_gain < (info_gaind - info_gain):
            max_gain = info_gaind - info_gain
            max_col = colName

    logging.row += 2
    logging.col = 1
    logging.append("Best attribute")
    logging.col = 2
    logging.append(max_col)
    logging.row += 1
    logging.col = 1

    return max_col


def calc_info_gain(in_data, col_name, type, n):
    c = {}
    class_index = len(in_data[0]) - 1
    col_focus = (index for index in range(len(in_data[0])) if in_data[0][index] == col_name)
    col_focus = next(col_focus)

    for i in range(1, len(in_data)):
        if in_data[i][col_focus] != type:
            continue

        if in_data[i][class_index] in c:
            c[in_data[i][class_index]] += 1
        else:
            c[in_data[i][class_index]] = 1

    info_gaind = sum((-val / n) * math.log2(val / n) for _, val in c.items())
    return info_gaind
