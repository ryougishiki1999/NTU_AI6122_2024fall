# How to use the search engine

## Introduction

The search engine is running based on Command Line Interface (CLI). It integrates the **normal query search** and **subtasks** including data analysis, review_summary and application in discovering "comparision sentence"

The search engine is desinged to be user-friendly and easy to use. You can follow the `intro` and `prompt` to use the search engine. Besides, you can also use the `help` or `?` command to get the detailed information of all commands.

## Specific formats of normal query search

There are there types of normal query search supported rightnow. (Future work may include more types of search)

Every type of search query must have at least one corresponding fieldname.

fieldname and filedvalue must be separated by `:`

there is must be a `,` between every fieldname

### Keyword search of Business

support search fieldnames: `name`, `categories`

example:

```
business name:abby, the catgories: traditional medical
```

### Keyword search of Review

support search fieldnames: `text`

example:

```
reviews text: delicious burger
```

### Geospatial search of Business locations

support search fieldnames:`latitude`, `longitude`
there must be `/` between min and max value of latitude and longitude (there is no matter of the order of min and max)

example:

```
latitude: 34/36, longitude: -118/-120
```

## For 3.5 App section

You'd better to run:
```
python -m spacy download en_core_web_sm
```
to install spacy model.