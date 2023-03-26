import streamlit as st
import newspaper
import nltk
import openai

nltk.download('punkt')
# openai.api_key = st.secrets["pass"]


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
        # st.text(','.join(authors))

        article.nlp()

        # keywords = article.keywords
        # st.subheader('Keywords:')
        # st.write(', '.join(keywords))

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
                # article_text = st.text_area(
                #     "기사넣기", value=article.text, height=200)
                # out_token = 2000

                if st.button("기사 요약 만들기! 누르고 기다리세요", type='primary'):
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "user", "content": f"You are now a professional Korean reporter. Rewrite this article as long as possible in Korean. Write in reporter tone like a 3rd person. The length should be 150% of original content. Do not give explanations, give me only the output. the article: + {article.text}"},
                        ]
                    )

                    res = response["choices"][0]["message"]

                st.text_area("결과물", value=res.content, height=500)

                # if res.content:
                #     if st.button("기사가 끈겼을때 누르세요", type='primary'):
                #         response1 = openai.ChatCompletion.create(
                #             model="gpt-3.5-turbo",
                #             messages=[
                #                 {"role": "user", "content": f"You are now a professional Korean reporter. Paraphrase and rewrite this article in Korean. The length should be 70% of original content. Do not give explanations, give me only the output. the article: + {article.text}"},
                #                 {"role": "assistant", "content": f"{res.content}"},
                #                 {"role": "user", "content": "계속해, 두배로 늘려써 줘 "}
                #             ]
                #         )
                #         print(response1)
                #         res1 = response1["choices"][0]["message"]

                #         st.text_area("결과물2", value=res.content +
                #                      res1.content, height=500)
                # else:
                #     st.success("")

            except:
                st.success("")

    except:
        st.success("")
