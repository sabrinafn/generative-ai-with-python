from google import genai
import sys
import os
from pydantic import BaseModel

instructions = """
<instructions>
You are an information extraction assistant.
Given a sentence describing a person, extract:
- name
- age (as a number)
- profession
- city of residence

Always respond **only in valid JSON**, in the following format:
{
  "nome": "string",
  "idade": number,
  "profissão": "string",
  "cidade": "string"
}

Do not include any explanations, text, or comments outside the JSON.
</instructions>
"""

example = """
<examples>
Here a few examples:

Input: "João Silva, 35 anos, é engenheiro e mora em São Paulo"
Output: {"nome": "João Silva", "idade": 35, "profissão": "engenheiro", "cidade": "São Paulo"}

Input: "Maria Fernandes tem 28 anos, trabalha como médica e vive em Belo Horizonte"
Output: {"nome": "Maria Fernandes", "idade": 28, "profissão": "médica", "cidade": "Belo Horizonte"}

Input: "Rafael Oliveira, 33 anos, trabalha como nutricionista e vive em Florianópolis"
Output: {"nome": "Rafael Oliveira", "idade": 33, "profissão": "nutricionista", "cidade": "Florianópolis"}

Input: "Camila Santos, 31 anos, é professora de yoga em Manaus"
Output: {"nome": "Camila Santos", "idade": 31, "profissão": "professora de yoga", "cidade": "Manaus"}

</examples>
"""

# this function validates CLI args and returns the provided term
def validate_arguments():
    prog = os.path.basename(sys.argv[0])
    if (len(sys.argv) == 2 and sys.argv[1] != ""):
        return sys.argv[1]
    print(f'Usage: python3 ./{prog} [name, age, profession and city]')
    return sys.exit(1)

# this function calls the GenAI API and returns the model's response
def generate_response(prompt):
    prompt = f"<text>prompt: {prompt}\noutput:</text>"
    try:
        client = genai.Client()
        response = client.models.generate_content(
            model = "gemini-2.0-flash",
            contents = prompt,
            config = {
                "temperature": 0.0,
                "system_instruction": instructions + example,
                "response_mime_type": "application/json",
                "response_schema": {
                    "type": "object",
                    "properties": {
                        "nome": {"type": "string"},
                        "idade": {"type": "integer"},
                        "profissao": {"type": "string"},
                        "cidade": {"type": "string"}
                    },
                    "required": ["nome", "idade", "profissao", "cidade"]
                },
            },
        )
        print(response.text)
        client.close()
    except Exception as e:
        print(f'Error: {e.message}')

# main  
def main():
    prompt = validate_arguments()
    generate_response(prompt)

if __name__ == "__main__":
    main()