import os
from google.genai import types

def get_files_info(working_directory,directory=None):
    abs_working_directory = os.path.abspath(working_directory)
    if directory is None:
        #directory = abs_working_directory
        abs_directory= abs_working_directory
    else:
        abs_directory=os.path.abspath(os.path.join(abs_working_directory,directory))
     
    if not abs_directory.startswith(abs_working_directory):
        return f"Erorr: {directory} is not in the working directory"

    files_info = ""
    files_list = os.listdir(abs_directory)
    for file in files_list:
        file_path = os.path.join(abs_directory, file)
        file_size = os.path.getsize(file_path)
        is_directory = os.path.isdir(file_path)
        files_info += f"- {file}: file size: {file_size} bytes, is_directory: {is_directory} \n"

    return files_info


schema_get_files_info = types.FunctionDeclaration(
name="get_files_info",
description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "directory": types.Schema(
            type=types.Type.STRING,
            description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
        ),
    },
),
)