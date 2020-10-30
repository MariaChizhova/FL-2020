import sys


class Lexer:
    def __init__(self, s):
        self.row = 0
        self.pos = 0
        self.lex = self.flexer(s)
        self.skip = False

    def skipped(self):
        return self.skip

    def flexer(self, s):
        self.skip = False
        for c in s:
            self.pos += 1
            if c == " " or c == '\t':
                self.skip = True
                continue
            elif c == "\n":
                self.skip = True
                self.row += 1
                self.pos = 0
                continue
            yield c
            self.skip = False
        while True:
            yield '\0'


class Parser:

    def __init__(self, s):
        self.lex = Lexer(s)
        self.current = next(self.lex.lex)

    def accept(self, c):
        if self.current == c:
            self.current = next(self.lex.lex)
            return True
        return False

    def expect(self, c):
        if self.current == c:
            self.current = next(self.lex.lex)
            return True
        #    print("Unexpected character. Expected", c)
        return False

    def parse_word(self, alphabet):
        buffer = ''
        self.lex.skip = False
        while not self.lex.skipped() and self.current in alphabet:
            buffer += self.current
            self.current = next(self.lex.lex)
        return buffer

    def expect_word(self, word):
        buffer = ''
        self.lex.skip = False
        for ind in range(len(word)):
            if self.lex.skip:
                return False
            buffer += self.current
            self.current = next(self.lex.lex)
        return buffer == word

    def skip_word(self):
        def is_alpha_num__():
            return self.current.isalpha() or self.current == '_' or self.current.isdigit()

        if self.current.isalpha() or self.current == '_':
            self.current = next(self.lex.lex)
        else:
            return False

        if not self.lex.skip:
            while not self.lex.skipped() and is_alpha_num__():
                self.current = next(self.lex.lex)

        return True

    def run(self):
        if not self.skip_word():
            return False
        if not self.current == '.':
            if self.expect_word(':-'):
                if self.disj() and self.expect('.'):
                    return True
            return False
        else:
            return True

    def disj(self):
        l = self.conj()
        if self.accept(';'):
            r = self.disj()
            if not r:
                return False
            return True
        return l

    def conj(self):
        l = self.literals()
        if self.accept(','):
            r = self.conj()
            if not r:
                return False
            return True
        return l

    def literals(self):
        if self.accept('('):
            r = self.disj()
            if self.expect(')'):
                return r
            return False
        return self.skip_word()


def tests():
    assert Parser("f.").run()
    assert Parser("f :- g.").run()
    assert Parser("f :- g, h; t.").run()
    assert Parser("f :- g, (h; t).").run()
    assert Parser("f :-(g, (f)).").run()
    assert Parser("f :- g. f :- h.").run()
    assert not Parser("f : - g. f :- h.").run()
    assert not Parser("f : -(g, (f)).").run()
    assert not Parser("f").run()
    assert not Parser(":- f.").run()
    assert not Parser("f :- .").run()
    assert not Parser("f :- g; h, .").run()
    assert not Parser("f :- (g; (f).").run()
    assert not Parser("f :- g).").run()
    assert not Parser("f :- (f, g)).").run()
    assert not Parser("f \n:-\ng").run()
    assert not Parser("f \n:-\ng, f)").run()
    assert not Parser("f :-(g, (((f)).").run()
    assert Parser("fgh :- h.").run()
    assert not Parser("1gh :- h.").run()
    assert Parser("o_o.").run()
    assert Parser("f :- gh.").run()
    assert Parser("f :- g_h.").run()


if __name__ == "__main__":
    tests()
    filename = "test.txt"  # sys.argv[1]
    file = open(filename, 'r')
    lines = file.read()
    parts = []
    s = ""
    for line in lines:
        s += line
        if line == '.':
            parts.append(s)
            s = ""
    if s:
        parts.append(s)
    #  print(parts)
    for i in parts:
        #   print(i)
        if i != '\n':
            p = Parser(i)
            res = p.run()
            if not res:
                print("Failed to parse.", "pos = ", p.lex.pos, ", row = ", p.lex.row)
