import polars as pl
import pandas as pd
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from multiprocessing import Pool
from tqdm import tqdm
import time

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """Analyze sentiment of a single text"""
    return analyzer.polarity_scores(str(text))["compound"]

def get_sentiment_label(compound_score):
    """Convert compound score to label"""
    if compound_score >= 0.05:
        return "good"
    elif compound_score <= -0.05:
        return "bad"
    else:
        return "neutral"

if __name__ == "__main__":
    BATCH_SIZE = 200_000
    start_time = time.time()
    data_file = os.path.abspath("data-lake/reddit/raw/new_tag_data.pkl")
    print(f"Loading data index from: {data_file}")
    pandas_df = pd.read_pickle(data_file)[["score", "body", "subreddit"]]
    total_rows = len(pandas_df)
    print(f"Total rows: {total_rows}")
    

    os.makedirs("data-lake/reddit/processed", exist_ok=True)

    output_dir = "data-lake/reddit/processed"
    os.makedirs(output_dir, exist_ok=True)

    batch_count = 0
    for batch_num, start in enumerate(range(0, total_rows, BATCH_SIZE)):
        end = min(start + BATCH_SIZE, total_rows)
        print(f"\nProcessing rows {start} to {end-1} (batch size: {end-start})...")
        batch_df = pandas_df.iloc[start:end]
        print(f"Batch {batch_num + 1}: {len(batch_df)} rows")
        data = pl.from_pandas(batch_df)

        with Pool() as pool:
            sentiments = list(tqdm(
                pool.imap(analyze_sentiment, data["body"], chunksize=1000),
                total=len(data),
                desc="Analyzing sentiments"
            ))

        data = data.with_columns([
            pl.Series("sentiment_score", sentiments),
        ])
        data = data.with_columns([
            pl.col("sentiment_score").map_elements(get_sentiment_label).alias("sentiment_label")
        ])

        batch_parquet_path = os.path.join(output_dir, f"fact_comments_batch_{batch_num}.parquet")
        data.write_parquet(batch_parquet_path)
        print(f"Batch {batch_num + 1} processed and saved to {batch_parquet_path}.")
        batch_count += 1

    # Print summary after all batches are processed
    print(f"\nAll batches processed and saved to separate Parquet files in {output_dir}.")
    print(f"Total batches written: {batch_count}")
    
