

 # libraries
import feedparser
import pandas as pd
import logging




def get_rss_feed_stackoverflow(tag: str) -> pd.DataFrame:

    """
    Retrieve the data from the stackoverflow feed using feedparser

    :param tag: the subject of the stackoverflow feed
    :return: the dataframe with the data
    
    """
    # URL of the RSS feed for the 'r' tag, sorted by newest
    rss_url = f"https://stackoverflow.com/feeds/tag?tagnames={tag}&sort=newest"

    # Parse the feed
    feed = feedparser.parse(rss_url)

    logging.info(f"Feed retrieved from {rss_url}")

    # Display the feed entries
    df = pd.DataFrame(columns=[
        "ID", "Title", "Link", "Published", "Updated", "Summary", "Author", 
        "Category", "Author Detail", "Tags"
    ])

    # check if the feed is empty or the number of line in the dataframe is correct

    number_of_entries = len(feed.entries)

    if number_of_entries == 0:
        AssertionError("No entries found in the feed")
    
    if number_of_entries != len(feed.entries):
        AssertionError(f"The number of entries is not correct: {number_of_entries} vs {len(feed.entries)}")

    for entry in feed.entries:
        new_row = {
            "ID": entry.id,
            "Title": entry.title,
            "Link": entry.link,
            "Published": pd.to_datetime(entry.published, errors='coerce'),
            "Updated": entry.updated,
            "Summary": entry.summary,
            "Author": entry.author,
            "Category": getattr(entry, 'category', ''),  # Utilise getattr pour éviter les erreurs si l'attribut n'existe pas
            "Author Detail": str(entry.author_detail),
            "Tags": str(entry.tags)
        }

        # Add the new row to the dataframe
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    
    
    logging.info(f"Data retrieved from the RSS feed: {df.shape[0]} entries")
    
    # Déplacé ici, en dehors de la boucle
    return df


df = get_rss_feed_stackoverflow("r")

def check_data_quality(df: pd.DataFrame) -> None:

    """
    Check the quality of the data

    :param df: the dataframe with the data
    :return: None
    
    """
    # Check the data quality
    assert df.shape[0] > 0, "No data in the dataframe"
    assert df.shape[1] == 10, f"Wrong number of columns in the dataframe: {df.shape[1]} instead of 10"
    assert df.isnull().sum().sum() == 0, "Missing values in the dataframe"
    assert df.duplicated().sum() == 0, "Duplicated values in the dataframe"
    assert df["ID"].duplicated().sum() == 0, "Duplicated IDs in the dataframe"
    assert pd.api.types.is_datetime64_any_dtype(df['Published']), "Erreur : 'date_col' n'est pas au format datetime"
    logging.info("Data quality checked")



check_data_quality(df)