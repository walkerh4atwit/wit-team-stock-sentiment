CREATE SEQUENCE articles_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE queue_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE sectors_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE tickers_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE articletickers_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE marketsentiment_seq START WITH 1 INCREMENT BY 1;


CREATE TABLE Articles (
    id NUMBER PRIMARY KEY,
    title VARCHAR2(255) NOT NULL,
    url VARCHAR2(255) NOT NULL,
    summary CLOB,
    date_published TIMESTAMP
);

CREATE TABLE Sectors (
    id NUMBER PRIMARY KEY,
    name VARCHAR2(255) NOT NULL,
    sentiment_score FLOAT
);

CREATE TABLE Tickers (
    id NUMBER PRIMARY KEY,
    ticker VARCHAR2(10) NOT NULL,
    company_name VARCHAR2(255),
    sector_id NUMBER,
    sentiment_score FLOAT,
    FOREIGN KEY (sector_id) REFERENCES Sectors(id)
);

CREATE TABLE ArticleTickers (
    id NUMBER PRIMARY KEY,
    article_id NUMBER NOT NULL,
    ticker_id NUMBER NOT NULL,
    sentiment_score FLOAT,
    FOREIGN KEY (article_id) REFERENCES Articles(id),
    FOREIGN KEY (ticker_id) REFERENCES Tickers(id)
);








CREATE OR REPLACE TRIGGER articles_bir
BEFORE INSERT ON Articles
FOR EACH ROW
BEGIN
    SELECT articles_seq.NEXTVAL INTO :new.id FROM dual;
END;
/

CREATE OR REPLACE TRIGGER queue_bir
BEFORE INSERT ON Queue
FOR EACH ROW
BEGIN
    SELECT queue_seq.NEXTVAL INTO :new.id FROM dual;
END;
/

CREATE OR REPLACE TRIGGER sectors_bir
BEFORE INSERT ON Sectors
FOR EACH ROW
BEGIN
    SELECT sectors_seq.NEXTVAL INTO :new.id FROM dual;
END;
/

CREATE OR REPLACE TRIGGER tickers_bir
BEFORE INSERT ON Tickers
FOR EACH ROW
BEGIN
    SELECT tickers_seq.NEXTVAL INTO :new.id FROM dual;
END;
/

CREATE OR REPLACE TRIGGER articletickers_bir
BEFORE INSERT ON ArticleTickers
FOR EACH ROW
BEGIN
    SELECT articletickers_seq.NEXTVAL INTO :new.id FROM dual;
END;
/

CREATE OR REPLACE TRIGGER marketsentiment_bir
BEFORE INSERT ON MarketSentiment
FOR EACH ROW
BEGIN
    SELECT marketsentiment_seq.NEXTVAL INTO :new.id FROM dual;
END;
/