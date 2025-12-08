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
        self.input_string: str = val
        self.symbolic_representation_tree: Optional[tree.Node] = None
        self.is_well_formed: bool = False
        self.is_formal: bool = False

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
