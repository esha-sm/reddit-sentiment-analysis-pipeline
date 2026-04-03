import duckdb
import os

def setup_database():
    """Initialize DuckDB with sentiment analysis schema"""
    db_path = "data-lake/reddit/sentiment.db"
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = duckdb.connect(db_path)
    
    # Create sequence for auto-increment FIRST
    conn.execute("CREATE SEQUENCE IF NOT EXISTS seq_id START 1")
    
    # Create sentiment data table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sentiment_data (
            id INTEGER PRIMARY KEY DEFAULT nextval('seq_id'),
            comment_id VARCHAR UNIQUE,
            subreddit VARCHAR,
            author VARCHAR,
            text VARCHAR,
            sentiment_score FLOAT,
            sentiment_label VARCHAR,
            reddit_score INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create daily summary table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_summary (
            date DATE PRIMARY KEY,
            total_comments INTEGER,
            good_count INTEGER,
            bad_count INTEGER,
            neutral_count INTEGER,
            avg_sentiment FLOAT,
            max_sentiment FLOAT,
            min_sentiment FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create indices for faster queries
    conn.execute("CREATE INDEX IF NOT EXISTS idx_sentiment_label ON sentiment_data(sentiment_label)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_subreddit ON sentiment_data(subreddit)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_created_at ON sentiment_data(created_at)")
    
    # Create archive table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sentiment_archive (
            id INTEGER,
            comment_id VARCHAR,
            subreddit VARCHAR,
            author VARCHAR,
            text VARCHAR,
            sentiment_score FLOAT,
            sentiment_label VARCHAR,
            reddit_score INTEGER,
            created_at TIMESTAMP,
            analyzed_at TIMESTAMP,
            archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.close()
    print(f"Database initialized: {db_path}")

if __name__ == "__main__":
    setup_database()
