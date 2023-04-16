import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

titanic = sns.load_dataset('titanic')

st.write(titanic.head())
st.write(titanic.columns)

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

