from google import genai
import sys
import os

instructions = """
<instructions>
You are a travel advisor AI. 
Your task is to receive a location as input 
and return the 5 best tourist attractions for that location. 
Respond with a simple numbered list, no extra text.
If the input is not a valid location, respond with a clear message explaining that you could not find the location, and remind that you are a travel advisor AI.
</instructions>
"""

example = """
<examples>
Here a few examples:

Input: "Paris"
Output:
1. Torre Eiffel
2. Museu do Louvre
3. Catedral de Notre-Dame
4. Arco do Triunfo
5. Basílica de Sacré-Cœur

Input: "Rome"
Output:
1. Coliseu
2. Fontana di Trevi
3. Vaticano
4. Panteão
5. Piazza Navona

Input: "New York"
Output:
1. Estátua da Liberdade
2. Central Park
3. Times Square
4. Empire State Building
5. Museu Metropolitano de Arte
</examples>
"""

# this function validates CLI args and returns the provided term
def validate_arguments():
    prog = os.path.basename(sys.argv[0])
    if (len(sys.argv) == 2 and sys.argv[1] != ""):
        return sys.argv[1]
    print(f'Usage: python3 ./{prog} [holiday location]')
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
                "system_instruction": instructions + example
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