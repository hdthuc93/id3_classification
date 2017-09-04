import io_file
import id3
import prediction
import draw_model
from models import LoggingExcel
import sys

def main():
    lst_params = sys.argv

    if not check_params(lst_params):
        print("Params incorrect, please try again follow one of patterns below:")
        print("\t --task train --input [path excel file] --output [path text file] --log [path excel file]")
        print("\t --task predict --input [path excel file] --model [path text file] --output [path excel file]")
        print("\t --task visualize --model [path text file] --output [path PNG file] ")
        return

    if "train" in lst_params:
        index = lst_params.index("--input") + 1
        input_excel_path = str(lst_params[index])
        index = lst_params.index("--output") + 1
        output_path = str(lst_params[index])
        index = lst_params.index("--log") + 1
        log_path = str(lst_params[index])

        lstExcel = io_file.read_excel(input_excel_path)
        logging = LoggingExcel()
        tree = id3.id3_main(lstExcel, logging)
        logging.append("finish")
        logging.writeToFile(log_path)
        io_file.write_result_id3(tree, output_path)
    elif "predict" in lst_params:
        index = lst_params.index("--input") + 1
        input_excel_path = str(lst_params[index])
        index = lst_params.index("--output") + 1
        output_excel_path = str(lst_params[index])
        index = lst_params.index("--model") + 1
        model_path = str(lst_params[index])

        lst = io_file.read_txt_file(model_path)
        lst_predict = io_file.read_excel(input_excel_path)
        prediction.prediction_main(lst, lst_predict)
        io_file.write_excel_file(lst_predict, output_excel_path)
    else:
        index = lst_params.index("--model") + 1
        input_model_path = str(lst_params[index])
        index = lst_params.index("--output") + 1
        output_img_path = str(lst_params[index])

        lst = io_file.read_txt_file(input_model_path)
        draw_model.draw_main(lst, output_img_path)


def check_params(lst_params):
    len_lst = len(lst_params)

    if "--task" not in lst_params:
        return False

    if "train" not in lst_params and "predict" not in lst_params and "visualize" not in lst_params:
        return False

    if "train" in lst_params or "predict" in lst_params:

        if "--input" not in lst_params or "--output" not in lst_params:
            return False

        index = lst_params.index("--input") + 1

        if index >= len_lst:
            return False

        check_lst = lst_params[index].split(".xlsx")
        if len(check_lst) != 2 or check_lst[1] != "":
            return False

        index = lst_params.index("--output") + 1

        if index >= len_lst:
            return False

        if "train" in lst_params:
            check_lst = lst_params[index].split(".")
            if len(check_lst) < 2 or check_lst[-1] == "":
                return False

            if "--log" not in lst_params:
                return False

            index = lst_params.index("--log") + 1

            if index >= len_lst:
                return False

            check_lst = lst_params[index].split(".xlsx")
            if len(check_lst) != 2 or check_lst[1] != "":
                return False
        else:
            check_lst = lst_params[index].split(".xlsx")
            if len(check_lst) != 2 or check_lst[1] != "":
                return False

            if "--model" not in lst_params:
                return False

            index = lst_params.index("--model") + 1
            if index >= len_lst:
                return False

            check_lst = lst_params[index].split(".")

            if len(check_lst) < 2 or check_lst[-1] == "":
                return False
    else:
        # check --model command
        if "--model" not in lst_params:
            return False

        index = lst_params.index("--model") + 1
        if index >= len_lst:
            return False

        check_lst = lst_params[index].split(".")

        if len(check_lst) < 2 or check_lst[-1] == "":
            return False

        # check --output command
        if "--output" not in lst_params:
            return False

        index = lst_params.index("--output") + 1
        if index >= len_lst:
            return False

        check_lst = lst_params[index].split(".png")

        if len(check_lst) < 2 or check_lst[-1] != "":
            return False

    return True


if __name__ == "__main__":
    main()
