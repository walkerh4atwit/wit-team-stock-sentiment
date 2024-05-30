CREATE DATABASE IF NOT EXISTS StockSentiment;

USE StockSentiment;

CREATE TABLE Articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    url VARCHAR(255) NOT NULL,
    summary TEXT,
    date_published DATETIME,
    date_processed DATETIME
);

CREATE TABLE Queue (
    id INT AUTO_INCREMENT PRIMARY KEY,
    article_id INT NOT NULL,
    date_added DATETIME,
    FOREIGN KEY (article_id) REFERENCES Articles(id)
);

CREATE TABLE Sectors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sentiment_score FLOAT
);

CREATE TABLE Tickers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    company_name VARCHAR(255),
    sector_id INT,
    sentiment_score FLOAT,
    FOREIGN KEY (sector_id) REFERENCES Sectors(id)
);

CREATE TABLE ArticleTickers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    article_id INT NOT NULL,
    ticker_id INT NOT NULL,
    sentiment_score FLOAT,
    FOREIGN KEY (article_id) REFERENCES Articles(id),
    FOREIGN KEY (ticker_id) REFERENCES Tickers(id)
);

CREATE TABLE MarketSentiment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    sentiment_score FLOAT,
    sector_id INT,
    FOREIGN KEY (sector_id) REFERENCES Sectors(id)
);
