import csv
import os
import tarfile

import boto3

from plenario.settings import S3_BUCKET
from plenario.tasks import archive
from tests import BaseTest


class TestArchive(BaseTest):

    # TODO(heyzoos)
    # Need a way to test /archive without calling out to AWS S3, as this seems
    # to fail when builds are running for non-urbanccd forks.
    def test_archive(self):

        archive('2017-01')

        s3 = boto3.client('s3')
        with open('test.tar.gz', 'wb') as file:
            s3.download_fileobj(S3_BUCKET, '2017-1/node0.tar.gz', file)

        tar = tarfile.open('test.tar.gz')
        tar.extractall()

        with open('node0.temperature.2017-01-01.2017-02-01.csv') as file:
            count = 0
            reader = csv.reader(file)
            for line in reader:
                count += 1
            # 31 records plus the header!
            self.assertEquals(count, 32)

        tar.close()

        os.remove('test.tar.gz')
        os.remove('node0.temperature.2017-01-01.2017-02-01.csv')
