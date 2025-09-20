from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def main():
    # print(get_files_info("calculator","pkg"))
    # print(get_files_info("calculator","."))
    # print(get_files_info("calculator","/.."))

    #print(get_file_content("functions","lorem-ipsum.txt"))
    # print(get_file_content("functions","not-a-file.txt"))
    # print(get_file_content("functions","/.."))

    #print(write_file("functions","new/hello1.txt","Wow, what a file!"))
    print(run_python_file("calculator", "main.py", ["3 + 5"]))


if __name__ == "__main__":
    main()