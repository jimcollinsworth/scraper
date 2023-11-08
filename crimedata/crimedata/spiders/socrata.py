''' crawl data from socrata online sources

https://dev.socrata.com/docs/endpoints.html
https://dev.socrata.com/foundry/data.austintexas.gov/fdj4-gpfu

should register for an api app token and pass it in.

'''


import scrapy
from pathlib import Path
import logging as log

class SocrataSpider(scrapy.Spider):
    name = "socrata"
    urls = {
        #"https://data.nashville.gov/api/views/2u6v-ujjs/rows.csv?date=20231107&accessType=DOWNLOAD": "nashville-tn-city-incidents",
        #"https://data.memphistn.gov/api/views/ybsi-jur4/rows.csv?date=20231107&accessType=DOWNLOAD": "memphis-tn-city-incidents",
        "https://data.hartford.gov/api/views/w8n8-xfuk/rows.csv?date=20231107&accessType=DOWNLOAD": "hartford-ct-city-incidents",
        "https://data.kcmo.org/api/views/bfyq-5nh6/rows.csv?date=20231107&accessType=DOWNLOAD": "kansas-city-mo-city-incidents",
        "https://data.littlerock.gov/api/views/bz82-34ep/rows.csv?date=20231107&accessType=DOWNLOAD": "littlerock-ak-city-incidents",
    }

    def start_requests(self):
        
        for url in [k for k,v in self.urls.items()]:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        name = self.urls[response.url]
        filename = f"socrata-{name}.csv"
        Path(filename).write_text(response.text)
        log.info(f"Saved file {filename}")
        

