import re
from enum import Enum, auto

class Node:
    def __init__(self):
        raise NotImplementedError
    def __repr__(self) -> str:
        raise NotImplementedError
    def evaluate(self, env):
        raise NotImplementedError


class Atom(Node):
    def __init__(self, val):
        self.value = val
    def __repr__(self) -> str:
        return f"{self.value}"
    def evaluate(self, env):
        return env[self.value]


class Operator(Node):
    def __init__(self, symbol, *args):
        self.symbol = symbol
        self.args = args

    @property
    def left(self) -> Node:
        return self.args[0]
    @property
    def right(self) -> Node:
        return self.args[1]
    @property
    def child(self) -> Node:
        return self.args[0]

    def __repr__(self):
        if len(self.args) == 0:
            return f"{self.symbol}"
        if len(self.args) == 1:
            return f" {self.symbol}{self.args[0]} "
        if len(self.args) == 2:
            return f" ({self.args[0]}{self.symbol}{self.args[1]}) "
        else:
            return f"({f' {self.symbol} '.join(map(str, self.args))})"

    def evaluate(self, env):
        return super().evaluate(env)


class Not(Operator):
    def __init__(self, child):
        super().__init__("\u223C", child)

    def evaluate(self, env):
        return not self.child.evaluate(env)


class And(Operator):
    def __init__(self, left, right):
        super().__init__("\u2227", left, right)

    def evaluate(self, env):
        return self.left.evaluate(env) and self.right.evaluate(env)


class Or(Operator):
    def __init__(self, left, right):
        super().__init__("\u2228", left, right)
    
    def evaluate(self, env):
        return self.left.evaluate(env) or self.right.evaluate(env)


class Implies(Operator):
    def __init__(self, left, right):
        super().__init__("\u2192", left, right)

    def evaluate(self, env):
        return (not self.left.evaluate(env)) or self.right.evaluate(env)


class Equivalence(Operator):
    def __init__(self, left, right):
        super().__init__("\u2194", left, right)

    def evaluate(self, env):
        return self.left.evaluate(env) == self.right.evaluate(env)


class TokenType(Enum):
    ATOM = auto()       # P, Q...
    NOT = auto()        # ~
    AND = auto()        # &
    OR = auto()         # |
    IMPLIES = auto()    # ->
    EQUIV = auto()      # <->
    LPAREN = auto()     # (
    RPAREN = auto()     # )
    EOF = auto()        # End of File

class Token:
    def __init__(self, type: TokenType, value: str, line: int, col: int):
        self.type = type
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}', at {self.line}:{self.col})"

