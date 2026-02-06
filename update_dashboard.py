import pandas_datareader.data as web
import datetime
import pandas as pd

# 1. FRED 데이터 가져오기
start = datetime.datetime(2020, 1, 1)
end = datetime.datetime.now()

try:
    df = web.DataReader(['T10Y2Y', 'BAMLH0A0HYM2'], 'fred', start, end).dropna()
    
    # 최신 값 추출
    curr_yield = df['T10Y2Y'].iloc[-1]
    curr_spread = df['BAMLH0A0HYM2'].iloc[-1]
    
    # 차트용 데이터 (최근 300일치만, 날짜 포맷 변경)
    recent_df = df.tail(300)
    dates = recent_df.index.strftime('%Y-%m-%d').tolist()
    yields = recent_df['T10Y2Y'].tolist()
    spreads = recent_df['BAMLH0A0HYM2'].tolist()
    
    update_time = end.strftime("%Y-%m-%d %H:%M")

    # 2. HTML 생성 (데이터를 자바스크립트 변수에 직접 주입)
    html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Macro Risk Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            body {{ background-color: #1e1e1e; color: #e0e0e0; font-family: sans-serif; padding: 20px; text-align: center; }}
            .container {{ max-width: 800px; margin: 0 auto; }}
            .card {{ background: #2d2d2d; padding: 20px; margin-bottom: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }}
            h1 {{ color: #bb86fc; margin-bottom: 5px; }}
            h3 {{ margin-top: 0; }}
            .val {{ font-size: 2.5em; font-weight: bold; margin: 10px 0; }}
            .danger {{ color: #cf6679; }} .safe {{ color: #03dac6; }} .warn {{ color: #f29c11; }}
            .desc {{ color: #aaa; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 Macro Risk Dashboard</h1>
            <p class="desc">Last Update: {update_time} (KST)</p>

            <div class="card">
                <h3>1. The Trigger (장단기 금리차)</h3>
                <div class="val {'danger' if curr_yield > 0 else 'safe'}">{curr_yield:.2f}%</div>
                <div class="desc">{'⚠️ 정상화됨 (Recession Risk)' if curr_yield > 0 else '✅ 역전 상태 (방어 중)'}</div>
                <canvas id="yieldChart"></canvas>
            </div>

            <div class="card">
                <h3>2. The Shield (하이일드 스프레드)</h3>
                <div class="val {'danger' if curr_spread > 5.0 else 'safe'}">{curr_spread:.2f}%</div>
                <div class="desc">{'🔥 위험 진입 (방패 균열)' if curr_spread > 5.0 else '🛡️ 안전 구역'}</div>
                <canvas id="spreadChart"></canvas>
            </div>
        </div>

        <script>
            // 파이썬이 주입한 데이터
            const dates = {dates};
            const yields = {yields};
            const spreads = {spreads};

            // 차트 그리기
            new Chart(document.getElementById('yieldChart'), {{
                type: 'line',
                data: {{ labels: dates, datasets: [{{ label: '10Y-2Y', data: yields, borderColor: '#bb86fc', pointRadius: 0, borderWidth: 2 }}] }},
                options: {{ scales: {{ x: {{ display: false }}, y: {{ grid: {{ color: '#444' }} }} }}, plugins: {{ legend: {{ display: false }} }} }}
            }});
            
            new Chart(document.getElementById('spreadChart'), {{
                type: 'line',
                data: {{ labels: dates, datasets: [{{ label: 'Spread', data: spreads, borderColor: '#03dac6', pointRadius: 0, borderWidth: 2 }}] }},
                options: {{ scales: {{ x: {{ display: false }}, y: {{ grid: {{ color: '#444' }} }} }}, plugins: {{ legend: {{ display: false }} }} }}
            }});
        </script>
    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
        
except Exception as e:
    print(f"Error: {e}")
