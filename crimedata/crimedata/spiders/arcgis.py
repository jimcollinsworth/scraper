from pathlib import Path
import json
import scrapy


class ArcgisSpider(scrapy.Spider):
    name = "arcgis"

    def start_requests(self):
        urls = [
            "https://services1.arcgis.com/79UxTxnBeBW8JHY4/arcgis/rest/services/AuroraIL.Police_Incidents/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json",
            "https://webgis2.durhamnc.gov/server/rest/services/PublicServices/Tables/MapServer/4/query?where=1%3D1&outFields=*&outSR=4326&f=json",
            "https://maps.cityofmadison.com/arcgis/rest/services/Public/OPEN_DB_TABLES/MapServer/2/query?where=1%3D1&outFields=*&outSR=4326&f=json",
            "https://services.arcgis.com/v400IkDOw1ad7Yad/arcgis/rest/services/Police_Incidents/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.log("------------------")
        self.log(dir(response))
        domain = response.url.split("//")[-1].split("/")[0]
        name = domain.replace(".", "-")
        filename = f"arcgis-{name}.json"
        Path(filename).write_text(json.dumps(response.json(), indent=4))
        self.log(f"Saved file {filename}")
        
