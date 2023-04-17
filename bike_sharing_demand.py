import io

import streamlit as st
import numpy as np
import pandas as pd

st.title('Bike Sharing Demand')

mnu = st.sidebar.selectbox('메뉴', options=['설명', 'EDA', 'MODELLING'])

if mnu == '설명':
    st.subheader('설명')
    st.write('자전거 공유 시스템은 회원 가입, 대여 및 자전거 반납 프로세스가 도시 전역의 키오스크 위치 네트워크를 통해 자동화되는 자전거 대여 수단입니다. 이러한 시스템을 사용하여 사람들은 한 위치에서 자전거를 빌리고 필요에 따라 다른 위치에 반납할 수 있습니다. 현재 전 세계적으로 500개가 넘는 자전거 공유 프로그램이 있습니다. 이러한 시스템에서 생성된 데이터는 여행 기간, 출발 위치, 도착 위치 및 경과 시간이 명시적으로 기록되기 때문에 연구자에게 매력적입니다. 따라서 자전거 공유 시스템은 도시의 이동성을 연구하는 데 사용할 수 있는 센서 네트워크로 기능합니다. 이 대회에서 참가자는 워싱턴 DC의 Capital Bikeshare 프로그램에서 자전거 대여 수요를 예측하기 위해 과거 사용 패턴과 날씨 데이터를 결합해야 합니다.')
    st.write('2년 동안의 시간당 임대 데이터가 제공됩니다. 이 대회의 경우 훈련 세트는 매월 첫 19일로 구성되고 테스트 세트는 20일부터 월말까지입니다. 대여 기간 전에 사용할 수 있는 정보만 사용하여 테스트 세트에서 다루는 각 시간 동안 대여한 총 자전거 수를 예측해야 합니다.')
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

    data_path = 'bike_sharing_demand/'
    train = pd.read_csv(data_path + 'train.csv')
    test = pd.read_csv(data_path + 'test.csv')
    submission = pd.read_csv(data_path + 'sampleSubmission.csv')

    st.text('(훈련 데이터 shape, 테스트 데이터 shape)')
    st.text(f'({train.shape}), ({test.shape})')

    st.text('훈련 데이터')
    st.dataframe(train.head())

    st.text('테스트 데이터')
    st.dataframe(test.head())

    st.text('제출 데이터')
    st.dataframe(submission.head())

    st.text('train.info()')
    buffer = io.StringIO()
    train.info(buf = buffer)
    st.text(buffer.getvalue())

    buffer.truncate(0) # 버퍼 비우기
    st.text('test.info()')
    test.info(buf = buffer)
    st.text(buffer.getvalue())

    st.text('datetime을 연도, 월, 일, 시, 분, 초 생성')
    train['date'] = train['datetime'].apply(lambda x:x.split()[0])
    train['year'] = train['datetime'].apply(lambda x: x.split()[0].split('-')[0])
    train['month'] = train['datetime'].apply(lambda x: x.split()[0].split('-')[1])
    train['day'] = train['datetime'].apply(lambda x: x.split()[0].split('-')[2])
    train['hour'] = train['datetime'].apply(lambda x: x.split()[1].split(':')[0])
    train['minute'] = train['datetime'].apply(lambda x: x.split()[1].split(':')[1])
    train['second'] = train['datetime'].apply(lambda x: x.split()[1].split(':')[2])
    from datetime import datetime
    import calendar
    train['weekday'] = train['date'].apply(lambda dateString: calendar.day_name[datetime.strptime(dateString, '%Y-%m-%d').weekday()])
    # print(list(calendar.day_name))
    # ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    train['season'] = train['season'].map({1: 'spring',
                                           2: 'summer',
                                           3: 'fall',
                                           4: 'winter'})

    train['weather'] = train['weather'].map({1: 'clear',
                                             2: 'mist, few clouds',
                                             3: 'light snow, rain, thunderstorm',
                                             4: 'heavy rain, thunderstorm, snow, fog'})
    st.write(train.head())

    st.text('date와 month 열 삭제')
    train = train.drop(['date', 'month'], axis=1)

    st.write(train.head())

elif mnu == 'MODELLING':
    pass