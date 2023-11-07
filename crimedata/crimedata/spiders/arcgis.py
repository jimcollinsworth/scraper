from pathlib import Path
import json
import scrapy


class ArcgisSpider(scrapy.Spider):
    name = "arcgis"
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
        #TODO for each main url, we want to save the metadata too, so create a couple urls
        # not in parse?
        # + /query?where=1%3D1&outFields=*&outSR=4326&f=json 
        # write the query parameters out to the json too
        # as is for meta, get date updated and other info, add it to the output json
        #TODO name files based on city, then keyword/function, then file type extension this will come from the csv that drives the process
        name = self.urls[response.url]
        filename = f"arcgis-{name}.json"
        Path(filename).write_text(json.dumps(response.json(), indent=4))
        self.log(f"Saved file {filename}")
        
