from models import Id3Tree


def prediction_main(lst, lst_predict):
    root = create_tree(lst)
    predict(root, lst_predict)
    # print(lst_predict)
    return


def create_tree(lst):
    root = Id3Tree()

    for item in lst:
        node = root
        child_lst = item.split("()")
        result = child_lst[-1]

        for index in range(0, len(child_lst) - 1, 2):
            node.name = child_lst[index]
            if child_lst[index + 1] not in node.type_table:
                node.type_table[child_lst[index + 1]] = Id3Tree()

            node = node.type_table[child_lst[index + 1]]

        node.name = result

    return root


def predict(root_tree, lst_predict):
    lst_title = lst_predict[0]

    for child_lst in lst_predict[1:]:
        node = root_tree

        while True:
            if len(node.type_table) == 0:
                child_lst[-1] = node.name
                break

            index = lst_title.index(node.name)

            if child_lst[index] in node.type_table:
                node = node.type_table[child_lst[index]]
            else:
                child_lst[-1] = "unknown"
                break

    return