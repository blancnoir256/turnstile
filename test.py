"""
Tests for token.py and tree.py modules.
This module tests the tokenization, parsing, and AST evaluation functionality.
"""
import sys
sys.path.insert(0, '.')  # Ensure we import local modules, not built-in token module

import tree
from token import (
    TokenType, Token, LexerGenerator, 
    StrictParser, FormalParser, InformalParser
)


def test_tree_atom():
    """Test Atom node creation, representation, and evaluation."""
    print("Testing Atom...")
    
    # Test creation and representation
    atom = tree.Atom('P')
    assert str(atom) == 'P', f"Expected 'P', got {str(atom)}"
    
    # Test evaluation
    assert atom.evaluate({'P': True}) == True
    assert atom.evaluate({'P': False}) == False
    
    # Test with subscripted atom
    atom2 = tree.Atom('P_1')
    assert str(atom2) == 'P_1'
    
    print("  ✓ Atom tests passed")


def test_tree_not():
    """Test Not operator."""
    print("Testing Not...")
    
    atom = tree.Atom('P')
    not_node = tree.Not(atom)
    
    # Test evaluation
    assert not_node.evaluate({'P': True}) == False
    assert not_node.evaluate({'P': False}) == True
    
    # Test representation (∼ is U+223C TILDE OPERATOR)
    assert '∼' in str(not_node) or '¬' in str(not_node) or '~' in str(not_node)
    
    print("  ✓ Not tests passed")


def test_tree_and():
    """Test And operator."""
    print("Testing And...")
    
    p = tree.Atom('P')
    q = tree.Atom('Q')
    and_node = tree.And(p, q)
    
    # Test evaluation (truth table)
    assert and_node.evaluate({'P': True, 'Q': True}) == True
    assert and_node.evaluate({'P': True, 'Q': False}) == False
    assert and_node.evaluate({'P': False, 'Q': True}) == False
    assert and_node.evaluate({'P': False, 'Q': False}) == False
    
    # Test representation
    assert '∧' in str(and_node)
    
    print("  ✓ And tests passed")


def test_tree_or():
    """Test Or operator."""
    print("Testing Or...")
    
    p = tree.Atom('P')
    q = tree.Atom('Q')
    or_node = tree.Or(p, q)
    
    # Test evaluation (truth table)
    assert or_node.evaluate({'P': True, 'Q': True}) == True
    assert or_node.evaluate({'P': True, 'Q': False}) == True
    assert or_node.evaluate({'P': False, 'Q': True}) == True
    assert or_node.evaluate({'P': False, 'Q': False}) == False
    
    # Test representation
    assert '∨' in str(or_node)
    
    print("  ✓ Or tests passed")


def test_tree_implies():
    """Test Implies operator."""
    print("Testing Implies...")
    
    p = tree.Atom('P')
    q = tree.Atom('Q')
    implies_node = tree.Implies(p, q)
    
    # Test evaluation (truth table for implication)
    assert implies_node.evaluate({'P': True, 'Q': True}) == True
    assert implies_node.evaluate({'P': True, 'Q': False}) == False
    assert implies_node.evaluate({'P': False, 'Q': True}) == True
    assert implies_node.evaluate({'P': False, 'Q': False}) == True
    
    # Test representation
    assert '→' in str(implies_node)
    
    print("  ✓ Implies tests passed")


def test_tree_equivalence():
    """Test Equivalence operator."""
    print("Testing Equivalence...")
    
    p = tree.Atom('P')
    q = tree.Atom('Q')
    equiv_node = tree.Equivalence(p, q)
    
    # Test evaluation (truth table for equivalence)
    assert equiv_node.evaluate({'P': True, 'Q': True}) == True
    assert equiv_node.evaluate({'P': True, 'Q': False}) == False
    assert equiv_node.evaluate({'P': False, 'Q': True}) == False
    assert equiv_node.evaluate({'P': False, 'Q': False}) == True
    
    # Test representation
    assert '↔' in str(equiv_node)
    
    print("  ✓ Equivalence tests passed")


def test_token_types():
    """Test TokenType enum."""
    print("Testing TokenType...")
    
    # Just verify the enum values exist
    assert TokenType.ATOM
    assert TokenType.NOT
    assert TokenType.AND
    assert TokenType.OR
    assert TokenType.IMPLIES
    assert TokenType.EQUIV
    assert TokenType.LPAREN
    assert TokenType.RPAREN
    assert TokenType.LBRACKET
    assert TokenType.RBRACKET
    
    print("  ✓ TokenType tests passed")


def test_token_class():
    """Test Token class."""
    print("Testing Token class...")
    
    token = Token(TokenType.ATOM, 'P')
    assert token.type == TokenType.ATOM
    assert token.value == 'P'
    assert 'ATOM' in repr(token)
    assert 'P' in repr(token)
    
    print("  ✓ Token class tests passed")


def test_lexer_simple():
    """Test LexerGenerator with simple inputs."""
    print("Testing LexerGenerator (simple)...")
    
    # Test single atom
    lexer = LexerGenerator('P')
    assert len(lexer.tokens) == 1
    assert lexer.tokens[0].type == TokenType.ATOM
    assert lexer.tokens[0].value == 'P'
    
    # Test atom with subscript
    lexer = LexerGenerator('P_1')
    assert len(lexer.tokens) == 1
    assert lexer.tokens[0].value == 'P_1'
    
    # Test NOT
    lexer = LexerGenerator('!P')
    assert len(lexer.tokens) == 2
    assert lexer.tokens[0].type == TokenType.NOT
    assert lexer.tokens[1].type == TokenType.ATOM
    
    print("  ✓ LexerGenerator (simple) tests passed")


def test_lexer_binary_operators():
    """Test LexerGenerator with binary operators."""
    print("Testing LexerGenerator (binary operators)...")
    
    # Test AND
    lexer = LexerGenerator('P & Q')
    assert len(lexer.tokens) == 3
    assert lexer.tokens[1].type == TokenType.AND
    
    # Test OR
    lexer = LexerGenerator('P | Q')
    assert len(lexer.tokens) == 3
    assert lexer.tokens[1].type == TokenType.OR
    
    # Test IMPLIES
    lexer = LexerGenerator('P -> Q')
    assert len(lexer.tokens) == 3
    assert lexer.tokens[1].type == TokenType.IMPLIES
    
    # Test EQUIV
    lexer = LexerGenerator('P <-> Q')
    assert len(lexer.tokens) == 3
    assert lexer.tokens[1].type == TokenType.EQUIV
    
    print("  ✓ LexerGenerator (binary operators) tests passed")


def test_lexer_parentheses():
    """Test LexerGenerator with parentheses."""
    print("Testing LexerGenerator (parentheses)...")
    
    lexer = LexerGenerator('(P & Q)')
    assert len(lexer.tokens) == 5
    assert lexer.tokens[0].type == TokenType.LPAREN
    assert lexer.tokens[4].type == TokenType.RPAREN
    
    # Test brackets
    lexer = LexerGenerator('[P | Q]')
    assert len(lexer.tokens) == 5
    assert lexer.tokens[0].type == TokenType.LBRACKET
    assert lexer.tokens[4].type == TokenType.RBRACKET
    
    print("  ✓ LexerGenerator (parentheses) tests passed")


def test_lexer_unicode_symbols():
    """Test LexerGenerator with Unicode logical symbols."""
    print("Testing LexerGenerator (Unicode symbols)...")
    
    # Test Unicode NOT
    lexer = LexerGenerator('~P')
    assert lexer.tokens[0].type == TokenType.NOT
    
    # Test Unicode AND
    lexer = LexerGenerator('P ∧ Q')
    assert lexer.tokens[1].type == TokenType.AND
    
    # Test Unicode OR
    lexer = LexerGenerator('P ∨ Q')
    assert lexer.tokens[1].type == TokenType.OR
    
    # Test Unicode IMPLIES
    lexer = LexerGenerator('P → Q')
    assert lexer.tokens[1].type == TokenType.IMPLIES
    
    # Test Unicode EQUIV
    lexer = LexerGenerator('P ↔ Q')
    assert lexer.tokens[1].type == TokenType.EQUIV
    
    print("  ✓ LexerGenerator (Unicode symbols) tests passed")


def test_strict_parser_atom():
    """Test StrictParser with atoms."""
    print("Testing StrictParser (atoms)...")
    
    lexer = LexerGenerator('P')
    parser = StrictParser(lexer)
    ast = parser.parse()
    
    assert isinstance(ast, tree.Atom)
    assert ast.value == 'P'
    
    print("  ✓ StrictParser (atoms) tests passed")


def test_strict_parser_not():
    """Test StrictParser with NOT."""
    print("Testing StrictParser (NOT)...")
    
    lexer = LexerGenerator('!P')
    parser = StrictParser(lexer)
    ast = parser.parse()
    
    assert isinstance(ast, tree.Not)
    assert isinstance(ast.child, tree.Atom)
    
    print("  ✓ StrictParser (NOT) tests passed")


def test_strict_parser_binary():
    """Test StrictParser with binary operators."""
    print("Testing StrictParser (binary operators)...")
    
    # Test AND
    lexer = LexerGenerator('(P & Q)')
    parser = StrictParser(lexer)
    ast = parser.parse()
    assert isinstance(ast, tree.And)
    assert isinstance(ast.left, tree.Atom)
    assert isinstance(ast.right, tree.Atom)
    
    # Test OR
    lexer = LexerGenerator('(P | Q)')
    parser = StrictParser(lexer)
    ast = parser.parse()
    assert isinstance(ast, tree.Or)
    
    # Test IMPLIES
    lexer = LexerGenerator('(P -> Q)')
    parser = StrictParser(lexer)
    ast = parser.parse()
    assert isinstance(ast, tree.Implies)
    
    # Test EQUIV
    lexer = LexerGenerator('(P <-> Q)')
    parser = StrictParser(lexer)
    ast = parser.parse()
    assert isinstance(ast, tree.Equivalence)
    
    print("  ✓ StrictParser (binary operators) tests passed")


def test_strict_parser_nested():
    """Test StrictParser with nested expressions."""
    print("Testing StrictParser (nested)...")
    
    # Test ((P & Q) -> R)
    lexer = LexerGenerator('((P & Q) -> R)')
    parser = StrictParser(lexer)
    ast = parser.parse()
    
    assert isinstance(ast, tree.Implies)
    assert isinstance(ast.left, tree.And)
    assert isinstance(ast.right, tree.Atom)
    
    print("  ✓ StrictParser (nested) tests passed")


def test_informal_parser_basic():
    """Test InformalParser with basic expressions."""
    print("Testing InformalParser (basic)...")
    
    # Test simple atom
    lexer = LexerGenerator('P')
    parser = InformalParser(lexer)
    ast = parser.parse()
    assert isinstance(ast, tree.Atom)
    
    # Test NOT
    lexer = LexerGenerator('!P')
    parser = InformalParser(lexer)
    ast = parser.parse()
    assert isinstance(ast, tree.Not)
    
    print("  ✓ InformalParser (basic) tests passed")


def test_informal_parser_no_parens():
    """Test InformalParser without parentheses (precedence)."""
    print("Testing InformalParser (no parentheses)...")
    
    # Test P & Q (should work without parentheses)
    lexer = LexerGenerator('P & Q')
    parser = InformalParser(lexer)
    ast = parser.parse()
    assert isinstance(ast, tree.And)
    
    # Test P | Q
    lexer = LexerGenerator('P | Q')
    parser = InformalParser(lexer)
    ast = parser.parse()
    assert isinstance(ast, tree.Or)
    
    print("  ✓ InformalParser (no parentheses) tests passed")


def test_informal_parser_precedence():
    """Test InformalParser operator precedence."""
    print("Testing InformalParser (precedence)...")
    
    # Test P & Q -> R (AND binds tighter than IMPLIES)
    lexer = LexerGenerator('P & Q -> R')
    parser = InformalParser(lexer)
    ast = parser.parse()
    
    # Should parse as (P & Q) -> R
    assert isinstance(ast, tree.Implies)
    assert isinstance(ast.left, tree.And)
    assert isinstance(ast.right, tree.Atom)
    
    print("  ✓ InformalParser (precedence) tests passed")


def test_informal_parser_left_associativity():
    """Test InformalParser left associativity."""
    print("Testing InformalParser (left associativity)...")
    
    # Test P & Q & R (should parse left-to-right)
    lexer = LexerGenerator('P & Q & R')
    parser = InformalParser(lexer)
    ast = parser.parse()
    
    # Should parse as (P & Q) & R
    assert isinstance(ast, tree.And)
    assert isinstance(ast.left, tree.And)
    assert isinstance(ast.right, tree.Atom)
    
    print("  ✓ InformalParser (left associativity) tests passed")


def test_informal_parser_brackets():
    """Test InformalParser with square brackets."""
    print("Testing InformalParser (brackets)...")
    
    # Test [P & Q]
    lexer = LexerGenerator('[P & Q]')
    parser = InformalParser(lexer)
    ast = parser.parse()
    assert isinstance(ast, tree.And)
    
    print("  ✓ InformalParser (brackets) tests passed")


def test_informal_parser_mixed_operators_error():
    """Test InformalParser rejects mixed AND/OR at same level."""
    print("Testing InformalParser (mixed operators error)...")
    
    # Test P & Q | R should raise error
    lexer = LexerGenerator('P & Q | R')
    parser = InformalParser(lexer)
    
    try:
        ast = parser.parse()
        # If this doesn't raise an error, the test should fail
        assert False, "Expected ValueError for mixed AND/OR operators"
    except ValueError as e:
        # This is expected
        assert '∧' in str(e) or '∨' in str(e) or 'AND' in str(e).upper() or 'OR' in str(e).upper()
    
    print("  ✓ InformalParser (mixed operators error) tests passed")


def test_end_to_end():
    """Test end-to-end parsing and evaluation."""
    print("Testing end-to-end...")
    
    # Test parsing and evaluating a complex formula using InformalParser
    lexer = LexerGenerator('(P -> Q) & (Q -> R)')
    parser = InformalParser(lexer)
    ast = parser.parse()
    
    # Evaluate with P=T, Q=T, R=T
    result = ast.evaluate({'P': True, 'Q': True, 'R': True})
    assert result == True
    
    # Evaluate with P=T, Q=F, R=T
    result = ast.evaluate({'P': True, 'Q': False, 'R': True})
    assert result == False  # (T -> F) & (F -> T) = F & T = F
    
    # Test with StrictParser (needs full parenthesization)
    lexer2 = LexerGenerator('((P -> Q) & (Q -> R))')
    parser2 = StrictParser(lexer2)
    ast2 = parser2.parse()
    result2 = ast2.evaluate({'P': True, 'Q': True, 'R': True})
    assert result2 == True
    
    print("  ✓ End-to-end tests passed")


def run_all_tests():
    """Run all test functions."""
    print("=" * 60)
    print("Running Tests for token.py and tree.py")
    print("=" * 60)
    
    # Tree tests
    print("\n--- Tree Module Tests ---")
    test_tree_atom()
    test_tree_not()
    test_tree_and()
    test_tree_or()
    test_tree_implies()
    test_tree_equivalence()
    
    # Token tests
    print("\n--- Token Module Tests ---")
    test_token_types()
    test_token_class()
    
    # Lexer tests
    print("\n--- Lexer Tests ---")
    test_lexer_simple()
    test_lexer_binary_operators()
    test_lexer_parentheses()
    test_lexer_unicode_symbols()
    
    # Parser tests
    print("\n--- Parser Tests ---")
    test_strict_parser_atom()
    test_strict_parser_not()
    test_strict_parser_binary()
    test_strict_parser_nested()
    
    # Informal parser tests
    print("\n--- Informal Parser Tests ---")
    test_informal_parser_basic()
    test_informal_parser_no_parens()
    test_informal_parser_precedence()
    test_informal_parser_left_associativity()
    test_informal_parser_brackets()
    test_informal_parser_mixed_operators_error()
    
    # End-to-end tests
    print("\n--- End-to-End Tests ---")
    test_end_to_end()
    
    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)


if __name__ == '__main__':
    run_all_tests()