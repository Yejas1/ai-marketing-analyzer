import streamlit as st
import snscrape.modules.twitter as sntwitter
import openai

# Load OpenAI API key from secrets
openai.api_key = st.secrets["openai_api_key"]

# Streamlit page setup
st.set_page_config(
    page_title="AI Marketing Analyzer",
    page_icon="📊",
    layout="centered"
)

# Custom dark theme styling
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
        color: #FFFFFF;
        font-family: 'Segoe UI', sans-serif;
    }
    .stTextInput>div>div>input {
        background-color: #262730;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.title("📊 AI Marketing Analyzer")
st.markdown("**Get smart marketing insights from your Twitter profile.** Just paste the link and let AI do the rest!")

# User input: Twitter profile URL
profile_url = st.text_input("🔗 Twitter Profile URL", placeholder="e.g., https://twitter.com/naval")

# Helper: extract username from URL
def extract_username(url):
    return url.rstrip("/").split("/")[-1]

# Helper: fetch recent tweets using snscrape
def get_recent_tweets(username, limit=15):
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterUserScraper(username).get_items()):
        if i >= limit:
            break
        tweets.append(tweet.content)
    return tweets

# Helper: use OpenAI to analyze and generate insights
def generate_insights(tweets):
    prompt = f"""
    You're a social media marketing coach. Analyze the following tweets and give:
    - 3 actionable tips to improve content strategy, engagement, or tone
    - 1 tweet idea that aligns with the current style

    Tweets:
    {'\\n'.join(tweets)}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response['choices'][0]['message']['content']

# 🔘 Analyze Now button logic
if st.button("🚀 Analyze Now"):
    if not profile_url:
        st.warning("Please enter a Twitter profile link.")
    else:
        with st.spinner("🔍 Fetching tweets and analyzing with AI..."):
            try:
                st.write("✅ Starting analysis...")
                username = extract_username(profile_url)
                st.write(f"👤 Username extracted: {username}")
                tweets = get_recent_tweets(username)
                st.write(f"📄 Number of tweets fetched: {len(tweets)}")

                if tweets:
                    insights = generate_insights(tweets)
                    st.success("✅ Done! Here's what we found:")
                    st.subheader("💡 AI Insights")
                    st.markdown(insights)
                else:
                    st.error("❌ No tweets found or invalid profile.")
            except Exception as e:
                st.error(f"🚨 Error occurred: {e}")

