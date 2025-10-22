from google import genai
import sys
import os

instructions = """
<instructions>
</instructions>
"""

example = """
<examples>
</examples>
"""

# this function validates CLI args and returns the provided term
def validate_arguments():
    prog = os.path.basename(sys.argv[0])
    if (len(sys.argv) == 2 and sys.argv[1] != ""):
        return sys.argv[1]
    print(f'Usage: python3 ./{prog} [prompt]')
    return sys.exit(1)

# this function constructs the few-shot prompt by appending it with the term received
def construct_prompt(example, prompt):
    return f"{example}\n<text>prompt: {prompt}\noutput:</text>"

# this function calls the GenAI API and returns the model's response
def generate_response(prompt):
    try:
        client = genai.Client()
        response = client.models.generate_content(
            model = "gemini-2.0-flash-lite",
            contents = prompt,
            config = {
                "temperature": 0.0,
                "system_instruction": instructions
            },
        )
        print(response.text)
        client.close()
    except Exception as e:
        print(f'Error: {e.message}')

# main  
def main():
    prompt = validate_arguments()
    constructed_prompt = construct_prompt(example, prompt)
    generate_response(constructed_prompt)

if __name__ == "__main__":
    main()