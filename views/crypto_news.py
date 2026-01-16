import streamlit as st
import feedparser
from datetime import datetime
import re
import html

def clean_html(text):
    if not text:
        return ""
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def render():

    st.set_page_config(page_title="Crypto News", layout="wide")
    st.title("Crypto News & Market Updates")

    RSS_URL = "https://news.google.com/rss/search?q=cryptocurrency"

    feed = feedparser.parse(RSS_URL)

    if not feed.entries:
        st.error("Unable to load cryptocurrency news at the moment.")
        return

    st.subheader("Latest Cryptocurrency Market News")

    shown = 0

    for entry in feed.entries:

        title = clean_html(entry.get("title", ""))
        summary_raw = entry.get("summary", "")
        summary = clean_html(summary_raw)
        published = entry.get("published", "")

        st.markdown("---")
        st.markdown(f"### {title}")

        if published:
            try:
                dt = datetime(*entry.published_parsed[:6])
                st.caption(dt.strftime("%d %b %Y, %H:%M"))
            except Exception:
                st.caption(published)

        if summary:
            sentences = summary.split(".")
            context = ". ".join(sentences[:5]).strip()
            st.write(context + ("..." if len(sentences) > 5 else ""))
        else:
            st.write("Summary not available.")

        shown += 1
        if shown >= 8:
            break

    st.subheader("Why This Matters")

    st.markdown("""
This module integrates **live cryptocurrency market news** via RSS feeds
and presents concise, readable summaries directly within the platform.

By exposing users to recent regulatory, technological, and market-wide
developments, the system provides essential **external context** to support
informed and explainable decision-making, in accordance with AE2 requirements.
""")
