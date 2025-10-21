from google import genai
import sys

data = """
This is a few shot prompt for you:
You should behave in a way that you will receive as input technical computer terms 
and return its translations what they are. Here are a few examples:
Example 1: prompt: SQL. your response: linguagem de consulta estruturada
Example 2: prompt: JSON. your response: formato de dados leve e legível
Example 3: prompt: API. your response: interface de programação de aplicações
"""


def validate_arguments():
    if (len(sys.argv) == 2 and sys.argv[1] != ""):
        return sys.argv[1]
    print(f'Usage: python3 ./fewshot.py [IT terminology]')
    return sys.exit(1)

def construct_prompt(data, prompt):
    return f"{data}\nTerm: {prompt}\nTranslation:"

def generate_response(prompt):
    client = genai.Client()
    response = client.models.generate_content(
        model = "gemini-2.0-flash-lite",
        contents = prompt
    )
    return response.text
    

def main():
    prompt = validate_arguments()
    constructed_prompt = construct_prompt(data, prompt)
    print(generate_response(constructed_prompt))

if __name__ == "__main__":
    main()