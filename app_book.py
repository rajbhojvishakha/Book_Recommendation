import pandas as pd
import streamlit as st
import pickle
import time
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


st.set_page_config(
    page_title="Book Recommendation System",
    page_icon="📚",
    layout="centered"
)


st.markdown("""
<style>
.stApp{
    background-color:#FCFCFD;
}
</style>
""",unsafe_allow_html=True)


st.markdown("""
<style>
h1{
    color:#4B2E2B;
    text-align:center;
    font-weight:bold;
}
</style>
""",unsafe_allow_html=True)



st.markdown("""
<style>

/* Sidebar */
[data-testid="stSidebar"]{
    background-color:#F8EEEC;
}

/* Sidebar Text */
[data-testid="stSidebar"] *{
    color:#4B2E2B;
}

</style>
""", unsafe_allow_html=True)


st.title("📚 Book Recommendation System")
st.divider()
st.info(
    "Select a book from the dropdown and click Recommend to discover similar books."
)

with st.sidebar:

    st.header("📖 About")

    st.write("""
This project recommends books based on

✔ Genre

✔ Summary

using

• TF-IDF

• Cosine Similarity
""")




df = pd.read_csv('clean_data_books.csv')

if not os.path.exists("similarities.pkl"):

    tfidf = TfidfVectorizer(max_features=5000,stop_words="english")
    vectors = tfidf.fit_transform(df["tags"]).toarray()
    similarities = cosine_similarity(vectors)
    pickle.dump(similarities, open("similarities.pkl", "wb"))

else:
    similarities = pickle.load(open("similarities.pkl", "rb"))

title=df['title'].tolist()
name=st.selectbox('Select a Book Name',title)



def get_name_by_index(i):

    if 0 <= i < len(df):

        return df.loc[i, "title"]

    return ""

def get_book_index(book_name):

    found_index = -1

    for i in df.index:

        if df.loc[i, "title"].lower() == book_name.lower():

            found_index = i
            break

    return found_index



def recommend(book_name):

    index = get_book_index(book_name)

    if index == -1:

        return None

    similarity_indexes = list(
        enumerate(similarities[index])
    )

    similarity_indexes = sorted(
        similarity_indexes,
        key=lambda x: x[1],
        reverse=True
    )

    
    books = []

    for i in range(1, number+1):

        books.append(
            get_name_by_index(
                similarity_indexes[i][0]
            )
        )

    return books




st.markdown("""
<style>
.stButton > button{
    background-color:#D4A373;
    color:white;
    border:none;
    border-radius:12px;
    padding:10px 18px;
    font-size:17px;
    font-weight:600;
}
</style>
""",unsafe_allow_html=True)
st.markdown("""
<style>
.stButton > button:hover{
    background-color:#BC8A5F;
    color:white;
    border:none;
}
</style>
""",unsafe_allow_html=True)



st.markdown("""
<style>
div[data-baseweb="select"] > div {
    border-radius: 10px;
}
            div[data-baseweb="select"] > div:hover{
/* hover */
    background-color:#BC8A5F;
    box-shadow:0 0 10px rgba(21,101,192,0.3);
    cursor:pointer;
}
</style>
""", unsafe_allow_html=True)



number = st.slider("Number of Book Recommendations",1,10,5)
if st.button("📚 Recommend"):

    recommendations = recommend(name)

    if recommendations is None:

        st.error("Book not found.")

    else:

        with st.spinner("Finding similar books..."):

            time.sleep(2)

        st.success("Recommendations Ready!")

        st.write(f"### Because you read **{name}**")
        for book in recommendations:
            st.markdown(f"""
            <div style="
                background:#F8EEEC;
                padding:18px;
                border-radius:14px;
                margin-bottom:12px;
                border-left:6px solid #BC8A5F;
                color:#0F172A;
                font-size:18px;
                font-weight:600;
                box-shadow:0px 3px 8px rgba(0,0,0,0.08);
            ">
                📖 {book}
            </div>
            """, unsafe_allow_html=True)