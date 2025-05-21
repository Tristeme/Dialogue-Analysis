import streamlit as st
import pandas as pd
from analysis import compute_sentiment, compute_filler_ratio

st.title("Dialogue Sentiment and Filler-Word Analysis")

# upload file
uploaded_file = st.file_uploader("📤 Upload a transcript (.txt) file", type="txt")

# read file
def parse_lines(lines):
    data = []
    for line in lines:
        if ":" in line:
            speaker, text = line.strip().split(":", 1)
            speaker = speaker.strip()
            text = text.strip()
            sentiment, score = compute_sentiment(text)
            filler_ratio = compute_filler_ratio(text)
            word_count = len(text.split())
            data.append({
                "Speaker": speaker,
                "Text": text,
                "Sentiment": sentiment,
                "Possibility": score,
                "Filler Ratio": filler_ratio,
                "Word Count": word_count
            })
    return pd.DataFrame(data)

# use upload file if there's any；otherwise use transcript.txt
if uploaded_file is not None:
    lines = uploaded_file.read().decode("utf-8").splitlines()
    st.success("✅ File uploaded successfully!")
else:
    with open("transcript.txt", "r") as f:
        lines = f.readlines()
    st.info("💡 No file uploaded. Using default transcript.txt")

df = parse_lines(lines)

# show table
st.subheader("Per-Turn Analysis")
st.dataframe(df)

# show Averages
st.subheader("Overall Averages")
st.write(f"**Average Filler Ratio**: {df['Filler Ratio'].mean():.3f}")
st.write(f"**Sentiment Distribution**:")
st.bar_chart(df['Sentiment'].value_counts())

# show filter ratio
st.subheader("Filler Ratio by Speaker")
st.bar_chart(df.groupby("Speaker")["Filler Ratio"].mean())

# Creative Extension：Word-count for each speaker
st.subheader("Total Word Count per Speaker")
wordcount_df = df.groupby("Speaker")["Word Count"].sum()
st.bar_chart(wordcount_df)