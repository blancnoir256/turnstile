from tree import Node, Atom, Operator, Not, And, Or, Implies, Equivalence

# (P->Q)/\(~P\/(Q<->R))
test = And(Implies(Atom("P"),Atom("Q")),Or(Not(Atom("P")),Equivalence(Atom("Q"),Atom("R"))))

print(test)

from tokenizer import LexerGenerator

test_text = "(P->Q)&(~P|(Q<->R))"
test = LexerGenerator(test_text).tokens
print(test)

