import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory,file_path):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_directory,file_path))
    
    if not abs_file_path.startswith(abs_working_directory):
        return f"Erorr: {file_path} is not in the working directory"
    
    if not os.path.isfile(abs_file_path):
        return f"Erorr: {file_path} is not a file"

    try:
        file_content_string = ""
        with open(abs_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) > MAX_CHARS:
                file_content_string += "... File truncated at 10000 characters"
    except Exception as e:
        return f"Erorr reading file: {e}"

    return file_content_string


schema_get_file_content = types.FunctionDeclaration(
name="get_file_content",
description="Gets the content of a given file as a string, constrained to the working directory.",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "file_path": types.Schema(
            type=types.Type.STRING,
            description="The path of the file, relative to the working directory.",
        ),
    },
),
)