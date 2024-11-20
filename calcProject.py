import re
import math

Tokens = [
    ('NUMBER', r'\d+'),
    ('PLUS', r'\+'),
    ('MINUS', r'\-'),
    ('TIMES', r'\*'),
    ('DIVISION', r'/'),
    ('EXPONENT', r'\^'),
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
    # Tokenizing the input string
    token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in Tokens)
    token_pattern = re.compile(token_regex)
    tokens = []
    for match in token_pattern.finditer(input_string):
        if match.lastgroup == "SKIP":
            continue
        elif match.lastgroup == "MISMATCH":
            continue
        else:
            tokens.append((match.lastgroup, match.group(match.lastgroup)))
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        return self.expression()

    def evaluate(self, tree):
        """Evaluate the parsed expression tree."""
        if isinstance(tree, int):
            return tree
        
        operator, *args = tree
        
        if operator in ['SINE', 'COSINE', 'TANGENT', 'COSECANT', 'SECANT', 'COTANGENT']:
            if len(args) == 1:
                arg = self.evaluate(args[0])
                if operator == 'SINE':
                    return math.sin(math.radians(arg))
                elif operator == 'COSINE':
                    return math.cos(math.radians(arg))
                elif operator == 'TANGENT':
                    return math.tan(math.radians(arg))
                elif operator == 'COSECANT':
                    return 1 / math.sin(math.radians(arg))
                elif operator == 'SECANT':
                    return 1 / math.cos(math.radians(arg))
                elif operator == 'COTANGENT':
                    return 1 / math.tan(math.radians(arg))
            else:
                raise ValueError(f"Unknown function signature: {operator} takes one argument")

        if operator == 'EXPONENT':
            left, right = args
            left_val = self.evaluate(left)
            right_val = self.evaluate(right)
            return left_val ** right_val

        left, right = args
        left_val = self.evaluate(left)
        right_val = self.evaluate(right)
        
        if operator == 'PLUS':
            return left_val + right_val
        elif operator == 'MINUS':
            return left_val - right_val
        elif operator == 'TIMES':
            return left_val * right_val
        elif operator == 'DIVISION':
            return left_val / right_val
        else:
            raise ValueError(f"Unknown operator: {operator}")

    def expression(self):
        # Handle + and - operators (lowest precedence)
        term = self.term()
        while self.match('PLUS', 'MINUS'):
            operator = self.previous()[0]
            right = self.term()
            term = (operator, term, right)
        return term
    
    def term(self):
        # Handle * and / (medium precedence)
        factor = self.factor()
        while self.match('TIMES', 'DIVISION'):
            operator = self.previous()[0]
            right = self.factor()
            factor = (operator, factor, right)
        return factor

    def factor(self):
        # Handle exponentiation first (highest precedence)
        base = self.exponent()
        
        # After exponentiation, handle numbers and functions
        return base
    
    def exponent(self):
        # Parse exponentiation: base ^ exponent
        left = self.primary()
        while self.match('EXPONENT'):
            operator = self.previous()[0]  # ^ operator
            right = self.primary()  # Right side of the exponentiation
            left = (operator, left, right)  # Exponentiation operation
        return left

    def primary(self):
        # Handles numbers, functions, and parentheses
        if self.match('NUMBER'):
            return int(self.previous()[1])
        elif self.match('SINE', 'COSINE', 'TANGENT', 'COSECANT', 'SECANT', 'COTANGENT'):
            func = self.previous()[0]
            self.consume('LPAR')
            expr = self.expression()
            self.consume('RPAR')
            return (func, expr)
        elif self.match('LPAR'):
            expr = self.expression()
            self.consume('RPAR')
            return expr
        else:
            raise SyntaxError("Unexpected token: " + self.peek()[0])

    def match(self, *types):
        if self.check(*types):
            self.advance()
            return True
        return False

    def check(self, *types):
        if self.is_at_end():
            return False
        return self.peek()[0] in types

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def consume(self, type):
        if self.check(type):
            return self.advance()
        raise SyntaxError(f"Expected '{type}' but found {self.peek()[0]}.")

    def peek(self):
        if self.is_at_end():
            return None
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1] if self.current > 0 else None

    def is_at_end(self):
        return self.current >= len(self.tokens)


if __name__ == '__main__':
    print("This is the start of something great!")
    
    example = "3 + 4 * 2 ^ 3"
    example2 = "sin(23)+cos(48)^2"
    
    print(f"\nExample 1 - ({example})")
    print("-" * 20)
    tokensFound1 = scan(example)
    print("Tokens Found:", tokensFound1)
    parser1 = Parser(tokensFound1)
    tree1 = parser1.parse()  # Parse the expression
    result1 = parser1.evaluate(tree1)  # Evaluate the result
    print("parse tree: ", tree1)
    print(f"Result = {result1}")
    
    print(f"\nExample 2 - ({example2})")
    print("-" * 20)
    tokensFound2 = scan(example2)
    print("Tokens Found:", tokensFound2)
    parser2 = Parser(tokensFound2)
    tree2 = parser2.parse()  # Parse the expression
    result2 = parser2.evaluate(tree2)  # Evaluate the result
    print('parse tree: ', tree2)
    print(f"Result = {result2}")
