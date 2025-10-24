from google import genai
import os
import sys
from database import init_db, Message, Summary

instructions = """
<role>
Você é um assistente conversacional inteligente, responsável por manter uma conversa coerente, contínua e contextualizada com o usuário.
Seu comportamento é orientado para parecer uma interação natural, mas eficiente. Fale de maneira direta e clara, sem floreios desnecessários.
</role>

<context_handling>
Você possui dois tipos de memória:
1. <short_term_memory>: contém as últimas mensagens recentes trocadas na conversa atual.</short_term_memory>
2. <long_term_memory>: contém resumos e informações persistentes armazenadas de interações anteriores.</long_term_memory>

Seu objetivo é utilizar ambas as memórias para manter contexto e coerência, sem repetir informações redundantes.
Quando uma nova sessão começa, você deve reconstruir o contexto consultando as memórias persistidas no banco de dados.
</context_handling>

<database_structure>
O sistema de persistência usa SQLAlchemy com duas tabelas:

<class Message>
- id: int (chave primária)
- role: str ('user' ou 'assistant')
- content: text (mensagem enviada)
- created_at: datetime (UTC)
</class>

<class Summary>
- id: int (chave primária)
- content: text (resumo das interações anteriores)
- created_at: datetime (UTC)
</class>
</database_structure>

<instructions>
- Sempre consulte a memória de longo prazo primeiro para recuperar informações relevantes sobre o histórico global.
- Depois, use a memória de curto prazo para manter continuidade com o diálogo atual.
- Se perceber que a conversa mudou de assunto ou que há informações novas importantes, gere um novo resumo e armazene na tabela Summary.
- As mensagens trocadas devem ser salvas na tabela Message, com o campo 'role' definido corretamente.
- Mantenha o histórico entre sessões para que, ao reabrir o chat, o contexto completo possa ser reconstruído.

Use a seguinte estrutura de resposta para cada turno de conversa:
<response>
<context_used>
[listar brevemente quais partes do contexto foram usadas]
</context_used>

<assistant_reply>
[resposta ao usuário]
</assistant_reply>
</response>
</instructions>

<examples>
<example>
<short_term_memory>
Usuário: Como posso criar uma conexão com banco de dados em Python?
Assistente: Você pode usar SQLAlchemy. Quer que eu te mostre um exemplo?
</short_term_memory>
<long_term_memory>
Resumo: O usuário está aprendendo Python e gosta de exemplos práticos com SQLAlchemy.
</long_term_memory>
Usuário: Sim, mostra.
<expected_response>
<context_used>long_term_memory</context_used>
<assistant_reply>
Claro. Aqui está um exemplo simples:
```python
from sqlalchemy import create_engine
engine = create_engine("sqlite:///meubanco.db")
Esse código cria um banco SQLite local chamado meubanco.db.
</assistant_reply>
</expected_response>
</example>
</examples>
"""

# this function validates CLI args and returns the provided term
def validate_arguments():
    prog = os.path.basename(sys.argv[0])
    if (len(sys.argv) != 1):
        print(f'Usage: python3 ./{prog}\nType a question when asked.')
        return sys.exit(1)


# this function calls the GenAI API and returns the model's response
def generate_response(prompt, instructions, chat_history):
    
    if chat_history:
        contents = f"History:\n{chat_history}\n\nUser: {prompt}\nAssistant: "
    else:
        contents = f"User: {prompt}\nAssistant: "

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

def add_message(role, content):
    new_message = Message(
            role=role,
            content=content,
            created_at=datetime.utcnow()
        )
        session.add(new_message)
        session.commit()

def get_last_messages(limit=5):
    messages = (
        session.query(Message)
        .order_by(Message.created_at.desc())
        .limit(limit)
        .all()
    )
    return list(reversed(messages))

def messages_to_string(messages):
    lines = []
    for m in messages:
        lines.append(f"{m.role}: {m.content}")
    return "\n".join(lines)

# main  
def main():
    validate_arguments()

    SessionLocal = init_db()
    session = SessionLocal()


    while True:
        question = input("Q: ")
        if (question == "bye"):
            print("A: bye\n")
            break
        add_message('user', question)
        msg = 
        response = generate_response(question, instructions, history_string)
        add_message('assistant', response)
        print(f"A: {response}") 




if __name__ == "__main__":
    main()