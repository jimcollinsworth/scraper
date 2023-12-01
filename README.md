#TODO spider ends after too many timeouts, need to ignore/return item tried DontCloseSpider https://docs.scrapy.org/en/latest/topics/exceptions.html
#TODO fallback to root domain crawl if url not found
#TODO make multiple requests but merge into single item (like a sub-crawl)


# scraper
*bookmark web scraper*

Crawls URLs from a list of browser bookmarks to gather metadata and other information useful for site categorization. Support a number of different spiders/options such as metadata, shallow, deep crawls, links vs text/content.

Help cleanup bookmark lists-bad domains, missing pages, etc. Could search for internet archive page. Classify all the urls with status and crawl result so user can filter later and re-import clean lists back into their browser.

Track the url status, some will fail, retry. or redirect to another domain. Maybe url fails but domain is good. Record this so the next crawl they get filtered.

Besides crawling the urls themselves, we can can also look them up in archive, search, directory, categorization sites such as google or commoncrawl.org.Want to build useful knowledge nets of my bookmarks, identify authorative vs biased sites and much more. 

Feed this KN back into the browser, first as an import file that has resorted/re-categorized bookmarks (static use-case), and next as a browser extension with dynamic updating and resorting.

Retrieve metadata for the crawled content, as well as any usage requirements.
Pull down terms and use, store and version it. This information will all be available for users of the real-time dashboard, so they can see detailed sourcing information.

Some sites suggest a token for access. Per researcher guidelines we should identify ourselves/NORC when scraping.

Scrapy for framework - Python, enables lots of functionality out of the box, scales from individual use to large cloud easily, good plugin ecosystem with multiple javascript engines available.

**input meta data**
 - bookmark url exported file

**tasks**
 - output file names - override
 - common jsonl output for all spiders (only ever append)

 **spiders**
  - bookmark-meta - get basic info about the URL, record status. Try domain only too, or maybe first.  
  - bookmark-links
  - bookmark-content

**pipelines**
Do some post processing on results, make use of LLMs for summarization/categorization/parsing. Use local LLM.
Rely on http caching so we aren't necessarily downloading data every time.

**monitoring**
Want to see activity of crawler for development and operations; domain/urls, status, size, messages, times, errors.
Options include:
  - console log - INFO->DEBUG level output, should use 'key=value, key=value' for important info, this can be read by Rundeck for automation or a dashboard for reporting and monitoring. [?python dashboard/monitoring solution]
  - items.json - one line per request, can contain all data or just meta.
  - scrapy API - run crawler as process, automate with scrapyd.

**db/file store**
How about a DuckDB/JSON/Pickled for both input (URLS..) and output (metadata, features, text, image), where retrieved data and subsequent calculated/inferred features can be added incrementally. Local db/files are easy to manage, can be versioned, and efficient. Default process could create new data on output, with an --inplace option to update the input file. Use pandas as the input/output layer, and we can support many file formats familiar to data scientists easily.

With this workflow the user can iterate crawling and cleaning up the list of bookmarks (and fixing code). Each time more bookmarks get sucessfully processed, and then filted out on the next crawl.
The db/file stores the status/timestamp and other results of the last crawl. This file can be versioned with git or other tech.

