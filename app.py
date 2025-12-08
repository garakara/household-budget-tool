import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# srcモジュールをインポート
sys.path.append(str(Path(__file__).parent))
from src.data_loader import DataLoader
from src.analyzer import Analyzer
from src.visualizer import Visualizer

# ページ設定
st.set_page_config(
    page_title="家計簿分析ツール",
    page_icon="💰",
    layout="wide"
)

# タイトル
st.title("💰 家計簿分析ツール")
st.markdown("---")

# サイドバー
st.sidebar.header("📊 メニュー")
menu = st.sidebar.radio(
    "表示する内容を選択",
    ["📈 ダッシュボード", "📋 データ一覧", "⚙️ 設定"]
)

# データ読み込み
@st.cache_data
def load_data():
    loader = DataLoader()
    df = loader.load_data()
    return df

# ファイルアップロード機能
st.sidebar.header("📂 ファイル")
uploaded_file = st.sidebar.file_uploader("CSVをアップロード", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("ファイルを読み込みました!")

# 日付範囲フィルター
st.sidebar.header("📅 期間")
loader = DataLoader()
df = loader.load_data()
df = loader.load_data()
date_range = st.sidebar.date_input(
    "期間を選択",
    [df['日付'].min(), df['日付'].max()]
)

try:
    df = load_data()
    
    if menu == "📈 ダッシュボード":
        st.header("📈 ダッシュボード")
        
        # 基本統計(3カラム)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("総支出", f"¥{df['金額'].sum():,}")
        
        with col2:
            st.metric("平均支出", f"¥{df['金額'].mean():,.0f}")
        
        with col3:
            st.metric("記録日数", f"{df['日付'].nunique()}日")
        
        st.markdown("---")
        
        # グラフ(2カラム)
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("カテゴリ別支出")
            category_sum = df.groupby('カテゴリ')['金額'].sum()
            
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(category_sum.values, labels=category_sum.index, 
                   autopct='%1.1f%%')
            ax.set_title('カテゴリ別支出割合')
            st.pyplot(fig)
        
        with col2:
            st.subheader("日別支出")
            daily_sum = df.groupby('日付')['金額'].sum()
            
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.bar(daily_sum.index, daily_sum.values)
            ax.set_xlabel('日付')
            ax.set_ylabel('支出金額 (円)')
            ax.set_title('日別支出')
            plt.xticks(rotation=45)
            st.pyplot(fig)
        
        st.markdown("---")
        
        # 分析結果
        st.subheader("📊 分析結果")
        
        analyzer = Analyzer(df)
        
        # 必需品 vs 浪費
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**必需品 vs 浪費**")
            necessity_sum = df.groupby('必需品フラグ')['金額'].sum()
            
            if 1 in necessity_sum.index:
                st.write(f"必需品: ¥{necessity_sum[1]:,}")
            if 0 in necessity_sum.index:
                st.write(f"浪費: ¥{necessity_sum[0]:,}")
                
                total = df['金額'].sum()
                waste_rate = necessity_sum[0] / total * 100
                st.write(f"浪費率: {waste_rate:.1f}%")
                
                if waste_rate > 30:
                    st.warning("⚠️ 浪費が30%を超えています!")
        
        with col2:
            st.write("**評価別支出**")
            rating_summary = df.groupby('評価')['金額'].sum()
            
            for rating, amount in rating_summary.items():
                st.write(f"評価{rating}: ¥{amount:,}")
    
    elif menu == "📋 データ一覧":
        st.header("📋 データ一覧")
        
        # フィルター
        st.sidebar.subheader("フィルター")
        
        categories = ["全て"] + list(df['カテゴリ'].unique())
        selected_category = st.sidebar.selectbox("カテゴリ", categories)
        
        # フィルター適用
        if selected_category != "全て":
            filtered_df = df[df['カテゴリ'] == selected_category]
        else:
            filtered_df = df
        
        st.write(f"表示件数: {len(filtered_df)}件")
        st.dataframe(filtered_df)
        
        # CSV ダウンロード
        csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            "CSVダウンロード",
            csv,
            "filtered_data.csv",
            "text/csv"
        )
    
    elif menu == "⚙️ 設定":
        st.header("⚙️ 設定")
        st.write("設定機能は開発中です...")

    

except FileNotFoundError:
    st.error("❌ data/sample.csv が見つかりません")
    st.info("data/sample.csv を配置してから再度実行してください")
except Exception as e:
    st.error(f"❌ エラーが発生しました: {e}")