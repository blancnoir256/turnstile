import re
from enum import Enum, auto
from typing import Optional
import tree

class TokenType(Enum):
    ATOM = auto()
    NOT = auto()
    AND = auto()
    OR = auto()
    IMPLIES = auto()
    EQUIV = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACKET = auto()
    RBRACKET = auto()

class Token:
    def __init__(self, type: TokenType, value: str):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}')"


TOKEN_DEFINITIONS = {
    TokenType.NOT:     ["!", "~", "～"],
    TokenType.AND:     ["&", "∧", "/\\"],
    TokenType.OR:      ["|", "∨", "\\/"],
    TokenType.IMPLIES: ["->", "→", "=>"],
    TokenType.EQUIV:   ["<->", "↔", "<=>"],
    TokenType.LPAREN:  ["("],
    TokenType.RPAREN:  [")"],
    TokenType.LBRACKET: ["["],
    TokenType.RBRACKET: ["]"],
}

class LexerGenerator:
    def __init__(self, text:str):
        self.symbol_map:dict[str, TokenType] = {}
        self._build_map()
        self.pattern = self._build_regex()
        self.pos = 0
        self.tokens = self.tokenize(text)

    def _build_map(self):
        for token_type, symbols in TOKEN_DEFINITIONS.items():
            for s in symbols:
                # 重複チェック
                if s in self.symbol_map:
                    raise ValueError(f"定義エラー: 記号 '{s}' が重複しています")
                self.symbol_map[s] = token_type

    def _build_regex(self):
        # tokenを切り分ける用のパターンを作成する
        sorted_symbols = sorted(self.symbol_map.keys(), key=len, reverse=True)
        escaped_symbols = [re.escape(s) for s in sorted_symbols]
        ops_pattern = '|'.join(escaped_symbols)
        atom_pattern = r'[P-Z](?:_[0-9]+)?'
        return re.compile(f'\\s*({ops_pattern}|{atom_pattern})\\s*')

    def tokenize(self, text:str) -> list[Token]:
        raw_tokens = [t for t in self.pattern.split(text) if t]
        results:list[Token] = []
        # token作成
        for raw in raw_tokens:
            # 1. マップにあれば演算子
            if raw in self.symbol_map:
                results.append(Token(self.symbol_map[raw], raw))
            # 2. なければ原子文かチェック
            elif re.match(r'^[P-Z](?:_[0-9]+)?$', raw):
                results.append(Token(TokenType.ATOM, raw))
            else:
                raise ValueError(f"未知のトークン: '{raw}'")
        return results

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        else:
            return None

    def consume(self, expected_type:Optional[TokenType]=None) -> Token:
        token = self.peek()
        if token is None:
            raise ValueError("Unexpected EOF")
        if expected_type and token.type != expected_type:
            raise ValueError(f"Expected {expected_type.name} but got {token.type.name}")
        self.pos += 1
        return token


class StrictParser:
    def __init__(self, lexer:LexerGenerator):
        self.lexer = lexer

    def parse(self) -> tree.Node:
        ast = self._parse_wff()
        if self.lexer.peek() is not None:
            raise ValueError("Extra tokens at end")
        return ast

    def _parse_wff(self) -> tree.Node:
        from tree import Atom, Not, And, Or, Implies, Equivalence
        
        token = self.lexer.peek()
        if token is None:
            raise ValueError("Empty")

        if token.type == TokenType.ATOM:
            self.lexer.consume()
            return Atom(token.value)

        if token.type == TokenType.NOT:
            self.lexer.consume()
            return Not(self._parse_wff())

        if token.type == TokenType.LPAREN:
            self.lexer.consume(TokenType.LPAREN)
            left = self._parse_wff()
            
            op = self.lexer.consume()
            right = self._parse_wff()
            self.lexer.consume(TokenType.RPAREN)
            
            if op.type == TokenType.AND:
                return And(left, right)
            elif op.type == TokenType.OR:
                return Or(left, right)
            elif op.type == TokenType.IMPLIES:
                return Implies(left, right)
            elif op.type == TokenType.EQUIV:
                return Equivalence(left, right)
            else:
                raise ValueError("Expected binary operator")

        raise ValueError(f"Invalid formal token: {token.value}")


class FormalParser:
    """公式な記号文のみをパースする"""
    def __init__(self, lexer: LexerGenerator):
        self.lexer = lexer

    def parse(self) -> tree.Node:
        ast = self._parse_wff()
        if self.lexer.peek() is not None:
            raise ValueError("Extra tokens at end")
        return ast

    def _parse_wff(self) -> tree.Node:
        from tree import Atom, Not, And, Or, Implies, Equivalence
        
        token = self.lexer.peek()
        if token is None:
            raise ValueError("Empty")

        if token.type == TokenType.ATOM:
            self.lexer.consume()
            return Atom(token.value)

        if token.type == TokenType.NOT:
            self.lexer.consume()
            return Not(self._parse_wff())

        if token.type == TokenType.LPAREN:
            self.lexer.consume(TokenType.LPAREN)
            left = self._parse_wff()
            
            op = self.lexer.consume()
            right = self._parse_wff()
            self.lexer.consume(TokenType.RPAREN)
            
            if op.type == TokenType.AND:
                return And(left, right)
            elif op.type == TokenType.OR:
                return Or(left, right)
            elif op.type == TokenType.IMPLIES:
                return Implies(left, right)
            elif op.type == TokenType.EQUIV:
                return Equivalence(left, right)
            else:
                raise ValueError("Expected binary operator")

        raise ValueError(f"Invalid formal token: {token.value}")


class InformalParser:
    """非公式な記号文もパースする(優先度と左寄せ対応)"""
    def __init__(self, lexer: LexerGenerator):
        self.lexer = lexer
        # 演算子の優先順位を定義 (値が大きいほど優先度が高い)
        self.precedence = {
            TokenType.EQUIV: 1,    # ↔ 最低優先度
            TokenType.IMPLIES: 1,  # → 最低優先度
            TokenType.OR: 2,       # ∨ 高優先度
            TokenType.AND: 2,      # ∧ 高優先度
        }

    def parse(self) -> tree.Node:
        """非公式な記号文をパースする"""
        ast = self._parse_expr(0, None)
        if self.lexer.peek() is not None:
            raise ValueError("Extra tokens at end")
        return ast

    def _parse_expr(self, min_precedence: int, last_op_type: Optional[TokenType] = None) -> tree.Node:
        """優先順位を考慮して式をパースする
        
        Args:
            min_precedence: この呼び出しで処理する最小の優先度
            last_op_type: 同じ優先度レベルで直前に使用された演算子の種類
                         (ANDとORの混在を防ぐため)
        """
        from tree import Atom, Not, And, Or, Implies, Equivalence
        
        # 左辺をパース
        left = self._parse_primary()
        
        # 二項演算子を処理
        while True:
            token = self.lexer.peek()
            if token is None:
                break
            
            # 閉じ括弧ならここで終了
            if token.type in (TokenType.RPAREN, TokenType.RBRACKET):
                break
            
            # 演算子でない、または優先度が低すぎる場合は終了
            if token.type not in self.precedence:
                break
            
            precedence = self.precedence[token.type]
            if precedence < min_precedence:
                break
            
            # 同じ優先度レベルで異なる演算子が混在していないかチェック
            # ANDとORは同じ優先度(2)だが、混在してはいけない
            if precedence == 2 and last_op_type is not None:
                # 同じ優先度レベルで、前回と異なる演算子が来た場合
                if last_op_type != token.type:
                    # ANDとORの混在を検出
                    if {last_op_type, token.type} == {TokenType.AND, TokenType.OR}:
                        raise ValueError(
                            f"結合子∧と∨が同じ優先順位で同時に出現しています。括弧を使用してください。"
                        )
            
            # 演算子を消費
            op = self.lexer.consume()
            
            # 左結合なので同じ優先度の演算子は precedence + 1 で再帰
            # ただし、同じ演算子タイプを渡して混在チェックができるようにする
            if precedence == min_precedence:
                # 同じ優先度レベルで続けている場合、演算子タイプを伝播
                right = self._parse_expr(precedence + 1, op.type)
            else:
                # より高い優先度レベルに入る場合、演算子タイプをリセット
                right = self._parse_expr(precedence + 1, None)
            
            # ASTノードを構築
            if op.type == TokenType.AND:
                left = And(left, right)
            elif op.type == TokenType.OR:
                left = Or(left, right)
            elif op.type == TokenType.IMPLIES:
                left = Implies(left, right)
            elif op.type == TokenType.EQUIV:
                left = Equivalence(left, right)
            
            # 次のループのために演算子タイプを更新
            last_op_type = op.type
        
        return left

    def _parse_primary(self) -> tree.Node:
        """一次式(原子文、否定、括弧で囲まれた式)をパースする"""
        from tree import Atom, Not
        
        token = self.lexer.peek()
        if token is None:
            raise ValueError("Unexpected end of input")
        
        # 原子文
        if token.type == TokenType.ATOM:
            self.lexer.consume()
            return Atom(token.value)
        
        # 否定
        if token.type == TokenType.NOT:
            self.lexer.consume()
            return Not(self._parse_primary())
        
        # 括弧 ( )
        if token.type == TokenType.LPAREN:
            self.lexer.consume(TokenType.LPAREN)
            # 括弧内は新しいスコープなので last_op_type をリセット
            expr = self._parse_expr(0, None)
            self.lexer.consume(TokenType.RPAREN)
            return expr
        
        # 角括弧 [ ]
        if token.type == TokenType.LBRACKET:
            self.lexer.consume(TokenType.LBRACKET)
            # 括弧内は新しいスコープなので last_op_type をリセット
            expr = self._parse_expr(0, None)
            self.lexer.consume(TokenType.RBRACKET)
            return expr
        
        raise ValueError(f"Unexpected token: {token.value}")
