import os
import subprocess

def run_python_file(working_directory,file_path,args=[]):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_directory,file_path))
    
    if not abs_file_path.startswith(abs_working_directory):
        return f"Erorr: {file_path} is not in the working directory"
    
    if not os.path.isfile(abs_file_path):
        return f"Erorr: {file_path} is not a file"

    if not abs_file_path.endswith(".py"):
        return f"Erorr: {file_path} is not a Python file"

    try:
        final_args= ["python", file_path] + args
        output = subprocess.run(final_args, 
        cwd=abs_working_directory,
        timeout=30,
        capture_output=True,
        )

        final_string = f"""
        STDOUT:{output.stdout}
        STDERR:{output.stderr}
        """
        
        if output.stdout == "" and output.stderr == "":
            final_string = "No output was produced"
        
        if output.returncode != 0:
            final_string += f"Process exited with code: {output.returncode}"

        return final_string
    except Exception as e:
        return f"Could not run {file_path}: {e}"
