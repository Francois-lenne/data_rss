import feedparser

# URL of the RSS feed for the 'r' tag, sorted by newest
rss_url = "https://stackoverflow.com/feeds/tag?tagnames=r&sort=newest"

# Parse the feed
feed = feedparser.parse(rss_url)

# Display the feed title
print(f"Feed Title: {feed.feed.title}\n")

# Loop through the entries and display details
for entry in feed.entries[:5]:  # Limiting to the first 5 entries
    print(f"Title: {entry.title}")
    print(f"Link: {entry.link}")
    print(f"Published: {entry.published}")
    print(f"Summary: {entry.summary}\n")
