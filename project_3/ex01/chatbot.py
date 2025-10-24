from google import genai
import os
import sys

instructions = """
<prompt>
    <instructions>
        You are an interactive chatbot. Your goal is to answer user questions clearly and directly, 
        keeping the context of the last five interactions. Each interaction should be presented as:
        "User: [message]" and "Assistant: [response]".
        Include the history of the last interactions in the prompt so your answers remain coherent.
        The chatbot should only stop when the user types 'bye'.
        Respond only with your answer text, without labels or additional explanations.
    </instructions>

    <example>
        History:
        User: What is the capital of France?
        Assistant: Paris is the capital of France.
        User: And what is its population?
        Assistant: The population of Paris is approximately 2.2 million inhabitants.
        
        New question:
        User: What are the famous tourist attractions?
        
        Assistant's response:
        Paris has famous tourist attractions such as the Eiffel Tower, the Louvre Museum, 
        Notre-Dame Cathedral, the Arc de Triomphe, and the Sacré-Cœur Basilica.
    </example>
</prompt>
"""


# this function validates CLI args and returns the provided term
def validate_arguments():
    prog = os.path.basename(sys.argv[0])
    if (len(sys.argv) != 1):
        print(f'Usage: python3 ./{prog}\nType a question when asked.')
        return sys.exit(1)

# transform chat_history (lista de dicts) in a string
def format_history(chat_history):
    chat_string = ""
    for h in chat_history:
        user = h.get("user", "")
        assistant = h.get("assistant", "")
        chat_string += f"User: {user}\nAssistant: {assistant}\n"
    return chat_string.strip()


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

# def print_chat(chat_history):
#     for line in chat_history:
#         print(f"User: {line.get('user', '')}")
#         print(f"Assistant: {line.get('assistant', '')}\n")

# main  
def main():
    validate_arguments()

    max_history = 5
    chat_history = []

    while True:
        question = input("Q: ")
        if (question == "bye"):
            print("A: bye\n")
            #print_chat(chat_history)
            break
        history_string = format_history(chat_history)
        response = generate_response(question, instructions, history_string)
        print(f"A: {response}")
        chat_history.append({
            "user": question,
            "assistant": response
        })
        if len(chat_history) > max_history:
            chat_history = chat_history[-max_history:] 
            # [-5:] positions before the last position: until the end of the list


if __name__ == "__main__":
    main()