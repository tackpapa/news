import streamlit as st
import newspaper
import nltk
import openai
import os
from dotenv import load_dotenv

load_dotenv()


nltk.download('punkt')

openai.api_key = os.getenv("api_key")


st.title('뉴스 변형기')


url = st.text_input(
    '', placeholder='뉴스기사 링크를 여기에 넣고 엔터를 누르세요.')

if url:
    try:
        article = newspaper.Article(url)

        article.download()
        # article.html
        article.parse()

        img = article.top_image
        st.image(img)

        title = article.title
        st.subheader(title)

        authors = article.authors

        article.nlp()

        tab1, tab2 = st.tabs(["전체기사", "요약본"])
        with tab1:
            txt = article.text
            txt = txt.replace('Advertisement', '')
            st.write(txt)

        with tab2:
            st.subheader('Summary')
            summary = article.summary
            summary = summary.replace('Advertisement', '')
            st.write(summary)

        if article.text:
            try:

                if st.button("기사 요약 만들기! 누르고 기다리세요", type='primary'):
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "user", "content": f"You are now a professional Korean reporter. Rewrite this article as long as possible in Korean. Write in reporter tone like a 3rd person. The length should be 150% of original content. Do not give explanations, give me only the output. the article: + {article.text}"},
                        ]
                    )

                    res = response["choices"][0]["message"]

                st.text_area("결과물", value=res.content, height=500)

            except:
                st.success("")

    except:
        st.success("")


st.title('스크립트=>블로그글')

CONTEXT_LENGTH = 8000

pt = st.text_area("스크립트를 넣어주세요", height=500)
if st.button("기사 요약 만들기! 누르고 기다리세요", type='primary'):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": f"make this text into a blog post. should be colloquial. 3rd person view in Korean. make it engaging. + {pt}"},
        ]
    )

    res = response["choices"][0]["message"]

    st.text_area("결과물", value=res.content, height=500)
