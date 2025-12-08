"""
追加のエッジケーステスト
"""
import sys
sys.path.insert(0, '/home/runner/work/turnstile/turnstile')

from main import Formula, Inference

def test_formula_with_subscripts():
    """下付き添字を含む原子文のテスト"""
    print("=== 下付き添字を含む原子文のテスト ===")
    
    # テストケース1: 単純な下付き添字
    f1 = Formula("P_1")
    assert f1.is_well_formed, "P_1 は整形式であるべき"
    assert f1.get_atoms() == {"P_1"}, "原子文は P_1"
    print("✓ テスト1: 下付き添字 'P_1' - 成功")
    
    # テストケース2: 複数の下付き添字を含む式
    f2 = Formula("P_1∧Q_2")
    assert f2.is_well_formed, "P_1∧Q_2 は整形式であるべき"
    assert f2.get_atoms() == {"P_1", "Q_2"}, "原子文は P_1 と Q_2"
    print("✓ テスト2: 複数の下付き添字 'P_1∧Q_2' - 成功")
    
    # テストケース3: 下付き添字を含む複雑な式
    f3 = Formula("(P_1→Q_2)∧(R_3∨S_4)")
    assert f3.is_well_formed, "複雑な式は整形式であるべき"
    assert f3.get_atoms() == {"P_1", "Q_2", "R_3", "S_4"}, "原子文は P_1, Q_2, R_3, S_4"
    print("✓ テスト3: 下付き添字を含む複雑な式 - 成功")
    
    print()

def test_formula_with_whitespace():
    """空白を含む記号文のテスト"""
    print("=== 空白を含む記号文のテスト ===")
    
    # テストケース1: 空白を含む式
    f1 = Formula("P ∧ Q")
    assert f1.is_well_formed, "空白を含む式は整形式であるべき"
    assert f1.get_atoms() == {"P", "Q"}, "原子文は P と Q"
    print("✓ テスト1: 空白を含む式 'P ∧ Q' - 成功")
    
    # テストケース2: タブを含む式
    f2 = Formula("P\t∧\tQ")
    assert f2.is_well_formed, "タブを含む式は整形式であるべき"
    assert f2.get_atoms() == {"P", "Q"}, "原子文は P と Q"
    print("✓ テスト2: タブを含む式 - 成功")
    
    # テストケース3: 複数の空白を含む式
    f3 = Formula("(  P  →  Q  )")
    assert f3.is_well_formed, "複数の空白を含む式は整形式であるべき"
    assert f3.is_formal, "括弧があるので公式であるべき"
    print("✓ テスト3: 複数の空白を含む式 - 成功")
    
    print()

def test_formula_alternative_symbols():
    """代替記号のテスト"""
    print("=== 代替記号のテスト ===")
    
    # テストケース1: 否定の代替記号
    symbols_not = ["!P", "~P", "～P"]
    for s in symbols_not:
        f = Formula(s)
        assert f.is_well_formed, f"{s} は整形式であるべき"
        print(f"✓ 否定 '{s}' - 成功")
    
    # テストケース2: 連言の代替記号
    symbols_and = ["P&Q", "P∧Q", "P/\\Q"]
    for s in symbols_and:
        f = Formula(s)
        assert f.is_well_formed, f"{s} は整形式であるべき"
        print(f"✓ 連言 '{s}' - 成功")
    
    # テストケース3: 選言の代替記号
    symbols_or = ["P|Q", "P∨Q", "P\\/Q"]
    for s in symbols_or:
        f = Formula(s)
        assert f.is_well_formed, f"{s} は整形式であるべき"
        print(f"✓ 選言 '{s}' - 成功")
    
    # テストケース4: 含意の代替記号
    symbols_implies = ["P->Q", "P→Q", "P=>Q"]
    for s in symbols_implies:
        f = Formula(s)
        assert f.is_well_formed, f"{s} は整形式であるべき"
        print(f"✓ 含意 '{s}' - 成功")
    
    # テストケース5: 同値の代替記号
    symbols_equiv = ["P<->Q", "P↔Q", "P<=>Q"]
    for s in symbols_equiv:
        f = Formula(s)
        assert f.is_well_formed, f"{s} は整形式であるべき"
        print(f"✓ 同値 '{s}' - 成功")
    
    print()

def test_inference_edge_cases():
    """推論のエッジケースのテスト"""
    print("=== 推論のエッジケースのテスト ===")
    
    # テストケース1: 前提が1つの場合
    p1 = Formula("P→Q")
    c1 = Formula("P→Q")
    inf1 = Inference([p1], c1)
    assert inf1.is_semantically_valid(), "P→Q ⊢ P→Q は妥当(恒真式)"
    print("✓ テスト1: 前提が1つ - 成功")
    
    # テストケース2: トートロジー
    p2 = Formula("P∨~P")
    c2 = Formula("Q→Q")
    inf2 = Inference([p2], c2)
    assert inf2.is_semantically_valid(), "トートロジーから何でも導ける"
    print("✓ テスト2: トートロジー - 成功")
    
    # テストケース3: 矛盾から何でも導ける (ex falso quodlibet)
    p3 = Formula("P∧~P")
    c3 = Formula("Q")
    inf3 = Inference([p3], c3)
    # 前提が矛盾なので、全ての行で前提が偽となり、意味論的に妥当
    assert inf3.is_semantically_valid(), "矛盾から何でも導ける"
    print("✓ テスト3: 矛盾から何でも導ける - 成功")
    
    # テストケース4: 原子文が多い場合 (4つ)
    p4 = Formula("P→Q")
    p5 = Formula("Q→R")
    p6 = Formula("R→S")
    c4 = Formula("P→S")
    inf4 = Inference([p4, p5, p6], c4)
    assert inf4.is_semantically_valid(), "連鎖的な含意は妥当"
    assert len(inf4.tf_table) == 16, "2^4 = 16 行の真偽値表"
    print("✓ テスト4: 原子文が4つ - 成功")
    
    # テストケース5: 同じ前提が複数回出現
    p7 = Formula("P")
    p8 = Formula("P")
    c5 = Formula("P")
    inf5 = Inference([p7, p8], c5)
    assert inf5.is_semantically_valid(), "P, P ⊢ P は妥当"
    print("✓ テスト5: 同じ前提が複数回 - 成功")
    
    print()

def test_double_negation():
    """二重否定のテスト"""
    print("=== 二重否定のテスト ===")
    
    # テストケース1: 二重否定の除去
    p1 = Formula("~~P")
    c1 = Formula("P")
    inf1 = Inference([p1], c1)
    assert inf1.is_semantically_valid(), "~~P ⊢ P は妥当"
    print("✓ テスト1: 二重否定の除去 - 成功")
    
    # テストケース2: 二重否定の導入
    p2 = Formula("P")
    c2 = Formula("~~P")
    inf2 = Inference([p2], c2)
    assert inf2.is_semantically_valid(), "P ⊢ ~~P は妥当"
    print("✓ テスト2: 二重否定の導入 - 成功")
    
    # テストケース3: 三重否定
    p3 = Formula("~~~P")
    c3 = Formula("~P")
    inf3 = Inference([p3], c3)
    assert inf3.is_semantically_valid(), "~~~P ⊢ ~P は妥当"
    print("✓ テスト3: 三重否定 - 成功")
    
    print()

def test_de_morgan_laws():
    """De Morgan の法則の完全なテスト"""
    print("=== De Morgan の法則の完全なテスト ===")
    
    # 法則1: ~(P∧Q) ⊢ ~P∨~Q
    p1 = Formula("~(P∧Q)")
    c1 = Formula("~P∨~Q")
    inf1 = Inference([p1], c1)
    assert inf1.is_semantically_valid(), "~(P∧Q) ⊢ ~P∨~Q は妥当"
    print("✓ 法則1: ~(P∧Q) ⊢ ~P∨~Q - 成功")
    
    # 法則2: ~P∨~Q ⊢ ~(P∧Q)
    p2 = Formula("~P∨~Q")
    c2 = Formula("~(P∧Q)")
    inf2 = Inference([p2], c2)
    assert inf2.is_semantically_valid(), "~P∨~Q ⊢ ~(P∧Q) は妥当"
    print("✓ 法則2: ~P∨~Q ⊢ ~(P∧Q) - 成功")
    
    # 法則3: ~(P∨Q) ⊢ ~P∧~Q
    p3 = Formula("~(P∨Q)")
    c3 = Formula("~P∧~Q")
    inf3 = Inference([p3], c3)
    assert inf3.is_semantically_valid(), "~(P∨Q) ⊢ ~P∧~Q は妥当"
    print("✓ 法則3: ~(P∨Q) ⊢ ~P∧~Q - 成功")
    
    # 法則4: ~P∧~Q ⊢ ~(P∨Q)
    p4 = Formula("~P∧~Q")
    c4 = Formula("~(P∨Q)")
    inf4 = Inference([p4], c4)
    assert inf4.is_semantically_valid(), "~P∧~Q ⊢ ~(P∨Q) は妥当"
    print("✓ 法則4: ~P∧~Q ⊢ ~(P∨Q) - 成功")
    
    print()

def test_complex_nested_formulas():
    """複雑にネストされた記号文のテスト"""
    print("=== 複雑にネストされた記号文のテスト ===")
    
    # テストケース1: 深くネストされた式
    f1 = Formula("((P→Q)→((Q→R)→(P→R)))")
    assert f1.is_well_formed, "深くネストされた式は整形式であるべき"
    assert f1.is_formal, "完全に括弧が付いているので公式"
    print("✓ テスト1: 深くネストされた式 - 成功")
    
    # テストケース2: 複雑な論理式
    f2 = Formula("((P∧Q)→R)↔((P→R)∨(Q→R))")
    assert f2.is_well_formed, "複雑な論理式は整形式であるべき"
    print("✓ テスト2: 複雑な論理式 - 成功")
    
    # テストケース3: 非公式でネストされた式
    f3 = Formula("P∧Q∧R→S∨T")
    assert f3.is_well_formed, "非公式でネストされた式は整形式であるべき"
    assert not f3.is_formal, "非公式な記号文"
    print("✓ テスト3: 非公式でネストされた式 - 成功")
    
    print()

def run_edge_case_tests():
    """全てのエッジケーステストを実行"""
    print("=" * 60)
    print("エッジケーステストを開始します")
    print("=" * 60)
    print()
    
    test_formula_with_subscripts()
    test_formula_with_whitespace()
    test_formula_alternative_symbols()
    test_inference_edge_cases()
    test_double_negation()
    test_de_morgan_laws()
    test_complex_nested_formulas()
    
    print("=" * 60)
    print("全てのエッジケーステストが成功しました！")
    print("=" * 60)

if __name__ == "__main__":
    run_edge_case_tests()
