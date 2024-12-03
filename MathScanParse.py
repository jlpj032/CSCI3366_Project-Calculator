# Module: MathScanParse
import re
import math

# The project was getting big so we decided to spread it into seperate files to organize it better
RAD = True

Tokens = [
    ('NUMBER', r'\d+\.\d+|\d+'),
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
    ('PI', r'pi'),
    ('EULER', r'e'),
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
            raise Exception("Syntax error Try again")
        else:
            token_type = match.lastgroup
            token_value = match.group(match.lastgroup)
            
            # Replace '-' before numbers with 'NEG' for negative numbers
            if token_type == 'MINUS' and (not tokens or tokens[-1][0] in ['PLUS', 'MINUS', 'TIMES', 'DIVISION', 'EXPONENT', 'LPAR']):
                token_type = 'NEG'  # Treat '-' as negative number
            
            tokens.append((token_type, token_value))
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
        if isinstance(tree, float):
            return tree
        operator, *args = tree
        
        if operator in ['SINE', 'COSINE', 'TANGENT', 'COSECANT', 'SECANT', 'COTANGENT']:
            if len(args) == 1:
                arg = self.evaluate(args[0])
                if RAD != True:
                    arg = math.radians(arg)

                if operator == 'SINE':
                    return math.sin(arg)
                elif operator == 'COSINE':
                    return math.cos(arg)
                elif operator == 'TANGENT':
                    return math.tan(arg)
                elif operator == 'COSECANT':
                    return 1 / math.sin(arg)
                elif operator == 'SECANT':
                    return 1 / math.cos(arg)
                elif operator == 'COTANGENT':
                    return 1 / math.tan(arg)
            else:
                raise ValueError(f"Unknown function signature: {operator} takes one argument")

        if operator == 'EXPONENT':
            left, right = args
            left_val = self.evaluate(left)
            right_val = self.evaluate(right)
            return math.pow(left_val, right_val) 

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
            
            if operator == 'MINUS' or 'PLUS':
                right = self.term()
                term = (operator, term, right)
            elif operator == "NEG":
                right = self.term()
                term = ('NEG', right)
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
            value = self.previous()[1]
            if '.' in value:
                return float(value)
            else:
                return int(value)
        elif self.match('PI'):
            return math.pi
        elif self.match("EULER"):
            return math.e
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
        elif self.match('NEG'):
            return -self.primary()
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
