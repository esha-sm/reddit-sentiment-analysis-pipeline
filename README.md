# Reddit Insights Engine: Scalable Data Pipeline & Analytics System

## Overview
This project builds an end-to-end data pipeline to process and analyze large-scale Reddit comment data. It combines data engineering, data warehousing, and machine learning (sentiment analysis) to extract meaningful insights.

## Architecture

![Pipeline Diagram](pipeline.png)


## Tech Stack

- Python
- Pandas
- Polars
- DuckDB
- SQL
- Parquet
- VADER Sentiment Analysis
- Multiprocessing


## Key Features

- Processed **4.5M+ Reddit comments**
- Built a **batch + parallel processing pipeline**
- Implemented **sentiment analysis on text data**
- Designed a **star schema (fact + dimension tables)**
- Optimized storage using **Parquet (columnar format)**
- Enabled fast querying using **DuckDB**


## Example Insights

- Most discussed Reddit topics
- Average sentiment per topic
- Engagement patterns based on comment scores



## Sample Query

```sql
SELECT t.Topic, AVG(f.sentiment_score) AS avg_sentiment
FROM fact_comments_final f
JOIN dim_topic t ON f.topic_id = t.rowid
GROUP BY t.Topic
ORDER BY avg_sentiment DESC;
```

## Future Work
- Integrate real-time streaming data from Reddit API (pending approval)

