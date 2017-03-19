import logging
from scrapy.pipelines.files import FileException, FilesPipeline, FSFilesStore, S3FilesStore
from scrapy.http import Request


class AWSS3Pipeline(FilesPipeline):

    def __init__(self, *args, **kwargs):
        super(AWSS3Pipeline, self).__init__(*args, **kwargs)

    def get_media_requests(self, item, info):
        yield Request(item['file_urls'], meta=item)

    def file_path(self, request, response=None, info=None):

        path = request.meta['s3_file_path']

        return path

    def item_completed(self, results, item, info):

        if not results:
            logging.info("*******************ERROR on S3 file upload******************")

        return item
