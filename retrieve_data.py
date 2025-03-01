

 # libraries
import feedparser
import pandas as pd




def get_rss_feed_stackoverflow(tag):

    """
    Retrieve the data from the stackoverflow feed using feedparser

    :param tag: the subject of the stackoverflow feed
    :return: the dataframe with the data
    
    """
    # URL of the RSS feed for the 'r' tag, sorted by newest
    rss_url = f"https://stackoverflow.com/feeds/tag?tagnames={tag}&sort=newest"

    # Parse the feed
    feed = feedparser.parse(rss_url)

    # Display the feed entries
    df = pd.DataFrame(columns=[
        "ID", "Title", "Link", "Published", "Updated", "Summary", "Author", 
        "Category", "Author Detail", "Tags"
    ])

    number_of_entries = len(feed.entries)
    print(f"Number of entries: {number_of_entries}")

    for entry in feed.entries:
        new_row = {
            "ID": entry.id,
            "Title": entry.title,
            "Link": entry.link,
            "Published": entry.published,
            "Updated": entry.updated,
            "Summary": entry.summary,
            "Author": entry.author,
            "Category": getattr(entry, 'category', ''),  # Utilise getattr pour éviter les erreurs si l'attribut n'existe pas
            "Author Detail": str(entry.author_detail),
            "Tags": str(entry.tags)
        }

        # Add the new row to the dataframe
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    
    # Déplacé ici, en dehors de la boucle
    return df


df = get_rss_feed_stackoverflow("r")

print(f"Dataframe lenght: {len(df)}")