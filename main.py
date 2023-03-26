import streamlit as st
import newspaper
import nltk
import streamlit.components.v1 as components

nltk.download('punkt')

# st.markdown('<style> .css-1v0mbdj {margin:0 auto; width:50%; </style>', unsafe_allow_html=True)
# port = 10000
# st.set_option('server.port', port)
# st.set_option('server.address', '0.0.0.0')

st.title('Article Summarizer')

url = st.text_input(
    '', placeholder='Paste the URL of the article amd press Enter')

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
        st.text(','.join(authors))

        article.nlp()

        keywords = article.keywords
        st.subheader('Keywords:')
        st.write(', '.join(keywords))

        tab1, tab2 = st.tabs(["Full Text", "Summary"])
        with tab1:
            txt = article.text
            txt = txt.replace('Advertisement', '')
            st.write(txt)

        with tab2:
            st.subheader('Summary')
            summary = article.summary
            summary = summary.replace('Advertisement', '')
            st.write(summary)

    except:
        st.error('Sorry something went wrong')
