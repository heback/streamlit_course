import io

import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
import calendar

data_path = 'bike_sharing_demand/'
train = pd.read_csv(data_path + 'train.csv', parse_dates=['datetime'])
test = pd.read_csv(data_path + 'test.csv', parse_dates=['datetime'])
submission = pd.read_csv(data_path + 'sampleSubmission.csv', parse_dates=['datetime'])


def feature_engineering():
    train['year'] = train['datetime'].dt.year
    train['month'] = train['datetime'].dt.month
    train['day'] = train['datetime'].dt.day
    train['hour'] = train['datetime'].dt.hour
    train['minute'] = train['datetime'].dt.minute
    train['second'] = train['datetime'].dt.second
    train['date'] = train['datetime'].dt.date
    train['dayofweek'] = train['datetime'].dt.dayofweek
    train['season'] = train['season'].map({1: 'spring',
                                           2: 'summer',
                                           3: 'fall',
                                           4: 'winter'})

    train['weather'] = train['weather'].map({1: 'clear',
                                             2: 'mist, few clouds',
                                             3: 'light snow, rain, thunderstorm',
                                             4: 'heavy rain, thunderstorm, snow, fog'})
    train['weekday'] = train['date'].apply(
        lambda date: calendar.day_name[datetime.combine(date, datetime.min.time()).weekday()]
    )


st.title('Bike Sharing Demand')

mnu = st.sidebar.selectbox('메뉴', options=['설명', 'EDA', '시각화', '모델링'])

if mnu == '설명':
    st.subheader('설명')
    st.write('''
    자전거 공유 시스템은 회원 가입, 대여 및 자전거 반납 프로세스가 도시 전역의 키오스크 위치 네트워크를 통해 자동화되는 자전거 대여 수단입니다. 
    이러한 시스템을 사용하여 사람들은 한 위치에서 자전거를 빌리고 필요에 따라 다른 위치에 반납할 수 있습니다. 
    현재 전 세계적으로 500개가 넘는 자전거 공유 프로그램이 있습니다. 
    이러한 시스템에서 생성된 데이터는 여행 기간, 출발 위치, 도착 위치 및 경과 시간이 
    명시적으로 기록되기 때문에 연구자에게 매력적입니다. 
    따라서 자전거 공유 시스템은 도시의 이동성을 연구하는 데 사용할 수 있는 센서 네트워크로 기능합니다. 
    이 대회에서 참가자는 워싱턴 DC의 Capital Bikeshare 프로그램에서 
    자전거 대여 수요를 예측하기 위해 과거 사용 패턴과 날씨 데이터를 결합해야 합니다.
    ''')
    st.write('''
    2년 동안의 시간당 임대 데이터가 제공됩니다. 
    이 대회의 경우 훈련 세트는 매월 첫 19일로 구성되고 테스트 세트는 20일부터 월말까지입니다. 
    대여 기간 전에 사용할 수 있는 정보만 사용하여 테스트 세트에서 다루는 각 시간 동안 대여한 총 자전거 수를 예측해야 합니다.''')
    st.image('https://storage.googleapis.com/kaggle-competitions/kaggle/3948/media/bikes.png')
    st.markdown('#### 데이터 필드')
    st.markdown('**datetime** - 시간별 날짜 + 타임스탬프')
    st.markdown('**season** - 1 = 봄, 2 = 여름, 3 = 가을, 4 = 겨울')
    st.markdown('**holiday** - 해당 요일을 휴일')
    st.markdown('**workingday** - 요일이 주말이나 휴일')
    st.markdown('**weather** - 1: 맑음, 약간 구름, 부분 흐림, 부분 흐림')
    st.markdown('2: 안개 + 흐림, 안개 + 부서진 구름, 안개 + 약간 구름, 안개')
    st.markdown('3: 가벼운 눈, 약한 비 + 뇌우 + 흩어진 구름, 약한 비 + 흩어진 구름')
    st.markdown('4: 폭우 + 얼음 팔레트 + 뇌우 + 안개, 눈 + 안개')
    st.markdown('**temp** - 온도(섭씨)')
    st.markdown('**atemp** - 체감 온도(섭씨)')
    st.markdown('**humidity** - 상대습도')
    st.markdown('**windspeed** - 풍속')
    st.markdown('**casual** - 미등록 사용자 대여수')
    st.markdown('**registered** - 등록 사용자 대여수')
    st.markdown('**count** - 총 대여수')

elif mnu == 'EDA':

    st.subheader('EDA')

    st.markdown('- (훈련 데이터 shape, 테스트 데이터 shape)')
    st.text(f'({train.shape}), ({test.shape})')

    st.markdown('- 훈련 데이터')
    st.dataframe(train.head())

    st.markdown('- 피처 엔지니어링')
    st.text('시각화에 적합한 형태로 피처 변환')
    feature_engineering()
    st.code('''
    train['year'] = train['datetime'].dt.year
    train['month'] = train['datetime'].dt.month
    train['day'] = train['datetime'].dt.day
    train['hour'] = train['datetime'].dt.hour
    train['minute'] = train['datetime'].dt.minute
    train['second'] = train['datetime'].dt.second
    train['date'] = train['datetime'].dt.date
    train['dayofweek'] = train['datetime'].dt.dayofweek
    train['season'] = train['season'].map({1: 'spring',
                                           2: 'summer',
                                           3: 'fall',
                                           4: 'winter'})
    
    train['weather'] = train['weather'].map({1: 'clear',
                                             2: 'mist, few clouds',
                                             3: 'light snow, rain, thunderstorm',
                                             4: 'heavy rain, thunderstorm, snow, fog'})
    train['weekday'] = train['date'].apply(
        lambda date: calendar.day_name[datetime.combine(date, datetime.min.time()).weekday()]
    )
    ''')

    st.markdown('- 수정된 훈련 데이터')
    st.dataframe(train.head())

    st.markdown('- 테스트 데이터')
    st.dataframe(test.head())

    st.markdown('- 제출 데이터')
    st.dataframe(submission.head())

    st.markdown('- train.info()')
    buffer = io.StringIO()
    train.info(buf=buffer)
    st.text(buffer.getvalue())

    buffer.truncate(0) # 버퍼 비우기
    st.markdown('- test.info()')
    test.info(buf=buffer)
    st.text(buffer.getvalue())

elif mnu == '시각화':

    import seaborn as sns
    import matplotlib as mpl
    import matplotlib.pyplot as plt

    st.set_option('deprecation.showPyplotGlobalUse', False)

    feature_engineering()

    st.subheader('시각화')

    st.markdown('**:blue[그래프를 해석하세요.]**')

    mpl.rc('font', size=12)
    st.markdown('- count의 분포도')
    fig, axes = plt.subplots(nrows=1, ncols=2)
    sns.histplot(train['count'], ax=axes[0])
    sns.histplot(np.log(train['count']), ax=axes[1])
    fig.set_size_inches(10, 5)
    st.pyplot()
    st.write('원본 count값의 분포가 왼쪽으로 많이 편향되어 있어서 로그변환을 통해 정규분포에 가깝게 만듦.')

    st.markdown('- 년, 월, 일, 시간, 분, 초에 따른 대여량 평균치')
    mpl.rc('font', size=15)
    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(nrows=2, ncols=3)
    fig.set_size_inches(18, 13)

    sns.barplot(data=train, x="year", y="count", ax=ax1)
    sns.barplot(data=train, x="month", y="count", ax=ax2)
    sns.barplot(data=train, x="day", y="count", ax=ax3)
    sns.barplot(data=train, x="hour", y="count", ax=ax4)
    sns.barplot(data=train, x="minute", y="count", ax=ax5)
    sns.barplot(data=train, x="second", y="count", ax=ax6)

    ax1.set(title="Rental amounts by year")
    ax2.set(title="Rental amounts by month")
    ax3.set(title="Rental amounts by day")
    ax4.set(title="Rental amounts by hour")

    st.pyplot()

    st.markdown('- 시즌별, 시간별, 근무일/휴무일에 따른 대여량 평균치')
    mpl.rc('font', size=15)
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
    fig.set_size_inches(18, 13)

    sns.boxplot(data=train, x='season', y='count', ax=ax1)
    sns.boxplot(data=train, x='weather', y='count', ax=ax2)
    sns.boxplot(data=train, x='holiday', y='count', ax=ax3)
    sns.boxplot(data=train, x='workingday', y='count', ax=ax4)

    ax1.set(title='BoxPlot on Count Across Season')
    ax2.set(title='BoxPlot on Count Across Weather')
    ax3.set(title='BoxPlot on Count Across Holiday')
    ax4.set(title='BoxPlot on Count Across Working Day')

    st.pyplot()

    st.markdown('- 근무일, 공휴일, 요일, 계절, 날씨에 따른 시간대별 평균 대여 수량')
    mpl.rc('font', size=8)
    fig, axes = plt.subplots(nrows=5)
    plt.tight_layout()
    fig.set_size_inches(7, 13)

    sns.pointplot(x='hour', y='count', data=train, hue='workingday', ax=axes[0])
    sns.pointplot(x='hour', y='count', data=train, hue='holiday', ax=axes[1])
    sns.pointplot(x='hour', y='count', data=train, hue='weekday', ax=axes[2])
    sns.pointplot(x='hour', y='count', data=train, hue='season', ax=axes[3])
    sns.pointplot(x='hour', y='count', data=train, hue='weather', ax=axes[4])
    st.pyplot()

    st.markdown('- 온도, 체감 온도, 픙속, 습도별 대여 수량 산점도 그래프')
    mpl.rc('font', size=12)
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2)
    plt.tight_layout()
    fig.set_size_inches(7, 6)
    sns.regplot(x="temp", y="count", data=train, ax=ax1, scatter_kws={'alpha':0.2}, line_kws={'color':'blue'})
    sns.regplot(x="atemp", y="count", data=train, ax=ax2, scatter_kws={'alpha': 0.2}, line_kws={'color': 'blue'})
    sns.regplot(x="windspeed", y="count", data=train, ax=ax3, scatter_kws={'alpha':0.2}, line_kws={'color':'blue'})
    sns.regplot(x="humidity", y="count", data=train, ax=ax4, scatter_kws={'alpha':0.2}, line_kws={'color':'blue'})
    st.pyplot()

    st.markdown('- 피처 간 상관관계 매트릭스')
    corrMat = train[['temp', 'atemp', 'humidity', 'windspeed', 'count']].corr()
    fig, ax = plt.subplots()
    fig.set_size_inches(10, 10)
    sns.heatmap(corrMat, annot=True)
    ax.set(title='Heatmap of Numerical Data')
    st.pyplot()

    st.markdown('#### 분석 정리 및 모델링 전략')
    st.markdown('**1. 타깃값 변환:** 분포도 확인 결과 타깃값인 count가 0근처로 치우쳐 있으므로 로그변환하여 정규분포에 가깝게 만들어야한다. '
                '마지막에 다시 지수변환해 count로 복원해야 한다.')
    st.markdown('**2. 파생피처 추가:** datetime 피처는 여러 가지 정보의 혼합체이므로 '
                '각각을 분리해 year, month, day, hour, minute, second 피처를 생성할 수 있다.')
    st.markdown('**3. 파생피처 추가:** datetime 에 숨어 있는 또 다른 정보인 요일(weekday) 피처를 추가한다.')
    st.markdown('**4. 피처 제거:** 테스트 데이터에 없는 피처는 훈련에 사용해도 큰 의미가 없다. '
                '따라서 훈련 데이터에만 있는 casual과 registered 피처는 제거한다.')
    st.markdown('**5. 피처 제거:** datetime 피처는 인덱스 역할만 하므로 타깃값 예측에 아무런 도움이 되지 않는다.')
    st.markdown('**6. 피처 제거:** date 피처가 제공하는 정보도 year, month, day 피처에 담겨 있다.')
    st.markdown('**7. 피처 제거:** month는 season 피처의 세부 분류로 볼 수 있다. '
                '데이터가 지나치게 세분화되어 있으면 분류별 데이터수가 적어서 학습에 오히려 방해가 되기도 한다.')
    st.markdown('**8. 피처 제거:** 막대 그래프 확인 결과 day는 분별력이 없다.')
    st.markdown('**9. 피처 제거:** 막대 그래프 확인 결과 minute와 second에는 아무런 정보가 담겨 있지 않다.')
    st.markdown('**10. 이상치 제거:** 포인트 플롯 확인 결과 weather가 4인 데이터는 이상치이다.')
    st.markdown('**11. 피처 제거:** 산점도 그래프와 히트맵 확인 결과 '
                'windspeed 피처에는 결측값이 많고 대여 수량과의 상관관계가 매우 약하다.')

elif mnu == '모델링':

    data_path = 'bike_sharing_demand/'
    train = pd.read_csv(data_path + 'train.csv', parse_dates=['datetime'])
    test = pd.read_csv(data_path + 'test.csv', parse_dates=['datetime'])
    submission = pd.read_csv(data_path + 'sampleSubmission.csv', parse_dates=['datetime'])

    st.markdown('#### 피처 엔지니어링')
    st.markdown('**이상치 제거**')
    st.write('폭우, 번개 속에서 실제로 자전거를 대여했을 수도 있지만 이 한 건의 데이터가 머신러닝 훈련에 부정적 영향을 끼치기 때문에 제거하는 것이 좋습니다.')
    train = train[train['weather'] != 4]
    st.code("train = train[train['weather']!=4]")

    st.markdown('**데이터 합치기**')
    st.write('훈련 데이터와 테스트 데이터에 같은 피처 엔지니어링을 적용하기 위해 두 데이터를 합친다.')
    all_data_temp = pd.concat([train, test], ignore_index=True)
    st.code("all_data_temp = pd.concat([train, test])")

    st.dataframe(all_data_temp)



    