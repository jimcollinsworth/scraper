from pathlib import Path
import json
import scrapy
import urllib.parse

class ArcgisItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
    url = scrapy.Field()
    status = scrapy.Field()

class ArcgisAPISpider(scrapy.Spider):
    name = "arcgisapi"
    urls = {
        "https://maps.cityofmadison.com/arcgis/rest/services/Public/OPEN_DB_TABLES/MapServer/2/query?where=1%3D1&outFields=%2A&outSR=4326&f=json": "madison-wi-city-incidents",
        "https://services.arcgis.com/v400IkDOw1ad7Yad/arcgis/rest/services/Police_Incidents/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json": "what-city-incidents",
        "https://services1.arcgis.com/79UxTxnBeBW8JHY4/arcgis/rest/services/Aurora_IL_Police_Crime_Stats/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json": "aurora-il-city-incidents",
        "https://webgis2.durhamnc.gov/server/rest/services/PublicServices/Tables/MapServer/4/query?where=1%3D1&outFields=%2A&outSR=4326&f=json": "nc-durham-city-incidents",
        "https://services1.arcgis.com/79kfd2K6fskCAkyg/arcgis/rest/services/2023CrimeData_OpenData/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json": "louisville-ky-metro-incidents",
        "https://services1.arcgis.com/9meaaHE3uiba0zr8/arcgis/rest/services/District_Council_4_-_Daytons_Bluff_-_Crime_Incidents/FeatureServer/0/query?where=1%3D1&outFields=%2A&outSR=4326&f=json": "st-paul-dc4-incidents"
    }

    def start_requests(self):
        for url in [k for k,v in self.urls.items()]:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = ArcgisItem()

        item['status'] = response.status
        item['url'] = response.url

        # save file name to download
        item['file_urls'] = [response.url]
        
        yield item

        
