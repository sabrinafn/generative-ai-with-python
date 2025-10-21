import sys
import cowsay

def greeting(name: str) -> None:
    if not name:
        cowsay.ghostbusters('OooOoooOoooooo')
    else:
        cowsay.tux(f'Hello {name}')

def name() -> str:
    if len(sys.argv) < 2:
        return ""
    else:
        return sys.argv[1]

def main():
    greeting(name())

if __name__ == "__main__":
    main()