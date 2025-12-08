from fastapi import FastAPI
from typing import Optional, List, Dict, Tuple
import tree

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}


class Formula:
    def __init__(self, val: str):
        self.input_string: str = val
        self.symbolic_representation_tree: Optional[tree.Node] = None
        self.tf_table: Optional[List[Dict[str, bool]]] = None
        self.syntactic_derivation: Optional[List[str]] = None
        self.is_well_formed: bool = False
        self.is_formal: bool = False


class Inference:
    premises: List[Formula]
    conclusion: Formula

    def __init__(self, premises: List[Formula], conclusion: Formula):
        self.premises = premises
        self.conclusion = conclusion

