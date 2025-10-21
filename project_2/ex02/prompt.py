from google import genai
import sys

default_temperature = 1.0

def validate_arguments():
    arg_count = len(sys.argv)
    if (arg_count == 2):
        return dict(prompt = sys.argv[1], temp = default_temperature)
    if (arg_count == 3):
        try:
            temp = float(sys.argv[2])
        except ValueError:
            raise ValueError("Temperature must be a number")
        if not (0.0 <= temp <= 2.0):
            raise ValueError("Temperature must be between 0.0 and 2.0")
        print(temp)
        return dict(prompt = sys.argv[1], temp = temp)
    
    raise ValueError("Invalid usage.\nUsage: ./prompt.py [prompt] [temperature]")


def generate_response(data):
    client = genai.Client()

    response = client.models.generate_content(
        model = "gemini-2.0-flash-lite",
        contents = data["prompt"],
        config = {
            "temperature": data["temp"]
        } 
    )
    print(response.text)
    

def main():
    try:
        data = validate_arguments()
        generate_response(data)
    except Exception as e:
        print(f'Error during request: {e}')

if __name__ == "__main__":
    main()