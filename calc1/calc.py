import string

INTEGER, OP, EOF, WHITESPACE = 'INTEGER', 'OP', 'EOF', 'WHITESPACE'


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

    def error(self):
        raise Exception('Error parsing input')

    def stripWhitespace(self):
        text = self.text
        for ws in string.whitespace:
            text = text.replace(ws, '')

        return text

    def getNumber(self, text):
        number = ''
        start = self.pos

        for char in text[start:]:
            if char.isdigit():
                number = number + char
                self.pos += 1
            else:
                break

        return int(number)

    def getNextToken(self):

        #text = self.stripWhitespace()
        text = self.text

        if self.pos > len(text) - 1:
            return Token(EOF, None)

        currentChar = text[self.pos]

        if currentChar.isdigit():
            number = self.getNumber(text)
            token = Token(INTEGER, number)
            return token

        if currentChar in ('+', '-'):
            token = Token(OP, currentChar)
            self.pos += 1
            return token

        if currentChar in string.whitespace:
            token = Token(WHITESPACE, currentChar)
            self.pos += 1
            return token

        self.error()

    # for checking if next token is the one we expect
    # and expression is valid
    def eat(self, tokenType):
        if self.currentToken.type == tokenType:
            self.currentToken = self.getNextToken()
        else:
            self.error()

    def eatWhitespace(self):
        while self.currentToken.type == WHITESPACE:
            self.eat(WHITESPACE)
            continue

    def expr(self):
        self.currentToken = self.getNextToken()

        self.eatWhitespace()

        left = self.currentToken
        self.eat(INTEGER)

        self.eatWhitespace()

        op = self.currentToken
        self.eat(OP)

        self.eatWhitespace()

        right = self.currentToken
        self.eat(INTEGER)

        if op.value == '+':
            result = left.value + right.value
        elif op.value == '-':
            result = left.value - right.value

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
