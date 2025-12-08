"""
Formula と Inference の使用例を示すデモンストレーション
"""
import sys
sys.path.insert(0, '/home/runner/work/turnstile/turnstile')

from main import Formula, Inference

def demo_formula():
    """Formulaクラスの使用例"""
    print("=" * 60)
    print("Formula クラスのデモンストレーション")
    print("=" * 60)
    print()
    
    # 1. 公式な記号文
    print("1. 公式な記号文の例:")
    formulas_formal = [
        "P",
        "~P",
        "(P∧Q)",
        "(P∨Q)",
        "(P→Q)",
        "(P↔Q)",
        "((P∧Q)→R)"
    ]
    
    for formula_str in formulas_formal:
        f = Formula(formula_str)
        print(f"  入力: {formula_str}")
        print(f"    整形式: {f.is_well_formed}")
        print(f"    公式: {f.is_formal}")
        print(f"    原子文: {sorted(f.get_atoms())}")
        print(f"    木構造: {f}")
        print()
    
    # 2. 非公式な記号文
    print("2. 非公式な記号文の例:")
    formulas_informal = [
        "P∧Q",           # 最外括弧の省略
        "[P∧Q]",         # 角括弧の使用
        "P∧Q→R",         # 優先順位による括弧省略
        "P∧Q∧R",         # 左寄せ(連言)
        "P∨Q∨R",         # 左寄せ(選言)
        "P&Q",           # 代替記号
        "P|Q",           # 代替記号
        "P->Q",          # 代替記号
    ]
    
    for formula_str in formulas_informal:
        f = Formula(formula_str)
        print(f"  入力: {formula_str}")
        print(f"    整形式: {f.is_well_formed}")
        print(f"    公式: {f.is_formal}")
        print(f"    原子文: {sorted(f.get_atoms())}")
        print(f"    木構造: {f}")
        print()
    
    # 3. 無効な記号列
    print("3. 無効な記号列の例:")
    invalid_formulas = [
        "",              # 空文字列
        "P#Q",           # 未知のトークン
        "P∧Q∨R",         # ∧と∨の混在(括弧なし)
        "(P∧Q",          # 括弧の不一致
        "P Q",           # 演算子なし
    ]
    
    for formula_str in invalid_formulas:
        try:
            f = Formula(formula_str)
            print(f"  入力: '{formula_str}' - 予期せず成功")
        except ValueError as e:
            print(f"  入力: '{formula_str}'")
            print(f"    エラー: {e}")
            print()

def demo_inference():
    """Inferenceクラスの使用例"""
    print("=" * 60)
    print("Inference クラスのデモンストレーション")
    print("=" * 60)
    print()
    
    # 1. Modus Ponens (妥当)
    print("1. Modus Ponens (P, P→Q ⊢ Q):")
    p1 = Formula("P")
    p2 = Formula("P→Q")
    c1 = Formula("Q")
    inf1 = Inference([p1, p2], c1)
    
    print(f"  前提: {p1}, {p2}")
    print(f"  結論: {c1}")
    print(f"  原子文: {sorted(inf1.get_all_atoms())}")
    print(f"  意味論的に妥当: {inf1.is_semantically_valid()}")
    print("  真偽値表:")
    inf1.print_truth_table()
    print()
    
    # 2. 妥当でない推論
    print("2. 妥当でない推論 (P ⊢ Q):")
    p3 = Formula("P")
    c2 = Formula("Q")
    inf2 = Inference([p3], c2)
    
    print(f"  前提: {p3}")
    print(f"  結論: {c2}")
    print(f"  意味論的に妥当: {inf2.is_semantically_valid()}")
    counterexample = inf2.get_counterexample()
    if counterexample:
        print(f"  反例が見つかりました:")
        for key, value in counterexample.items():
            if not key.startswith("premise_") and key != "conclusion":
                print(f"    {key} = {value}")
        print(f"    前提0 = {counterexample['premise_0']}")
        print(f"    結論 = {counterexample['conclusion']}")
    print()
    
    # 3. 三段論法 (妥当)
    print("3. 三段論法 (P→Q, Q→R ⊢ P→R):")
    p4 = Formula("P→Q")
    p5 = Formula("Q→R")
    c3 = Formula("P→R")
    inf3 = Inference([p4, p5], c3)
    
    print(f"  前提: {p4}, {p5}")
    print(f"  結論: {c3}")
    print(f"  原子文: {sorted(inf3.get_all_atoms())}")
    print(f"  意味論的に妥当: {inf3.is_semantically_valid()}")
    print("  真偽値表:")
    inf3.print_truth_table()
    print()
    
    # 4. 選言三段論法 (妥当)
    print("4. 選言三段論法 (P∨Q, ~P ⊢ Q):")
    p6 = Formula("P∨Q")
    p7 = Formula("~P")
    c4 = Formula("Q")
    inf4 = Inference([p6, p7], c4)
    
    print(f"  前提: {p6}, {p7}")
    print(f"  結論: {c4}")
    print(f"  意味論的に妥当: {inf4.is_semantically_valid()}")
    print()
    
    # 5. De Morgan の法則
    print("5. De Morgan の法則 (~(P∧Q) ⊢ ~P∨~Q):")
    p8 = Formula("~(P∧Q)")
    c5 = Formula("~P∨~Q")
    inf5 = Inference([p8], c5)
    
    print(f"  前提: {p8}")
    print(f"  結論: {c5}")
    print(f"  意味論的に妥当: {inf5.is_semantically_valid()}")
    print()
    
    # 6. 非公式な記号文を使った推論
    print("6. 非公式な記号文を使った推論 (P∧Q, P∧Q→R ⊢ R):")
    p9 = Formula("P∧Q")
    p10 = Formula("P∧Q→R")
    c6 = Formula("R")
    inf6 = Inference([p9, p10], c6)
    
    print(f"  前提: {p9}, {p10}")
    print(f"  結論: {c6}")
    print(f"  意味論的に妥当: {inf6.is_semantically_valid()}")
    print("  真偽値表:")
    inf6.print_truth_table()
    print()

def demo_complex_example():
    """より複雑な例"""
    print("=" * 60)
    print("複雑な推論の例")
    print("=" * 60)
    print()
    
    # 複雑な推論: [(P→Q)∧(R→S), P∨R, ~Q] ⊢ S
    print("推論: [(P→Q)∧(R→S), P∨R, ~Q] ⊢ S")
    p1 = Formula("(P→Q)∧(R→S)")
    p2 = Formula("P∨R")
    p3 = Formula("~Q")
    c = Formula("S")
    inf = Inference([p1, p2, p3], c)
    
    print(f"  前提1: {p1}")
    print(f"  前提2: {p2}")
    print(f"  前提3: {p3}")
    print(f"  結論: {c}")
    print(f"  原子文: {sorted(inf.get_all_atoms())}")
    print(f"  意味論的に妥当: {inf.is_semantically_valid()}")
    print()
    print("  真偽値表:")
    inf.print_truth_table()
    print()

if __name__ == "__main__":
    demo_formula()
    print()
    demo_inference()
    print()
    demo_complex_example()
