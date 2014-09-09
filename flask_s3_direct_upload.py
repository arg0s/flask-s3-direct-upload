# -*- coding: utf-8 -*-
from flask import current_app, jsonify
from json import dumps
import pdb
import os
from base64 import b64encode
import hmac
try:
    import hashlib
except ImportError:
    import md5
    import sha
from uuid import uuid4
import arrow

# Find the stack on which we want to store the database connection.
# Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# before that we need to use the _request_ctx_stack.
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


def conf(key):
  # Shortcut for grabbing current app conf
  return current_app.config.get(key)

def verify_config(l, d):
  # Shortcut for checking a list of keys against the app config dictionary
  # to see if all required parameters have been set in the app config
  k = d.keys()
  m = list(set(l)-set(k))
  return len(m)>0, m

class S3UploadPolicy(object):

    # List of app config parameters that need to be set if the extension is being used
    req_keys = ['S3_UPLOAD_BUCKET', 'S3_UPLOAD_SECRET_KEY', 'S3_UPLOAD_ACCESS_KEY']


    def _policy(self):
      def make_policy():
          arw = arrow.utcnow() # "2009-01-01T00:00:00Z" "2013-02-08T09:30:26 Z"
          sExpiry = "{0}000Z".format(arw.replace(hours=+1).format('YYYY-MM-DDTHH:mm:'))
          policy_object = {
              "expiration": sExpiry,
              "conditions": [
                  { "bucket": "{0}".format(conf('S3_UPLOAD_BUCKET'))},
                  [ "starts-with", "$key", "uploads/user/"],
                  [ "starts-with", "$Content-Type", "image/"],
                  [ "content-length-range", 1, 5242880 ]
              ]
          }
          return b64encode(dumps(policy_object).replace('\n', '').replace('\r', '')) , sExpiry

      def sign_policy(policy):
          return b64encode(hmac.new(conf('S3_UPLOAD_SECRET_KEY'), policy, sha).digest())

      policy , sExpiry = make_policy()
      return jsonify({
          "s3BucketUrl":"http://{0}.s3.amazonaws.com/".format(conf('S3_UPLOAD_BUCKET')),
          "s3Bucket":"{0}".format(conf('S3_UPLOAD_BUCKET')),
          "AWSAccessKeyId":conf('S3_UPLOAD_ACCESS_KEY'),
          "policy": policy,
          "expiry": sExpiry,
          "signature": sign_policy(policy),
          "key": "uploads/user/" + uuid4().hex + ""
      })


    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):

        class S3UploadPolicyError(Exception):
          # Class exception that gets raised if the req_keys are not all set
          pass


        # Use the newstyle teardown_appcontext if it's available,
        # otherwise fall back to the request context
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)
        invalid, items = verify_config(self.req_keys, app.config)
        if invalid:
          raise S3UploadPolicyError('S3UploadPolicy configuration is incomplete: Check the settings of %s' % ','.join(items))
        app.add_url_rule('/policy', 'policy', self._policy)

    def teardown(self, exception):
        ctx = stack.top
