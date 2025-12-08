import pandas as pd
from datetime import datetime
import config
class Analyzer:
    def __init__(self, df):
        self.df = df
    
    def analyze_necessity(self):
        """必需品 vs 浪費の分析"""
        necessity_sum = self.df.groupby('必需品フラグ')['金額'].sum()
        
        print("\n=== 必需品 vs 浪費 ===")
        if 1 in necessity_sum.index:
            print(f"必需品: ¥{necessity_sum[1]:,}")
        if 0 in necessity_sum.index:
            print(f"浪費:   ¥{necessity_sum[0]:,}")
        
        # 割合計算
        total = self.df['金額'].sum()
        if 0 in necessity_sum.index:
            waste_rate = necessity_sum[0] / total * 100
            print(f"\n浪費率: {waste_rate:.1f}%")
            
            if waste_rate > 30:
                print("⚠️  警告: 浪費が30%を超えています!")
        
        return necessity_sum
    
    def analyze_rating(self):
        """5段階評価の分析"""
        rating_summary = self.df.groupby('評価').agg({
            '金額': ['sum', 'count', 'mean']
        }).round(0)
        
        print("\n=== 買い物評価別 ===")
        print(rating_summary)
        
        # 低評価(1-2)の買い物を警告
        low_rating = self.df[self.df['評価'] <= 2]
        if len(low_rating) > 0:
            print(f"\n⚠️  低評価の買い物が{len(low_rating)}件あります")
            print(f"   合計金額: ¥{low_rating['金額'].sum():,}")
            print("\n【詳細】")
            for _, row in low_rating.iterrows():
                print(f"  - {row['日付'].strftime('%m/%d')} {row['店舗']}: ¥{row['金額']:,} ({row['メモ']})")
                
    
    def check_budget_alert(self):
        """予算警告をチェック"""
        # 今月のデータだけ抽出
        today = datetime.now()
        this_month = self.df[self.df['日付'].dt.month == today.month]
        
        # 経過日数
        days_passed = today.day
        days_in_month = 30  # 簡易版
        
        print("\n" + "=" * 50)
        print("  予算使用状況")
        print("=" * 50)
        
        # 総予算チェック
        total_spending = this_month['金額'].sum()
        total_budget = config.BUDGET["月予算"]
        usage_rate = total_spending / total_budget
        expected_rate = days_passed / days_in_month
        pace = usage_rate / expected_rate if expected_rate > 0 else 0
        
        print(f"\n【総予算】")
        print(f"今月の支出: ¥{total_spending:,} / ¥{total_budget:,}")
        print(f"使用率: {usage_rate*100:.1f}% (経過日数: {days_passed}/{days_in_month}日)")
        print(f"ペース: {pace:.2f}倍")
        
        if pace >= 1.5:
            print("🚨 危険! 通常ペースの1.5倍以上です!")
        elif pace >= 1.2:
            print("⚠️  警告: 通常ペースの1.2倍以上です")
        elif pace >= 1.0:
            print("⚡ 注意: やや使いすぎています")
        else:
            print("✅ 順調です!")
        
        # カテゴリ別チェック
        print(f"\n【カテゴリ別】")
        category_spending = this_month.groupby('カテゴリ')['金額'].sum()
        
        for category, budget in config.BUDGET["カテゴリ別"].items():
            spending = category_spending.get(category, 0)
            usage = spending / budget
            
            status = ""
            if usage >= 0.95:
                status = "🚨"
            elif usage >= 0.85:
                status = "⚠️ "
            elif usage >= 0.70:
                status = "⚡"
            else:
                status = "✅"
            
            print(f"{status} {category:8s}: ¥{spending:6,} / ¥{budget:6,} ({usage*100:5.1f}%)")