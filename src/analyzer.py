def check_budget_alert(current_spending, budget, days_passed, days_in_month):
    """
    予算使用状況をチェック
    
    Args:
        current_spending: 今月の支出合計
        budget: 月予算
        days_passed: 経過日数
        days_in_month: 月の日数
    
    Returns:
        alert_level: None, "注意", "警告", "危険"
    """
    # 使用割合
    usage_rate = current_spending / budget
    
    # 期待使用割合(日割り)
    expected_rate = days_passed / days_in_month
    
    # ペース
    pace = usage_rate / expected_rate if expected_rate > 0 else 0
    
    if pace >= 1.5:  # 1.5倍のペース
        return "危険", f"予算の{usage_rate*100:.1f}%を使用中(通常ペースの{pace:.1f}倍)"
    elif pace >= 1.2:
        return "警告", f"予算の{usage_rate*100:.1f}%を使用中(通常ペースの{pace:.1f}倍)"
    elif pace >= 1.0:
        return "注意", f"予算の{usage_rate*100:.1f}%を使用中"
    else:
        return None, f"順調です(予算の{usage_rate*100:.1f}%)"