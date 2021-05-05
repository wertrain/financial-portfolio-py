import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import datetime

def strip_unit_of_money(str):
    str = str.replace(',', '')
    str = str.replace('USD', '')
    str = str.replace('円', '')
    return str.strip()

def make_data_frame_from_file(file_name):
    f = open(file_name, 'r', encoding='UTF-8')
    datalist = f.readlines()

    brands = []
    ticker_symbols = []
    markets = []
    prices_yen = []
    prices_usd = []
    stocks = []
    acq_prices_yen = []
    acq_prices_usd = []
    amounts_yen = []
    amounts_usd = []
    evaluation_values_usd = []
    evaluation_values_yen = []
    profits_yen= []
    profits_usd = []

    index = 9 # 表題を飛ばした開始インデックス
    offset = 18 # 一つの銘柄の行数

    while (len(datalist) > index + offset):
        base_index = index
        brands.append(datalist[base_index + 0].strip())
        ticker_and_market = datalist[base_index + 1].strip().split(' ')
        ticker_symbols.append(ticker_and_market[0]) 
        markets.append(ticker_and_market[1])

        # 途中から空行がなくなってしまったので両方対応できるように判定しておく
        has_empty_line = 0
        if (len(datalist[base_index + 2]) > 0):
            has_empty_line = 1
        # 空行がない場合は 1 行少なくする必要がある
        new_index = base_index - has_empty_line
        
        prices_yen.append(strip_unit_of_money(datalist[new_index + 3]))
        prices_usd.append(strip_unit_of_money(datalist[new_index + 4]))
        stocks.append(datalist[new_index + 5].strip())
        acq_prices_usd.append(strip_unit_of_money(datalist[new_index + 7]))
        acq_prices_yen.append(strip_unit_of_money(datalist[new_index + 8]))
        amounts_usd.append(strip_unit_of_money(datalist[new_index + 9]))
        amounts_yen.append(strip_unit_of_money(datalist[new_index + 10]))
        evaluation_values_usd.append(strip_unit_of_money(datalist[new_index + 11]))
        evaluation_values_yen.append(strip_unit_of_money(datalist[new_index + 12]))
        profits_usd.append(strip_unit_of_money(datalist[new_index + 13]))
        profits_yen.append(strip_unit_of_money(datalist[new_index + 14]))
        index = index + offset - has_empty_line

    return pd.DataFrame({
        '銘柄' : brands,
        'ティッカー' : ticker_symbols,
        '市場' : markets,
        '現在値 (USD)' : list(map(float, prices_usd)),
        '現在値 (YEN)' : list(map(float, prices_yen)),
        '保有数量' : list(map(int, stocks)),
        '取得単価 (USD)' : list(map(float, acq_prices_usd)),
        '取得単価 (YEN)' : list(map(float, acq_prices_yen)),
        '取得金額 (USD)' : list(map(float, amounts_usd)),
        '取得金額 (YEN)' : list(map(float, amounts_yen)),
        '評価額 (USD)' : list(map(float, evaluation_values_usd)),
        '評価額 (YEN)' : list(map(float, evaluation_values_yen)),
        '評価損益 (USD)' : list(map(float, profits_usd)),
        '評価損益 (YEN)' : list(map(float, profits_yen)),
    })

def sbi_text_to_pie_chart(file_name):
    df = make_data_frame_from_file(file_name)

    font_name = '07LightNovelPOP'
    font_name = 'BIZ UDGothic'

    fig, ax = plt.subplots(num=None, figsize=(18, 14), dpi=80, facecolor='w', edgecolor='k')
    fig.canvas.set_window_title(datetime.datetime.now().isoformat())
    plt.rcParams["figure.figsize"] = (100, 1100)
    plt.rcParams['font.family'] = font_name
    plt.rcParams['font.size'] = 10
    ax.pie(df['評価額 (YEN)'], labels=df['銘柄'], autopct='%1.1f %%')
    plt.legend(df['銘柄'], fontsize=8, bbox_to_anchor=(0.9, 0.3), prop={'family':font_name})
    plt.show()

def sbi_text_to_df(file_name):
    df = make_data_frame_from_file(file_name)
    print (df)

if __name__ == '__main__':
    file = 'sample.txt'
    if (len(sys.argv) > 1):
        file = sys.argv[1];
    sbi_text_to_pie_chart(file)