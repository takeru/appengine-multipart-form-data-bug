#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import webapp2
import logging
import os
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from google.appengine.api import images


logging.getLogger().setLevel(logging.DEBUG)
def log(s):
    logging.info("\n********\n"+s+"\n********")

class MyHandler(blobstore_handlers.BlobstoreUploadHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/')

        html = '''
<html>
<body>
<form action="%s" method="post" enctype="multipart/form-data">
  <input type="text" name="text1" value="あいうえお">
  <input type="file" name="file1">
  <input type="submit" name="submit1">
</form>
</body>
</html>
''' % (upload_url)

        self.response.out.write(html)

    def post(self):
        text1 = self.request.get("text1")

        # workaround. http://code.google.com/p/googleappengine/issues/detail?id=2749#c58
        upload_files_bug = self.get_uploads('file1')
        upload_files = blobstore.BlobInfo.get([blob.key() for blob in upload_files_bug])

        if len(upload_files)==0:
            self.response.out.write("len(upload_files)=" + str(len(upload_files)))
            return
        blob_info = upload_files[0]

        html = """
<html>
<body>
  sys.getdefaultencoding()=[%s]
  text1=[%s]
  file1=[%s] <img src="%s">
</body>
</html>
""" % (sys.getdefaultencoding(),
       text1,
       blob_info.filename,
       "/blob?key=%s" % (blob_info.key()))

        self.response.out.write(html)

class BlobHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        blob_key = self.request.get("key")
        if not blobstore.get(blob_key):
            self.error(404)
        else:
            self.send_blob(blob_key)


app = webapp2.WSGIApplication([
        ('/',            MyHandler),
        ('/blob',        BlobHandler),
        ], debug=True, config={})

