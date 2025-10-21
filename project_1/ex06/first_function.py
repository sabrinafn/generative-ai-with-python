import sys

def greeting(name: str) -> None:
    if not name:
        print('No arguments provided')
    else:
        print(f'Hello, {name}')

def name() -> str:
    if len(sys.argv) < 2:
        return ""
    else:
        return sys.argv[1]

def main():
    greeting(name())

if __name__ == "__main__":
    main()