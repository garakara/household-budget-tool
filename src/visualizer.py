import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 日本語フォント設定
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'DejaVu Sans']

class Visualizer:
    def __init__(self, df):
        self.df = df
    
    def plot_category_pie(self, save_path="outputs/graphs/category_pie.png"):
        """カテゴリ別円グラフ"""
        category_sum = self.df.groupby('カテゴリ')['金額'].sum()
        
        plt.figure(figsize=(10, 6))
        plt.pie(category_sum.values, labels=category_sum.index, autopct='%1.1f%%')
        plt.title('カテゴリ別支出割合', fontsize=16)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ グラフを保存: {save_path}")
    
    def plot_daily_spending(self, save_path="outputs/graphs/daily_spending.png"):
        """日別支出グラフ"""
        daily_sum = self.df.groupby('日付')['金額'].sum()
        
        plt.figure(figsize=(12, 6))
        plt.bar(daily_sum.index, daily_sum.values)
        plt.xlabel('日付', fontsize=12)
        plt.ylabel('支出金額 (円)', fontsize=12)
        plt.title('日別支出', fontsize=16)
        plt.xticks(rotation=45)
        plt.grid(axis='y', alpha=0.3)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ グラフを保存: {save_path}")



    def plot_necessity_comparison(self, save_path="outputs/graphs/necessity.png"):
        """必需品 vs 浪費の比較"""
        necessity_sum = self.df.groupby('必需品フラグ')['金額'].sum()
        
        labels = ['浪費', '必需品']
        colors = ['#FF6B6B', '#4ECDC4']
        
        plt.figure(figsize=(8, 6))
        plt.pie(necessity_sum.values, labels=labels, colors=colors, 
                autopct='%1.1f%%', startangle=90)
        plt.title('必需品 vs 浪費', fontsize=16)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ グラフを保存: {save_path}")

    def plot_rating_distribution(self, save_path="outputs/graphs/rating.png"):
        """評価別の支出分布"""
        rating_sum = self.df.groupby('評価')['金額'].sum()
        
        plt.figure(figsize=(10, 6))
        colors = ['#FF6B6B', '#FFA07A', '#FFD93D', '#6BCF7F', '#4ECDC4']
        plt.bar(rating_sum.index, rating_sum.values, color=colors)
        plt.xlabel('評価', fontsize=12)
        plt.ylabel('支出金額 (円)', fontsize=12)
        plt.title('買い物評価別支出', fontsize=16)
        plt.xticks([1, 2, 3, 4, 5])
        plt.grid(axis='y', alpha=0.3)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ グラフを保存: {save_path}")
    
# テスト
if __name__ == "__main__":
    from data_loader import DataLoader
    
    loader = DataLoader()
    df = loader.load_data()
    
    viz = Visualizer(df)
    viz.plot_category_pie()
    viz.plot_daily_spending()