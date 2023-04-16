import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import io
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

titanic = sns.load_dataset('titanic')

st.write(titanic.head())
st.write(titanic.columns)

st.dataframe(titanic.head())

buffer = io.StringIO()
titanic.info(buf=buffer)
st.text(buffer.getvalue())

st.dataframe(titanic.describe(include='all'), use_container_width=True)

st.text('객실 등급(pclass)에 따른 생존율 비교')
st.dataframe(titanic[['pclass', 'survived']].groupby(['pclass'], as_index=True).mean().sort_values(by='survived', ascending=False))

st.text('성별(sex)에 따른 생존율 비교')
st.dataframe(titanic[["sex", "survived"]].groupby(['sex'], as_index=True).mean().sort_values(by='survived', ascending=False))

st.text('함께 승선한 형제자매와 배우자 수(sibsp)에 따른 생존율 비교')
st.dataframe(titanic[["sibsp", "survived"]].groupby(['sibsp'], as_index=True).mean().sort_values(by='sibsp', ascending=False))

st.text('승선한 부모와 자식 수(parch)에 따른 생존율 비교')
st.dataframe(titanic[["parch", "survived"]].groupby(['parch'], as_index=True).mean().sort_values(by='parch', ascending=False))

st.set_option('deprecation.showPyplotGlobalUse', False)
st.text('생존 여부(survived)에 따른 연령(age) 분포')
g = sns.FacetGrid(titanic, col='survived')
g.map(plt.hist, 'age', bins=20)
st.pyplot()

# https://computer-science-student.tistory.com/113

st.text('성별, 생존 여부(sex, survived)에 따른 요금(fare) 분포')
g = sns.FacetGrid(titanic, col='sex', row='survived')
g.map(plt.hist, 'fare', bins=20)
st.pyplot()

st.text('성별, 생존 여부(sex, survived)에 따른 요금(fare), 나이(age) 분포')
g = sns.FacetGrid(titanic, col='sex', hue='survived')
g.map(sns.regplot, 'fare', 'age', fit_reg=False)
g.add_legend()
st.pyplot()

st.text('성별, 생존 여부(sex, survived)에 따른 요금(fare), 나이(age), 등급(class) 분포')
g = sns.FacetGrid(titanic, col='sex', row='survived', hue='class')
g.map(sns.regplot, 'fare', 'age', fit_reg=False)
g.add_legend()
st.pyplot()

st.text('생존 여부, 등급에 따른 나이(age) 분포')
g = sns.FacetGrid(titanic, col='survived', row='class', hue='class')
g.map(plt.hist, 'age', bins=20)
g.add_legend()
st.pyplot()

st.text('승선지(embarked)와 객실 등급(pclass)에 따른 생존율(survived)')
grid = sns.FacetGrid(titanic, row='embarked', height=2.2, aspect=1.6)
# Pointplot으로 시각화, x: 객실 등급, y: 생존 여부, 색깔: 성별, x축 순서: [1, 2, 3], 색깔 순서: [남성, 여성]
grid.map(sns.pointplot, x='pclass', y='survived', hue='sex', palette='deep', order = [1, 2, 3], hue_order = ["male", "female"])
g.add_legend()
st.pyplot()


#############################################################################

st.subheader('히스토그램')
fig = plt.figure(figsize=(12, 6))

plt.title('titanic histogram(age)')
sns.histplot(data=titanic, x='age')
st.pyplot(plt.gcf(), clear_figure=True)

plt.title('titanic histogram(age-alive)')
sns.histplot(data=titanic, x='age', hue='alive')
st.pyplot(fig, clear_figure=True)

plt.title('titanic histogram(age-alive-stack)')
sns.histplot(data=titanic, x='age', hue='alive', multiple='stack')
st.pyplot(fig, clear_figure=True)

st.subheader('커널정밀도추정 함수 그래프')
plt.title('titanic kde(age)')
sns.kdeplot(data=titanic, x='age')
st.pyplot(fig, clear_figure=True)

plt.title('titanic kde(age-alive)')
sns.kdeplot(data=titanic, x='age', hue='alive', multiple='stack')
st.pyplot(fig, clear_figure=True)

st.subheader('러그플롯')
plt.title('titanic regplot(age)')
sns.kdeplot(data=titanic, x='age')
sns.rugplot(data=titanic, x='age')
st.pyplot(fig, clear_figure=True)

st.subheader('막대 그래프')
plt.title('titanic barplot(class)')
sns.barplot(data=titanic, x='class', y='fare')
st.pyplot(fig, clear_figure=True)

st.subheader('포인트 플롯')
plt.title('titanic pointplot(class)')
sns.pointplot(data=titanic, x='class', y='fare')
st.pyplot(fig, clear_figure=True)

st.subheader('박스 플롯')
plt.title('titanic pointplot(class)')
sns.boxplot(data=titanic, x='class', y='age')
st.pyplot(fig, clear_figure=True)