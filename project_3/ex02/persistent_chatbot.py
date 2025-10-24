from google import genai
import os
import sys
from database import init_db, Message, Summary
from datetime import datetime

instructions = """
<prompt>
    <instrucao_sistema>
        Você é um assistente de IA altamente inteligente, empático e informativo. 
        Seu objetivo é fornecer respostas precisas, relevantes e úteis com base no contexto da conversa. 
        Você sempre deve usar as informações fornecidas nas memórias de curto e longo prazo.
    </instrucao_sistema>

    <few_shot_examples>
        <exemplo>
            <entrada_usuario>
                Olá! Me lembra sobre o que conversamos na semana passada?
            </entrada_usuario>
            <short_term_memory>
                User: oi
                Assistant: Olá! Como você está?
            </short_term_memory>
            <long_term_memory>
                Resumo 1: O usuário gosta de filmes de ficção científica.
                Resumo 2: O usuário prefere respostas curtas e diretas.
            </long_term_memory>
            <saida_esperada>
                Olá! Você mencionou anteriormente que gosta de filmes de ficção científica. Posso te sugerir algo nesse estilo?
            </saida_esperada>
        </exemplo>
    </few_shot_examples>

    <contexto>
        <short_term_memory> 
            <!-- Substitua por uma string contendo as últimas 5 mensagens do banco de dados Messages -->
        </short_term_memory>
        <long_term_memory>
            <!-- Substitua por uma string contendo os últimos 10 resumos do banco de dados Summary -->
        </long_term_memory>
    </contexto>

    <tarefa>
        Com base nas memórias fornecidas acima, forneça uma resposta coerente, útil e relevante à mensagem do usuário. 
        Sempre considere tanto o contexto recente quanto o histórico persistente.
    </tarefa>

    <regras_restritas>
        1. Não invente informações que não estejam nas memórias fornecidas.
        2. Sempre mantenha a clareza e objetividade na resposta.
        3. Use linguagem natural e amigável.
        4. Não inclua nenhum dado do banco que não esteja na memória fornecida.
    </regras_restritas>
</prompt>
"""


# this function validates CLI args and returns the provided term
def validate_arguments():
    prog = os.path.basename(sys.argv[0])
    if (len(sys.argv) != 1):
        print(f'Usage: python3 ./{prog}\nType a question when asked.')
        return sys.exit(1)


# this function calls the GenAI API and returns the model's response
def generate_response(prompt, instructions):
    try:
        client = genai.Client()
        response = client.models.generate_content(
            model = "gemini-2.5-flash-lite",
            contents = contents,
            config = {
                "temperature": 0.0,
                "system_instruction": instructions,
                "max_output_tokens": 80,
                },
        )
        return response.text
    except Exception as e:
        print(f'Error: {e.message}')
        sys.exit(1)

def add_message(role, content, session):
    new_message = Message(
        role=role,
        content=content,
        created_at=datetime.utcnow()
    )
    session.add(new_message)
    session.commit()

def get_last_messages(session):
    messages = (
        session.query(Message)
        .order_by(Message.created_at.desc())
        .limit(5)
        .all()
    )
    return list(reversed(messages))

def add_summary(summary_text, session):
    new_summary = Summary(
        content=summary_text,
        created_at=datetime.utcnow()
    )
    session.add(new_summary)
    session.commit()

def get_last_summaries(session):
    summaries = (
        session.query(Summary)
        .order_by(Summary.created_at.desc())
        .limit(10)
        .all()
    )
    return list(reversed(summaries))

def summaries_to_string(summaries):
    lines = []
    lines.append(f"last 10 summaries: ")
    for s in summaries:
        lines.append(f"- {s.content}")
    return "\n".join(lines)

def messages_to_string(messages):
    lines = []
    lines.append(f"last 5 messages: ")
    for m in messages:
        lines.append(f"{m.role}: {m.content}")
    return "\n".join(lines)

# main  
def main():
    validate_arguments()

    Session = init_db()

    while True:
        question = input("Q: ")
        if (question == "bye"):
            print("A: bye\n")
            break
        add_message('user', question, Session)
        last_five = messages_to_string(get_last_messages(5, Session))
        add_summary(last_five, Session)
        last_ten = summaries_to_string(get_last_summaries(10, Session))

        response = generate_response(question, instructions + last_five + last_ten)
        add_message('assistant', response)
        print(f"A: {response}") 




if __name__ == "__main__":
    main()