import string

INTEGER, PLUS, MINUS, MULT, DIV, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MULT', 'DIV', 'EOF'


class Token(object):

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token(type:{type}, value:{value})'.format(type=self.type,
                                                          value=self.value)

    def __repr__(self):
        return self.__str__()


class Interpreter(object):

    def __init__(self, text):
        self.text = text  # client string input
        self.pos = 0
        self.currentToken = None
        self.currentChar = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.currentChar = None
        else:
            self.currentChar = self.text[self.pos]

    def skipWhitespace(self):
        while self.currentChar is not None and self.currentChar.isspace():
            self.advance()

    def getNumber(self):
        result = ''

        while self.currentChar is not None and self.currentChar.isdigit():
            result += self.currentChar
            self.advance()

        return int(result)

    def getNextToken(self):

        while self.currentChar is not None:

            if self.currentChar.isspace():
                self.skipWhitespace()
                continue

            if self.currentChar.isdigit():
                return Token(INTEGER, self.getNumber())

            if self.currentChar == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.currentChar == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.currentChar == '*':
                self.advance()
                return Token(MULT, '*')

            if self.currentChar == '/':
                self.advance()
                return Token(DIV, '/')

            self.error()

        return Token(EOF, None)

    # for checking if next token is the one we expect
    # and expression is valid
    def eat(self, tokenType):
        if self.currentToken.type == tokenType:
            self.currentToken = self.getNextToken()
        else:
            self.error()

    def expr(self):
        self.currentToken = self.getNextToken()

        left = self.currentToken
        self.eat(INTEGER)

        op = self.currentToken
        if op.type == PLUS:
            self.eat(PLUS)
        elif op.type == MINUS:
            self.eat(MINUS)
        elif op.type == MULT:
            self.eat(MULT)
        elif op.type == DIV:
            self.eat(DIV)

        right = self.currentToken
        self.eat(INTEGER)

        if op.type == PLUS:
            result = left.value + right.value
        elif op.type == MINUS:
            result = left.value - right.value
        elif op.type == MULT:
            result = left.value * right.value
        elif op.type == DIV:
            result = left.value / right.value

        return result


def main():
    while True:
        try:
            text = raw_input('calc> ')
        except EOFError:
            break

        if not text:
            continue

        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
