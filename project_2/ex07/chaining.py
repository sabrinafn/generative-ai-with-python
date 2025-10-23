from google import genai
import sys
import os

GREEN = "\033[32m"
RESET = "\033[0m"

first_prompt = """
<prompt>
    <instructions>
        Você é um especialista em marketing de produtos. 
        Sua tarefa é pegar uma descrição curta e genérica de um produto e transformá-la 
        em uma descrição detalhada, envolvente e persuasiva, destacando seus benefícios, 
        funcionalidades e diferenciais de forma natural e atrativa.
        **Responda apenas com o texto final da descrição, sem rótulos como "output:" ou explicações adicionais.**
        **Limite sua resposta a no máximo 200 tokens**
    </instructions>

    <example>
        input: "fone de ouvido sem fio"
        output: "Os fones de ouvido sem fio oferecem liberdade total de movimento, 
        conectividade Bluetooth estável e som de alta qualidade. Com design ergonômico 
        e bateria de longa duração, são ideais para ouvir músicas, atender chamadas 
        e praticar esportes sem interrupções."
    </example>
</prompt>
"""

second_prompt = """
<prompt>
    <instructions>
        Você é um redator publicitário criativo. 
        Sua função é transformar a descrição detalhada de um produto em um anúncio 
        publicitário curto, atraente e envolvente. 
        O texto deve despertar desejo no consumidor e transmitir os principais benefícios 
        do produto de forma emocional e direta.
        **Responda apenas com o texto do anúncio final, sem comentários ou rótulos.**
        **Limite sua resposta a no máximo 100 tokens**
    </instructions>

    <example>
        input: "Os fones de ouvido sem fio oferecem liberdade total de movimento, 
        conectividade Bluetooth estável e som de alta qualidade. Com design ergonômico 
        e bateria de longa duração, são ideais para ouvir músicas, atender chamadas 
        e praticar esportes sem interrupções."
        output: "Sinta o som da liberdade! Experimente os novos fones de ouvido sem fio 
        e viva sua música com conforto, estilo e qualidade."
    </example>
</prompt>
"""

third_prompt = """
<prompt>
    <instructions>
        Você é um tradutor profissional especializado em marketing. 
        Sua tarefa é traduzir o texto fornecido para o inglês, preservando o tom 
        criativo e publicitário do original. A tradução deve soar natural para o público 
        de língua inglesa.
        **Responda apenas com a tradução final, sem dizer 'Translation:' ou 'Output:'.**
    </instructions>

    <example>
        input: "Sinta o som da liberdade! Experimente os novos fones de ouvido sem fio 
        e viva sua música com conforto, estilo e qualidade."
        output: "Feel the sound of freedom! Try the new wireless earbuds and enjoy your music 
        with comfort, style, and quality."
    </example>
</prompt>
"""


# this function validates CLI args and returns the provided term
def validate_arguments():
    prog = os.path.basename(sys.argv[0])
    if (len(sys.argv) == 2 and sys.argv[1] != ""):
        return sys.argv[1]
    print(f'Usage: python3 ./{prog} [short description of a product]')
    return sys.exit(1)

# this function calls the GenAI API and returns the model's response
def generate_response(prompt, instructions, temperature, max_output_tokens):
    prompt = f"<text>input: {prompt}\noutput:</text>"
    try:
        client = genai.Client()
        response = client.models.generate_content(
            model = "gemini-2.5-flash-lite",
            contents = prompt,
            config = {
                "temperature": temperature,
                "system_instruction": instructions,
                "max_output_tokens": max_output_tokens,
                },
        )
        print(response.text)
        return response.text
    except Exception as e:
        print(f'Error: {e.message}')
        sys.exit(1)

# main  
def main():
    prompt = validate_arguments()

    print(f"{GREEN}[Descrição detalhada gerada pelo primeiro prompt]{RESET}")
    first_response = generate_response(prompt, first_prompt, 0.0, 200)
    print("\n")

    print(f"{GREEN}[Anúncio publicitário gerado pelo segundo prompt]{RESET}")
    second_response = generate_response(first_response, second_prompt, 2.0, 100)
    print("\n")

    print(f"{GREEN}[Tradução para a língua inglesa]{RESET}")
    generate_response(second_response, third_prompt, 0.0, 100)


if __name__ == "__main__":
    main()