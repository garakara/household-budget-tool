import pandas as pd
from pathlib import Path

class DataLoader:
    def __init__(self, csv_path=None):
        """
        Args:
            csv_path: CSVファイルのパス(Noneの場合はデフォルト)
        """
        if csv_path is None:
            # このファイルの場所から相対パスで data/sample.csv を探す
            project_root = Path(__file__).parent.parent
            csv_path = project_root / "data" / "sample.csv"
        else:
            csv_path = Path(csv_path)
        
        self.csv_path = csv_path
        self.df = None
        
        # デバッグ情報
        print(f"📁 CSVパス: {self.csv_path}")
        print(f"📂 プロジェクトルート: {self.csv_path.parent.parent}")
        
    def load_data(self):
        """CSVデータを読み込む"""
        # ファイル存在チェック
        if not self.csv_path.exists():
            print(f"\n❌ エラー: ファイルが見つかりません")
            print(f"探したパス: {self.csv_path.absolute()}")
            print(f"\n現在のディレクトリ構造:")
            
            # data フォルダの中身を表示
            data_dir = self.csv_path.parent
            if data_dir.exists():
                print(f"  {data_dir}/ には以下のファイルがあります:")
                for file in data_dir.iterdir():
                    print(f"    - {file.name}")
            else:
                print(f"  {data_dir}/ が存在しません")
            
            raise FileNotFoundError(f"CSVファイルが見つかりません: {self.csv_path}")
        
        # データ読み込み
        self.df = pd.read_csv(self.csv_path, parse_dates=['日付'])
        print(f"✓ {len(self.df)}件のデータを読み込みました\n")
        return self.df
    
    def get_summary(self):
        """基本統計を表示"""
        if self.df is None:
            raise ValueError("データが読み込まれていません。load_data()を先に実行してください")
        
        print("=== 基本統計 ===")
        print(f"総支出: ¥{self.df['金額'].sum():,}")
        print(f"平均支出: ¥{self.df['金額'].mean():,.0f}")
        print(f"記録日数: {self.df['日付'].nunique()}日")
        
        print("\n=== カテゴリ別支出 ===")
        category_sum = self.df.groupby('カテゴリ')['金額'].sum().sort_values(ascending=False)
        for cat, amount in category_sum.items():
            print(f"{cat}: ¥{amount:,}")
        
        return category_sum

# テスト用
if __name__ == "__main__":
    print("=== DataLoader テスト ===\n")
    
    loader = DataLoader()
    df = loader.load_data()
    loader.get_summary()