# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import logging as log

class JsonlWriterPipeline:
    # writes the item metadata out to a JSONL file, the key difference being there is no array, its just one object per line.
    # makes it easy to append to and don't have to worry about closing. For safety the crawlers will only ever append to this file.
    def open_spider(self, spider):
        #TODO make the file location configurable through command line.
        self.file = open("items.jsonl", "a")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        #line = json.dumps(ItemAdapter(item).asdict(), indent=4) + "\n"
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item


from scrapy.pipelines.files import FilesPipeline

class CrimeDataFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        media_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        media_ext = Path(request.url).suffix
        # Handles empty and wild extensions by trying to guess the
        # mime type then extension or default to empty string otherwise
        if media_ext not in mimetypes.types_map:
            media_ext = ""
            media_type = mimetypes.guess_type(request.url)[0]
            if media_type:
                media_ext = mimetypes.guess_extension(media_type)
        return f"full/{media_guid}{media_ext}"
