from fastapi import FastAPI
from typing import Optional, List
import tree

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


class Formula:
    input_string:str = ""                   # 入力
    symbolic_representation_tree:tree.Node  # 公式な記号文として木構造にしたもの
    tf_table = None                         # 真理値表
    syntactic_derivation = None             # 統語論的方法による演繹の道筋

    def __init__(self,val):
        self.input_string = val
        self.is_well_formed = False         # 入力は記号文か？
        self.is_formal = False              # 入力は公式な記号文か？


class ronri:
    premises: List[Formula]
    conclusion: Formula