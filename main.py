import os,sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from call_function import call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Get the content of a file
    - Write to a file
    - Run a python file with optional CLI arguments

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    verbose_flag = False

    if len(sys.argv) > 1:
        prompt = sys.argv[1]
    else:
        print("No prompt provided")
        sys.exit(1)

    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True

    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]

)
    config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages,
        config=config
    )
    
    if response is None or response.usage_metadata is None:
        print("Response is missing")
        return
    
    if response.function_calls:
        for function_call_part in response.function_calls:
            # print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            response = call_function(function_call_part, verbose_flag)
            print(response)
    else:
        print(response.text)

    if verbose_flag:
        print("User Prompt: ", prompt)
        print("Prompt Token: ", response.usage_metadata.prompt_token_count)
        print("Candidates Token: ", response.usage_metadata.candidates_token_count)


if __name__ == "__main__":
    main()