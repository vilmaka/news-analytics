# news-analytics
This project focuses on AI-based analytics of news articles. Code is written in python and hosted in Azure using functions.

Technology stack: Azure functions, OpenAI API, Blob storage, PostgreSQL

![alt text](https://github.com/vilmaka/news-analytics/blob/main/architecture.png?)

## Web scraper
In the first stage of this project, the web scraper fetches news articles only from Yle.fi. Scraper is divided into two parts: one timed function to find the articles to download and a queue-function to fetch, parse and save the content. This is for two reasons:
- Queue-trigger enables better control of the pipeline: we can have automated process to enqueue new articles, another process to add old articles and also insert items manually in the development phase
- In case of errors, it's easy to identify and investigate the failed items and also re-run them from the poison-queue

## Analytics
The first step of the analysis is to filter out articles like columns or opinions, as the interest is on the news. Then, the remaining items are scheduled for analytics tasks. Scheduling is required as Azure OpenAI API has an hourly token limit that cannot be exceeded.

The first goal is to calculate the "positivity index" for news on a scale from 1 to 5. For example, utilizing this metric it would be possible to determine if the share of negative news has increased over time, and show statistics like "The worst news of the week".

## Visualization
This is not the main focus of the project, but the aim is to share the results publicly.

