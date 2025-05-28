# libraries
import feedparser
import pandas as pd
import logging
import warnings
import ast
import os
import re
import correct_r_code
# from google.cloud import bigquery

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


def store_r_code_gcp_storage(df: pd.DataFrame) -> None:
    """
    Store the R code provide by the user in a r file in a google cloud storage

    :param df: the dataframe with the data
    :return: None
    
    """
    
    # Créer un dossier pour stocker les fichiers s'il n'existe pas
    output_dir = "stackoverflow_codes"
    os.makedirs(output_dir, exist_ok=True)

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
        
        # Create the file name
        file_name = f"{output_dir}/stackoverflow_code_{id}_{update_date}.R"

        r_code_modfied = correct_r_code.add_comment_code(r_code, "# ")        
        # Store the file
        with open(file_name, 'w') as f:
            f.write(r_code_modfied)
            logging.info(f"File {file_name} stored in the google cloud storage")


store_r_code_gcp_storage(df)


def load_bigquery(df: pd.DataFrame, project_id: str, dataset_id: str) -> None:
    """
    Load the data in a bigquery table

    :param df: the dataframe with the data
    :param project_id: the id of the project
    :param dataset_id: the id of the dataset
    :return: None
    
    """
    

    # Create a BigQuery client
    client = bigquery.Client(project=project_id)

    # Define the table ID
    table_id = f"{project_id}.{dataset_id}.stackoverflow_data"

    # Load the dataframe into BigQuery
    job = client.load_table_from_dataframe(df, table_id)

    # Wait for the job to complete
    job.result()

    logging.info(f"Data loaded in BigQuery table {table_id}")