import os,sys
import time
import random
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ClientError
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from call_function import call_function


def make_api_call_with_retry(client, model, contents, config, max_retries=5, base_delay=1.0):
    """
    Make an API call with exponential backoff retry logic for rate limits.
    
    Args:
        client: The genai client
        model: Model name to use
        contents: Message contents
        config: Generation config
        max_retries: Maximum number of retry attempts
        base_delay: Base delay in seconds for exponential backoff
    
    Returns:
        API response or None if all retries failed
    """
    for attempt in range(max_retries + 1):
        try:
            response = client.models.generate_content(
                model=model, contents=contents, config=config
            )
            return response
        except ClientError as e:
            if e.status_code == 429:  # Rate limit exceeded
                if attempt == max_retries:
                    print(f"Rate limit exceeded. Maximum retries ({max_retries}) reached.")
                    print("Please wait a few minutes before trying again or consider upgrading your API plan.")
                    return None
                
                # Extract retry delay from error if available
                retry_delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                
                # Try to parse the suggested delay from the error message
                if 'retry in' in str(e):
                    try:
                        import re
                        match = re.search(r'retry in (\d+(?:\.\d+)?)s', str(e))
                        if match:
                            suggested_delay = float(match.group(1))
                            retry_delay = max(retry_delay, suggested_delay)
                    except:
                        pass
                
                print(f"Rate limit hit. Retrying in {retry_delay:.2f} seconds... (attempt {attempt + 1}/{max_retries + 1})")
                time.sleep(retry_delay)
            else:
                # Re-raise non-rate-limit errors
                raise e
    
    return None


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

    max_iters=20
    # Add a small delay between iterations to help avoid rate limits
    iteration_delay = 0.5  # seconds
    
    for i in range(max_iters):
        # Add delay between iterations (except for the first one)
        if i > 0:
            time.sleep(iteration_delay)
            
        response = make_api_call_with_retry(
            client, 'gemini-2.0-flash-001', messages, config
        )
        
        if response is None:
            print("Failed to get response after retries. Exiting.")
            return
            
        if response.usage_metadata is None:
            print("Response is missing usage metadata")
            return
        
        if verbose_flag:
            print("User Prompt: ", prompt)
            print("Prompt Token: ", response.usage_metadata.prompt_token_count)
            print("Response Token: ", response.usage_metadata.candidates_token_count)
        
        if response.candidates:
            for candidate in response.candidates:
                if candidate is None or candidate.content is None:
                    continue
                messages.append(candidate.content)
                
        if response.function_calls:
            for function_call_part in response.function_calls:
                result = call_function(function_call_part, verbose_flag)
                messages.append(result)
        else:
            print(response.text)
            break  # Exit the loop when no more function calls are needed




if __name__ == "__main__":
    main()