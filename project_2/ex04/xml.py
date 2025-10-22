from google import genai
import sys
import os

instructions = """
<instructions>You are a summarization assistant.
You will receive a text and summarize it in **no more than 20 words**.
</instructions>
"""

examples = """
<examples>
Input:
Durante a Idade Média, as universidades europeias surgiram como centros de
conhecimento, reunindo estudiosos de diversas áreas. Elas desempenharam papel essencial na
preservação e transmissão de saberes clássicos, além de estimular debates filosóficos e
científicos que moldaram o pensamento ocidental e prepararam terreno para o Renascimento.
Output:
Universidades medievais preservaram saber clássico, promoveram debates e criaram base intelectual que impulsionou o Renascimento europeu.

Input:
A Revolução Industrial transformou profundamente a economia e a sociedade, introduzindo máquinas, fábricas e novas formas de trabalho urbano.
Output:
Revolução Industrial mecanizou a produção e acelerou mudanças sociais e econômicas nas cidades.

Input:
Os ecossistemas tropicais são fundamentais para a regulação do clima, abrigando grande biodiversidade e atuando como sumidouros de carbono.
Output:
Ecossistemas tropicais regulam o clima e preservam biodiversidade essencial ao equilíbrio ambiental.

Input:
Com o avanço da tecnologia digital, o compartilhamento rápido de informações tornou-se global, impactando a comunicação e o comportamento social.
Output:
Tecnologia digital globalizou a informação e transformou padrões de comunicação e comportamento social.

Input:
A invenção da imprensa por Gutenberg possibilitou a ampla difusão do conhecimento, impulsionando a educação e a Reforma Protestante.
Output:
Imprensa de Gutenberg democratizou o saber e fomentou avanços culturais e religiosos na Europa.
</examples>
"""

# this function validates CLI args and returns the provided term
def validate_arguments():
    prog = os.path.basename(sys.argv[0])
    if (len(sys.argv) == 2 and sys.argv[1] != ""):
        return sys.argv[1]
    print(f'Usage: python3 ./{prog} [text to summarize]')
    return sys.exit(1)

# this function constructs the few-shot prompt by appending it with the term received
def construct_prompt(examples, prompt):
    return f"{examples}\n<text>prompt: {prompt}\noutput:</text>"

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
    except Exception as e:
        print(f'Error: {e.message}')

# main  
def main():
    prompt = validate_arguments()
    constructed_prompt = construct_prompt(examples, prompt)
    generate_response(constructed_prompt)

if __name__ == "__main__":
    main()