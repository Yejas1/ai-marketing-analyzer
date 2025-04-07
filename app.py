import streamlit as st
import openai

# Load OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["openai_api_key"]

st.set_page_config(
    page_title="AI Marketing Analyzer",
    page_icon="📊",
    layout="centered"
)

# Custom styling
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

# Title and description
st.title("📊 AI Marketing Analyzer")
st.markdown("**Get smart marketing insights from your Twitter profile.** Just paste the link and let AI do the rest!")

# Input field
profile_url = st.text_input("🔗 Twitter Profile URL", placeholder="e.g., https://twitter.com/naval")

# Function to extract username
def extract_username(url):
    return url.rstrip("/").split("/")[-1]

# ✅ Mock tweet generator (for now)
def get_recent_tweets(username, limit=15):
    tweets = [
        "Excited to announce my latest project!",
        "Building in public has been so rewarding.",
        "Top 3 marketing tips I learned this week...",
        "Reflecting on my journey so far.",
        "Here’s a thread on growth hacking 🔥",
        "Just hit 10k followers — thank you all!",
        "Quick thread: How to go viral on X 👇",
        "Marketing tip: Post consistently and add value.",
        "Don’t sell. Tell stories.",
        "Consistency wins over talent every time.",
    ]
    return tweets[:limit]

# Function to get insights using OpenAI
def generate_insights(tweets):
    prompt = f"""
    You're a social media marketing coach. Analyze the following tweets and give:
    - 3 actionable tips to improve content strategy, engagement, or tone
    - 1 tweet idea that aligns with the current style

    Tweets:
    {'\n'.join(tweets)}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response['choices'][0]['message']['content']

# Button to trigger analysis
if st.button("🚀 Analyze Now"):
    if not profile_url:
        st.warning("Please enter a Twitter profile link.")
    else:
        with st.spinner("🔍 Fetching tweets and analyzing with AI..."):
            username = extract_username(profile_url)
            tweets = get_recent_tweets(username)
            if tweets:
                insights = generate_insights(tweets)
                st.success("✅ Done! Here's what we found:")
                st.subheader("💡 AI Insights")
                st.markdown(insights)
            else:
                st.error("❌ No tweets found or invalid profile.")


