# Project 1 — Exercises Overview

This module contains small standalone Python scripts/programs (ex01–ex08) and this documentation (ex09). Run scripts from the `project_1` directory with Python 3.

General notes:
- Recommended: Python 3.10
- From inside `project_1`, run scripts like: `python3 ex01/name.py`
- External dependencies:
  - `cowsay` (for ex07): `pip install cowsay`
  - `requests` (for ex08): `pip install requests`
- Internet required for ex08 (calls Open-Meteo APIs)

## ex01 — Name
- File: [ex01/name.py](../ex01/name.py)
- Summary:
  - Prints the full name defined in the script.
- Run:
  - `python3 ex01/name.py`

## ex02 — Boolean
- File: [ex02/boolean.py](../ex02/boolean.py)
- Summary:
  - Compares the strings `'1'` and `'0'` using equality and ordering, printing results (messages are in Portuguese).
- Notes:
  - This is string comparison, not numeric.
- Run:
  - `python3 ex02/boolean.py`

## ex03 — Lists
- File: [ex03/lists.py](../ex03/lists.py)
- Summary:
  - Iterates over a list and prints each item.
- Run:
  - `python3 ex03/lists.py`

## ex04 — Dicts
- File: [ex04/dicts.py](../ex04/dicts.py)
- Summary:
  - Iterates over a dictionary and prints key–value pairs.
- Run:
  - `python3 ex04/dicts.py`

## ex05 — Arguments
- File: [ex05/arguments.py](../ex05/arguments.py)
- Summary:
  - Prints all command-line arguments provided after the script name; prints “No arguments provided” if none.
- Notes:
  - Use quotes for arguments that contain spaces.
- Run:
  - No args: `python3 ex05/arguments.py`
  - With args: `python3 ex05/arguments.py one two`

## ex06 — First Function
- File: [ex06/first_function.py](../ex06/first_function.py)
- Summary:
  - Reads a single name from the command line and prints `Hello, <name>`; prints “No arguments provided” if missing.
- Run:
  - `python3 ex06/first_function.py Alice`

## ex07 — Greetings from the Farm
- File: [ex07/greetings_from_the_farm.py](../ex07/greetings_from_the_farm.py)
- Summary:
  - Like ex06, but uses `cowsay` for ASCII-art output. With a name, prints a Tux greeting; without a name, prints a Ghostbusters-style message.
- Requirements:
  - Install dependency: `pip install cowsay`
  - Terminal should support ASCII/UTF-8.
- Run:
  - `python3 ex07/greetings_from_the_farm.py Alice`

## ex08 — Weather
- File: [ex08/weather.py](../ex08/weather.py)
- Summary:
  - Looks up a city using Open-Meteo’s geocoding API, fetches current temperature, and prints: `Current temperature in City, Country is <temp> <unit>`.
- Requirements:
  - Install dependency: `pip install requests`
  - Internet access (calls Open-Meteo APIs).
- Notes:
  - Usage: `python3 ex08/weather.py "City Name"`
  - Exits with code 1 on incorrect usage or if the city is not found.
- Run:
  - `python3 ex08/weather.py "New York"`

## ex09 — Documentation (README)
- File: [ex09/README.md](README.md)
- Summary:
  - This documentation file describes each exercise in the module.
- Notes:
  - No code to run for this exercise.
- Assignment Prompt:

    Analyze all files and folders inside the directory "project_1" (ex01 to ex09). Update ex09/README.md with a description of each exercise. Use the provided PDF with the exercises for reference.

    For each exercise, include:
    - The exercise name and folder name
    - A short summary of what the exercise does
    - Any special requirements or notes for running it

    Formatting requirements:
    - Use Markdown headings and bullet points
    - Only write in English"
