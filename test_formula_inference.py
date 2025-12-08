"""
Formula と Inference クラスのテスト
"""
import sys
sys.path.insert(0, '/home/runner/work/turnstile/turnstile')

from main import Formula, Inference

def test_formula_formal():
    """公式な記号文のテスト"""
    print("=== 公式な記号文のテスト ===")
    
    # テストケース1: 単純な原子文
    f1 = Formula("P")
    assert f1.is_well_formed, "P は整形式であるべき"
    assert f1.is_formal, "P は公式な記号文であるべき"
    assert f1.get_atoms() == {"P"}, "原子文は P のみ"
    print("✓ テスト1: 原子文 'P' - 成功")
    
    # テストケース2: 否定
    f2 = Formula("~P")
    assert f2.is_well_formed, "~P は整形式であるべき"
    assert f2.is_formal, "~P は公式な記号文であるべき"
    assert f2.get_atoms() == {"P"}, "原子文は P のみ"
    print("✓ テスト2: 否定 '~P' - 成功")
    
    # テストケース3: 連言(公式)
    f3 = Formula("(P∧Q)")
    assert f3.is_well_formed, "(P∧Q) は整形式であるべき"
    assert f3.is_formal, "(P∧Q) は公式な記号文であるべき"
    assert f3.get_atoms() == {"P", "Q"}, "原子文は P と Q"
    print("✓ テスト3: 連言 '(P∧Q)' - 成功")
    
    # テストケース4: 選言(公式)
    f4 = Formula("(P∨Q)")
    assert f4.is_well_formed, "(P∨Q) は整形式であるべき"
    assert f4.is_formal, "(P∨Q) は公式な記号文であるべき"
    print("✓ テスト4: 選言 '(P∨Q)' - 成功")
    
    # テストケース5: 含意(公式)
    f5 = Formula("(P→Q)")
    assert f5.is_well_formed, "(P→Q) は整形式であるべき"
    assert f5.is_formal, "(P→Q) は公式な記号文であるべき"
    print("✓ テスト5: 含意 '(P→Q)' - 成功")
    
    # テストケース6: 同値(公式)
    f6 = Formula("(P↔Q)")
    assert f6.is_well_formed, "(P↔Q) は整形式であるべき"
    assert f6.is_formal, "(P↔Q) は公式な記号文であるべき"
    print("✓ テスト6: 同値 '(P↔Q)' - 成功")
    
    # テストケース7: 複雑な式(公式)
    f7 = Formula("((P∧Q)→R)")
    assert f7.is_well_formed, "((P∧Q)→R) は整形式であるべき"
    assert f7.is_formal, "((P∧Q)→R) は公式な記号文であるべき"
    assert f7.get_atoms() == {"P", "Q", "R"}, "原子文は P, Q, R"
    print("✓ テスト7: 複雑な式 '((P∧Q)→R)' - 成功")
    
    print()

def test_formula_informal():
    """非公式な記号文のテスト"""
    print("=== 非公式な記号文のテスト ===")
    
    # テストケース1: 最外括弧の省略
    f1 = Formula("P∧Q")
    assert f1.is_well_formed, "P∧Q は整形式であるべき"
    assert not f1.is_formal, "P∧Q は非公式な記号文であるべき"
    assert f1.get_atoms() == {"P", "Q"}, "原子文は P と Q"
    print("✓ テスト1: 最外括弧省略 'P∧Q' - 成功")
    
    # テストケース2: 角括弧の使用
    f2 = Formula("[P∧Q]")
    assert f2.is_well_formed, "[P∧Q] は整形式であるべき"
    assert not f2.is_formal, "[P∧Q] は非公式な記号文であるべき"
    print("✓ テスト2: 角括弧 '[P∧Q]' - 成功")
    
    # テストケース3: 優先順位による括弧省略 (∧ > →)
    f3 = Formula("P∧Q→R")
    assert f3.is_well_formed, "P∧Q→R は整形式であるべき"
    assert not f3.is_formal, "P∧Q→R は非公式な記号文であるべき"
    assert f3.get_atoms() == {"P", "Q", "R"}, "原子文は P, Q, R"
    print("✓ テスト3: 優先順位 'P∧Q→R' - 成功")
    
    # テストケース4: 左寄せの規則 (連言)
    f4 = Formula("P∧Q∧R")
    assert f4.is_well_formed, "P∧Q∧R は整形式であるべき"
    assert not f4.is_formal, "P∧Q∧R は非公式な記号文であるべき"
    print("✓ テスト4: 左寄せ連言 'P∧Q∧R' - 成功")
    
    # テストケース5: 左寄せの規則 (選言)
    f5 = Formula("P∨Q∨R")
    assert f5.is_well_formed, "P∨Q∨R は整形式であるべき"
    assert not f5.is_formal, "P∨Q∨R は非公式な記号文であるべき"
    print("✓ テスト5: 左寄せ選言 'P∨Q∨R' - 成功")
    
    # テストケース6: 別の記号の使用
    f6 = Formula("P&Q")  # & は ∧ の代替表記
    assert f6.is_well_formed, "P&Q は整形式であるべき"
    print("✓ テスト6: 代替記号 'P&Q' - 成功")
    
    print()

def test_formula_invalid():
    """無効な記号列のテスト"""
    print("=== 無効な記号列のテスト ===")
    
    # テストケース1: 空文字列
    try:
        f1 = Formula("")
        assert False, "空文字列はエラーになるべき"
    except ValueError as e:
        print(f"✓ テスト1: 空文字列 - 正しくエラー: {e}")
    
    # テストケース2: 未知のトークン
    try:
        f2 = Formula("P#Q")
        assert False, "未知のトークンはエラーになるべき"
    except ValueError as e:
        print(f"✓ テスト2: 未知のトークン 'P#Q' - 正しくエラー: {e}")
    
    # テストケース3: ∧と∨の混在(括弧なし)
    try:
        f3 = Formula("P∧Q∨R")
        assert False, "∧と∨の混在(括弧なし)はエラーになるべき"
    except ValueError as e:
        print(f"✓ テスト3: ∧と∨の混在 'P∧Q∨R' - 正しくエラー: {e}")
    
    # テストケース4: 括弧の不一致
    try:
        f4 = Formula("(P∧Q")
        assert False, "括弧の不一致はエラーになるべき"
    except ValueError as e:
        print(f"✓ テスト4: 括弧不一致 '(P∧Q' - 正しくエラー: {e}")
    
    print()

def test_formula_evaluation():
    """記号文の評価のテスト"""
    print("=== 記号文の評価のテスト ===")
    
    # テストケース1: 単純な原子文
    f1 = Formula("P")
    assert f1.evaluate({"P": True}) == True, "P が True なら True"
    assert f1.evaluate({"P": False}) == False, "P が False なら False"
    print("✓ テスト1: 原子文の評価 - 成功")
    
    # テストケース2: 否定
    f2 = Formula("~P")
    assert f2.evaluate({"P": True}) == False, "~P が True なら False"
    assert f2.evaluate({"P": False}) == True, "~P が False なら True"
    print("✓ テスト2: 否定の評価 - 成功")
    
    # テストケース3: 連言
    f3 = Formula("P∧Q")
    assert f3.evaluate({"P": True, "Q": True}) == True
    assert f3.evaluate({"P": True, "Q": False}) == False
    assert f3.evaluate({"P": False, "Q": True}) == False
    assert f3.evaluate({"P": False, "Q": False}) == False
    print("✓ テスト3: 連言の評価 - 成功")
    
    # テストケース4: 選言
    f4 = Formula("P∨Q")
    assert f4.evaluate({"P": True, "Q": True}) == True
    assert f4.evaluate({"P": True, "Q": False}) == True
    assert f4.evaluate({"P": False, "Q": True}) == True
    assert f4.evaluate({"P": False, "Q": False}) == False
    print("✓ テスト4: 選言の評価 - 成功")
    
    # テストケース5: 含意
    f5 = Formula("P→Q")
    assert f5.evaluate({"P": True, "Q": True}) == True
    assert f5.evaluate({"P": True, "Q": False}) == False
    assert f5.evaluate({"P": False, "Q": True}) == True
    assert f5.evaluate({"P": False, "Q": False}) == True
    print("✓ テスト5: 含意の評価 - 成功")
    
    print()

def test_inference_simple():
    """単純な推論のテスト"""
    print("=== 単純な推論のテスト ===")
    
    # テストケース1: Modus Ponens (妥当)
    # P, P→Q ⊢ Q
    p1 = Formula("P")
    p2 = Formula("P→Q")
    c1 = Formula("Q")
    inf1 = Inference([p1, p2], c1)
    
    assert inf1.get_all_atoms() == {"P", "Q"}, "原子文は P と Q"
    table1 = inf1.generate_truth_table()
    assert len(table1) == 4, "2^2 = 4 行の真偽値表"
    assert inf1.is_semantically_valid(), "Modus Ponens は妥当"
    print("✓ テスト1: Modus Ponens - 妥当")
    
    # テストケース2: 妥当でない推論
    # P ⊢ Q
    p3 = Formula("P")
    c2 = Formula("Q")
    inf2 = Inference([p3], c2)
    
    assert not inf2.is_semantically_valid(), "P ⊢ Q は妥当でない"
    counterexample = inf2.get_counterexample()
    assert counterexample is not None, "反例が存在する"
    assert counterexample["P"] == True and counterexample["Q"] == False, "P=T, Q=F が反例"
    print("✓ テスト2: 妥当でない推論 - 正しく判定")
    
    print()

def test_inference_complex():
    """複雑な推論のテスト"""
    print("=== 複雑な推論のテスト ===")
    
    # テストケース1: 三段論法 (妥当)
    # P→Q, Q→R ⊢ P→R
    p1 = Formula("P→Q")
    p2 = Formula("Q→R")
    c1 = Formula("P→R")
    inf1 = Inference([p1, p2], c1)
    
    assert inf1.get_all_atoms() == {"P", "Q", "R"}, "原子文は P, Q, R"
    table1 = inf1.generate_truth_table()
    assert len(table1) == 8, "2^3 = 8 行の真偽値表"
    assert inf1.is_semantically_valid(), "三段論法は妥当"
    print("✓ テスト1: 三段論法 - 妥当")
    
    # テストケース2: 選言三段論法 (妥当)
    # P∨Q, ~P ⊢ Q
    p3 = Formula("P∨Q")
    p4 = Formula("~P")
    c2 = Formula("Q")
    inf2 = Inference([p3, p4], c2)
    
    assert inf2.is_semantically_valid(), "選言三段論法は妥当"
    print("✓ テスト2: 選言三段論法 - 妥当")
    
    # テストケース3: De Morgan の法則 (妥当)
    # ~(P∧Q) ⊢ ~P∨~Q
    p5 = Formula("~(P∧Q)")
    c3 = Formula("~P∨~Q")
    inf3 = Inference([p5], c3)
    
    assert inf3.is_semantically_valid(), "De Morgan の法則は妥当"
    print("✓ テスト3: De Morgan の法則 - 妥当")
    
    print()

def test_inference_with_informal():
    """非公式な記号文を含む推論のテスト"""
    print("=== 非公式な記号文を含む推論のテスト ===")
    
    # 非公式な記号文でも正しく動作することを確認
    # P∧Q, P∧Q→R ⊢ R
    p1 = Formula("P∧Q")  # 非公式(括弧省略)
    p2 = Formula("P∧Q→R")  # 非公式(優先順位)
    c1 = Formula("R")
    inf1 = Inference([p1, p2], c1)
    
    assert inf1.is_semantically_valid(), "非公式な記号文でも推論は妥当"
    print("✓ テスト: 非公式な記号文を含む推論 - 成功")
    
    print()

def test_truth_table_display():
    """真偽値表の表示テスト"""
    print("=== 真偽値表の表示テスト ===")
    
    # P, P→Q ⊢ Q (Modus Ponens)
    p1 = Formula("P")
    p2 = Formula("P→Q")
    c1 = Formula("Q")
    inf1 = Inference([p1, p2], c1)
    
    print("Modus Ponens の真偽値表:")
    inf1.print_truth_table()
    print()
    
    # P→Q, Q→R ⊢ P→R (三段論法)
    p3 = Formula("P→Q")
    p4 = Formula("Q→R")
    c2 = Formula("P→R")
    inf2 = Inference([p3, p4], c2)
    
    print("三段論法の真偽値表:")
    inf2.print_truth_table()
    print()

def run_all_tests():
    """全てのテストを実行"""
    print("=" * 60)
    print("Formula と Inference クラスのテストを開始します")
    print("=" * 60)
    print()
    
    test_formula_formal()
    test_formula_informal()
    test_formula_invalid()
    test_formula_evaluation()
    test_inference_simple()
    test_inference_complex()
    test_inference_with_informal()
    test_truth_table_display()
    
    print("=" * 60)
    print("全てのテストが成功しました！")
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()
