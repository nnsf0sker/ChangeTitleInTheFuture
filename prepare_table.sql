CREATE DATABASE IF NOT EXISTS youtube_parsed_items_database;

CREATE TABLE IF NOT EXISTS youtube_parsed_items_database.youtube_parsed_items_table (
    video_id VARCHAR(11) PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    author_id VARCHAR(24),
    views DECIMAL(11, 0) UNSIGNED NOT NULL,
    comments DECIMAL(11, 0) UNSIGNED,
    date VARCHAR(48),
    likes DECIMAL(11, 0) UNSIGNED,
    dislikes DECIMAL(11, 0) UNSIGNED,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);