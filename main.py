import os,sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    verbose_flag = False

    if len(sys.argv) > 1:
        prompt = sys.argv[1]
    else:
        print("No prompt provided")
        sys.exit(1)

    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages
    )
    print(response.text)

    if verbose_flag:
        print("User Prompt: ", prompt)
        print("Prompt Token: ", response.usage_metadata.prompt_token_count)
        print("Candidates Token: ", response.usage_metadata.candidates_token_count)


if __name__ == "__main__":
    main()