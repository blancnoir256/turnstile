class Node:
    def __init__(self):
        pass
    
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
            return f"{self.symbol}{self.args[0]}"
        if len(self.args) == 2:
            return f"({self.args[0]}{self.symbol}{self.args[1]})"
        else:
            return f"({f' {self.symbol} '.join(map(str, self.args))})"

    def evaluate(self, env):
        return super().evaluate(env)


class Not(Operator):
    def __init__(self, child):
        # "~","\u223C" 但しここでは"~"
        super().__init__(chr(0x7E), child)

    def evaluate(self, env):
        return not self.child.evaluate(env)


class And(Operator):
    def __init__(self, left, right):
        # "∧","\u2227" 但しここでは"&"
        super().__init__(chr(0x26), left, right)

    def evaluate(self, env):
        return self.left.evaluate(env) and self.right.evaluate(env)


class Or(Operator):
    def __init__(self, left, right):
        # "∨","\u2228" 但しここでは"|"
        super().__init__(chr(0x7C), left, right)
    
    def evaluate(self, env):
        return self.left.evaluate(env) or self.right.evaluate(env)


class Implies(Operator):
    def __init__(self, left, right):
        # "\u2192" 但しここでは"->"
        super().__init__(chr(0x2D)+chr(0x3E), left, right)

    def evaluate(self, env):
        return (not self.left.evaluate(env)) or self.right.evaluate(env)


class Equivalence(Operator):
    def __init__(self, left, right):
        # "\u2194" 但しここでは"<->"
        super().__init__(chr(0x3C)+chr(0x2D)+chr(0x3E), left, right)

    def evaluate(self, env):
        return self.left.evaluate(env) == self.right.evaluate(env)
