# scraper
*crimedata web scraper*

Retrieve metadata for the crawled content, as well as any usage requirements.
Pull down terms and use, store and version it. This information will all be available for users of the real time dashboard, so they can see detailed sourcing information.
Some sites suggest a token for access. Per researcher guidelines we should identify ourselves/NORC when scraping.

Scrapy for framework - Python, enables lots of functionality out of the box, scales from individual use to large cloud easily, good plugin ecosystem with multiple javascript engines available.

Use the XLS file directly for driving the scraper, will get list of urls with IDs and other metadata from the XLS file:Crime data_Web Scraping_2023sept18.xlsx
**input meta data**
 - Type - crime-incidents
 - URL ID - memphis-city-ky
 - root URL - https://maps.cityofmadison.com/arcgis/rest/services/Public/OPEN_DB_TABLES/MapServer/2/    (the crawler might append something like query?where=1%3D1&outFields=%2A&outSR=4326&f=json)
 - crawler ID - arcgis-api, socrata-api, arcgis-table-ux.....

**tasks**
 - output file names - override
 - common jsonl output for all spiders (only ever append)

 **spiders**
  - arcgis-api - targets the arcgis cloud API, can get full JSON feature files. This is the data as loaded into the mapping system, and has geodata such as extents. Might be missing fields available in the CSV/Tables.
        - API docs https://developers.arcgis.com/rest/services-reference/enterprise/get-started-with-the-services-directory.htm
  - socrata-api - API docs from city of austin site https://dev.socrata.com/foundry/data.austintexas.gov/fdj4-gpfu
  - arcgis-table-ux - uses the arcgis cloud table UX to filter data, prepare downloads, wait and download CSV data. More complicated but can be very selective and efficient in the filtering.

