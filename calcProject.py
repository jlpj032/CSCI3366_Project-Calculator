import re
import math

# here wee are designing the tokens that we will be using for mathimatical expressions 
Tokens = [
        ('NUMBERS', r'\d+'),
        ('PLUS', r'\+'),
        ('MINUS', r'\-'),
        ('TIMES', r'\*'),
        ('DIVITION', r'/'),
        ('SINE', r'sin'),
        ('COSINE', r'cos'),
        ('TANGENT', r'tan'),
        ('COSECANT', r'csc'),
        ('SECANT', r'sec'),
        ('COTANGENT', r'cot'),
        ('LPAR', r'\('),
        ('RPAR', r'\)'),
        ('SKIP', r'[ \t\n]'),
        ('MISMATCH', r'.')
    ]

def scan(input_string):
    token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in Tokens)
    token_pattern = re.compile(token_regex)
    tokens = []
    for match in token_pattern.finditer(input_string):
        print(match.lastgroup)
        print(match.group(match.lastgroup))

            



class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0



if __name__ == '__main__':
    print("this is the start of something great")
    example = "13 + 4 - 4"
    example2 = "sin(23) + cot(48)"
    print("\nExample 1\n")
    scan(example)
    print("\nExample 2\n")
    scan(example2)
