from pathlib import Path
from src.data_loader import DataLoader
from src.visualizer import Visualizer

def main():
    print("=" * 50)
    print("  家計簿分析ツール")
    print("=" * 50)
    print()
    
    try:
        # データ読み込み(デフォルトパス使用)
        loader = DataLoader()
        df = loader.load_data()
        
        # 基本統計
        loader.get_summary()
        
        # グラフ作成
        print("\n=== グラフ作成中 ===")
        viz = Visualizer(df)
        viz.plot_category_pie()
        viz.plot_daily_spending()
        
        print("\n" + "=" * 50)
        print("✓ 完了!")
        print("=" * 50)
        print("outputs/graphs/ にグラフが保存されました")
        
    except FileNotFoundError as e:
        print(f"\n❌ エラー: {e}")
        print("\n対処方法:")
        print("1. data/sample.csv が存在するか確認してください")
        print("2. プロジェクトルート(household-budget-tool/)で実行してください")
        print("   コマンド: python main.py")
    except Exception as e:
        print(f"\n❌ 予期しないエラー: {e}")

if __name__ == "__main__":
    main()