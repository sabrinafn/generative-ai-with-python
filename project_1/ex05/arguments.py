import sys

args = sys.argv

if (len(args) < 2 or args[1] == ""):
    print('No arguments provided')
else:
    print(*args[1:])