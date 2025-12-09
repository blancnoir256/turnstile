from tree import Node, Atom, Operator, Not, And, Or, Implies, Equivalence

# (P->Q)/\(~P\/(Q<->R))
test = And(Implies(Atom("P"),Atom("Q")),Or(Not(Atom("P")),Equivalence(Atom("Q"),Atom("R"))))

print(test)