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

