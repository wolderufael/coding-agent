import os

def write_file(working_directory,file_path,content):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_directory,file_path))
    
    if not abs_file_path.startswith(abs_working_directory):
        return f"Erorr: {file_path} is not in the working directory"
    
    parent_directory = os.path.dirname(abs_file_path)
    if not os.path.exists(parent_directory):
        try:
            os.makedirs(parent_directory)
        except Exception as e:
            return f"Could not create parent directory {parent_directory}: {e}"
        
    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Could not write file {file_path}: {e}"
    
    return f"Successfully wrote to {file_path}"