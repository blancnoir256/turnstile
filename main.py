# from fastapi import FastAPI
from typing import Optional, List, Dict
import tree

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}

#TODO FormulaとInferenceをコメントの通り完成させる。他のファイルを変更しても構わない。但し、一通りテストを行うこと。
class Formula:
# Formulaは推論に登場する一つの記号文である。
# 記号文はREADME.mdに従って[公式な記号文,非公式な記号文,記号文でないただの記号列]の状態を取りうる。
# 元の入力を生で保持する。
# このクラスのインスタンスの記号文を木構造で保持する。
# 非公式な記号文はそれから一意に変換される公式な記号文から変換される木構造として保持する。
# 記号文でない入力があればその一文を提示し、どのような規則に反しているかを述べ、エラーを投げる。
# このクラスのインスタンスの記号文が公式な記号文か非公式な記号文か記号文でないただの記号列かを保持する。
# 可能であれば非公式な記号文はどこが省略されているかを述べて変換する。
    def __init__(self, val: str):
        from token import LexerGenerator, FormalParser, InformalParser
        
        self.input_string: str = val
        self.symbolic_representation_tree: Optional[tree.Node] = None
        self.is_well_formed: bool = False
        self.is_formal: bool = False
        self.error_message: Optional[str] = None
        
        # 入力が空の場合はエラー
        if not val or val.strip() == "":
            self.error_message = "入力が空です。記号文ではありません。"
            raise ValueError(self.error_message)
        
        try:
            # まずトークン化を試みる
            lexer = LexerGenerator(val)
            
            # 公式な記号文としてパースを試みる
            try:
                lexer_formal = LexerGenerator(val)
                parser = FormalParser(lexer_formal)
                self.symbolic_representation_tree = parser.parse()
                self.is_well_formed = True
                self.is_formal = True
            except ValueError as e:
                # 公式な記号文としてパースできなかった場合、非公式な記号文としてパースを試みる
                try:
                    lexer_informal = LexerGenerator(val)
                    parser = InformalParser(lexer_informal)
                    self.symbolic_representation_tree = parser.parse()
                    self.is_well_formed = True
                    self.is_formal = False
                except ValueError as e2:
                    # 非公式な記号文としてもパースできない場合はエラー
                    self.error_message = f"記号文として解釈できません: {str(e2)}"
                    raise ValueError(self.error_message)
                    
        except ValueError as e:
            # トークン化やパースに失敗した場合
            self.error_message = f"記号文ではありません: {str(e)}"
            raise ValueError(self.error_message)
    
    def get_atoms(self) -> set:
        """記号文に含まれる全ての原子文(文記号)を取得する"""
        if not self.is_well_formed or self.symbolic_representation_tree is None:
            return set()
        
        atoms = set()
        self._collect_atoms(self.symbolic_representation_tree, atoms)
        return atoms
    
    def _collect_atoms(self, node: tree.Node, atoms: set):
        """木構造から原子文を再帰的に収集する"""
        if isinstance(node, tree.Atom):
            atoms.add(node.value)
        elif isinstance(node, tree.Operator):
            for arg in node.args:
                self._collect_atoms(arg, atoms)
    
    def evaluate(self, env: Dict[str, bool]) -> bool:
        """与えられた真偽値割り当てで記号文を評価する"""
        if not self.is_well_formed or self.symbolic_representation_tree is None:
            raise ValueError("整形式でない記号文は評価できません")
        return self.symbolic_representation_tree.evaluate(env)
    
    def __repr__(self) -> str:
        if self.symbolic_representation_tree:
            return str(self.symbolic_representation_tree)
        return self.input_string

class Inference:
# Inferenceは推論そのものである。
# 仮定と結論を持ち、README.mdのとおりに真偽値表を作成でき、意味論的妥当性を判断できる。
# 前提、結論、意味論的妥当性をTFで保持する。
    premises: List[Formula]
    conclusion: Formula

    def __init__(self, premises: List[Formula], conclusion: Formula):
        self.premises = premises
        self.conclusion = conclusion
        self.tf_table = None
        self._is_semantically_valid = None
        
        # 全ての前提と結論が整形式であることを確認
        for premise in premises:
            if not premise.is_well_formed:
                raise ValueError(f"前提に整形式でない記号文が含まれています: {premise.input_string}")
        if not conclusion.is_well_formed:
            raise ValueError(f"結論が整形式でない記号文です: {conclusion.input_string}")
    
    def get_all_atoms(self) -> set:
        """推論に含まれる全ての原子文を取得する"""
        atoms = set()
        for premise in self.premises:
            atoms.update(premise.get_atoms())
        atoms.update(self.conclusion.get_atoms())
        return atoms
    
    def generate_truth_table(self) -> List[Dict]:
        """真偽値表を生成する
        
        Returns:
            真偽値表の各行を辞書のリストとして返す
            各辞書は {原子文: 真偽値, 前提1: 真偽値, ..., 結論: 真偽値} の形式
        """
        atoms = sorted(self.get_all_atoms())  # ソートして順序を安定させる
        n = len(atoms)
        
        # 2^n 通りの真偽値の組み合わせを生成
        truth_table = []
        for i in range(2 ** n):
            # i のビットパターンから真偽値割り当てを生成
            env = {}
            for j, atom in enumerate(atoms):
                # 右から j 番目のビットが 1 なら True, 0 なら False
                env[atom] = bool((i >> (n - 1 - j)) & 1)
            
            # この環境での各前提と結論の真偽値を計算
            row = env.copy()
            for idx, premise in enumerate(self.premises):
                row[f"premise_{idx}"] = premise.evaluate(env)
            row["conclusion"] = self.conclusion.evaluate(env)
            
            truth_table.append(row)
        
        self.tf_table = truth_table
        return truth_table
    
    def is_semantically_valid(self) -> bool:
        """意味論的妥当性を判断する
        
        真偽値表の全ての行において、全ての前提が真の場合に結論も真であれば、
        この推論は意味論的に妥当である。
        
        Returns:
            意味論的に妥当であれば True, そうでなければ False
        """
        if self._is_semantically_valid is not None:
            return self._is_semantically_valid
        
        # 真偽値表が生成されていなければ生成する
        if self.tf_table is None:
            self.generate_truth_table()
        
        # 全ての行をチェック
        for row in self.tf_table:
            # 全ての前提が真かチェック
            all_premises_true = all(
                row[f"premise_{idx}"] for idx in range(len(self.premises))
            )
            
            # 全ての前提が真なのに結論が偽の行があれば、意味論的に妥当でない
            if all_premises_true and not row["conclusion"]:
                self._is_semantically_valid = False
                return False
        
        # 全ての行で条件を満たせば意味論的に妥当
        self._is_semantically_valid = True
        return True
    
    def get_counterexample(self) -> Optional[Dict]:
        """反例(全ての前提が真だが結論が偽である行)を取得する
        
        Returns:
            反例があればその行を返し、なければ None を返す
        """
        if self.tf_table is None:
            self.generate_truth_table()
        
        for row in self.tf_table:
            all_premises_true = all(
                row[f"premise_{idx}"] for idx in range(len(self.premises))
            )
            if all_premises_true and not row["conclusion"]:
                return row
        
        return None
    
    def print_truth_table(self):
        """真偽値表を見やすく表示する"""
        if self.tf_table is None:
            self.generate_truth_table()
        
        atoms = sorted(self.get_all_atoms())
        
        # ヘッダーを表示
        header = atoms + [f"P{i+1}" for i in range(len(self.premises))] + ["C"]
        print(" | ".join(header))
        print("-" * (len(" | ".join(header))))
        
        # 各行を表示
        for row in self.tf_table:
            values = []
            for atom in atoms:
                values.append("T" if row[atom] else "F")
            for idx in range(len(self.premises)):
                values.append("T" if row[f"premise_{idx}"] else "F")
            values.append("T" if row["conclusion"] else "F")
            print(" | ".join(values))
