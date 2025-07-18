# libraries
import feedparser
import pandas as pd
import logging
import warnings
import ast
import os
import re
import correct_r_code
from google.cloud import storage
from google.cloud import bigquery
from datetime import datetime
import pytz

warnings.filterwarnings("ignore")


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


    print((f"{len(df)} entries retrieved from the feed"))
    
    
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


def parsed_chain(df: pd.DataFrame) -> None:

    """
    Parse all the chain column (type of data) and transform it in string or array

    :param df: the dataframe with the data
    :return df: the dataframe with the data without chain 
    
    """
    df['Tags_list'] = df['Tags'].apply(lambda x: [item['term'] for item in ast.literal_eval(x)])

    df['Author_link'] = df['Author Detail'].apply(lambda x: ast.literal_eval(x)['href'] if 'href' in ast.literal_eval(x) else None)


    df = df.drop(columns=['Author Detail', 'Tags', 'Category'])  # delete unnecessary columns


    return df

df = parsed_chain(df)


print(df.head())


def store_r_code_gcp_storage(df: pd.DataFrame, bucket_name: str) -> None:
    """
    Store the R code provided by the user in R files in Google Cloud Storage

    :param df: the dataframe with the data
    :param bucket_name: nom du bucket GCS
    :return: None
    """

    print(os.getenv('BUCKET_NAME'))
    
    # Initialiser le client GCS
    client = storage.Client()
    bucket = client.bucket(bucket_name)



    for index, row in df.iterrows():
        # Get the R code from the row
        r_code = row['Summary']
        
        # Get the ID of the row - extrait uniquement les chiffres après "q/"
        full_id = row['ID']
        # Utiliser une expression régulière pour extraire seulement le nombre après "q/"
        id_match = re.search(r'q/(\d+)', str(full_id))
        if id_match:
            id = id_match.group(1)  # Le premier groupe capturé (les chiffres)
        else:
            id = "unknown"  # Valeur par défaut si le pattern n'est pas trouvé
        
        # Formater la date pour éviter les caractères spéciaux
        update_date = re.sub(r'[:/\?<>\\:\*\|"]', '_', str(row['Updated']))
        
        # Create the file name (chemin dans GCS)
        file_name = f"stackoverflow_codes/stackoverflow_code_{id}_{update_date}.R"

        r_code_modified = correct_r_code.add_comment_code(r_code, "# ")        
        
        # Créer un blob et charger le contenu directement
        blob = bucket.blob(file_name)
        blob.upload_from_string(r_code_modified, content_type='text/plain')
        
        logging.info(f"File {file_name} stored in Google Cloud Storage")

        

# Utilisation
# store_r_code_gcp_storage(df, os.getenv('BUCKET_NAME'))



def load_bigquery(df: pd.DataFrame, dataset_id: str) -> None:
    """
    Load the data in a bigquery table

    :param df: the dataframe with the data
    :param project_id: the id of the project
    :param dataset_id: the id of the dataset
    :return: None
    
    """

    # modify the dataframe to match the BigQuery schema
    df_for_bg = df.drop(columns=['Summary']).copy()
    
    df_for_bg = df_for_bg.astype(str)
    df['Title'] = df['Title'].fillna('EMPTY')  # Ou un placeholder du type 'UNKNOWN'
    paris_tz = pytz.timezone('Europe/Paris')
    df_for_bg['ingestion_timestamp'] = datetime.now(paris_tz)

    # Create a BigQuery client
    client = bigquery.Client()

    # Define the table ID
    project_id = client.project
    table_id = f"{project_id}.{dataset_id}.stackoverflow_r_bronze"

    # Load the dataframe into BigQuery
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")

    job = client.load_table_from_dataframe(df_for_bg, table_id, job_config=job_config)

    # Wait for the job to complete
    job.result()

    logging.info(f"Data loaded in BigQuery table {table_id}")


load_bigquery(df, 'rss')