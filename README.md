#Flask-S3-Direct-Upload

Sets up S3 upload policies for you to directly upload from client side javascript to S3 bypassing your Flask server.


## Setup

Usage is straightforward. Just set the three S3 parameters `S3_UPLOAD_BUCKET`, `S3_UPLOAD_ACCESS_KEY`, and `S3_UPLOAD_SECRET_KEY` in your app config. While the example below reads these from your environment, feel free to choose a method that makes sense for your deployment.

```python
app = Flask(__name__)
app.config['S3_UPLOAD_BUCKET'] = os.environ.get('S3_UPLOAD_BUCKET')
app.config['S3_UPLOAD_ACCESS_KEY'] = os.environ.get('S3_UPLOAD_ACCESS_KEY')
app.config['S3_UPLOAD_SECRET_KEY'] = os.environ.get('S3_UPLOAD_SECRET_KEY')
s3upload = S3UploadPolicy(app)
```

## Usage

Once this is set, you'll automatically have a top level route setup for `/policy`. For instance, in your dev setup, this will likely be:

```
http://localhost:5000/policy
```

This will return a `JSON` blob which can be consumed via your javascript form post.

```json

{
  "AWSAccessKeyId": "<YOURKEY>",
  "expiry": "2014-08-23T12:15:000Z",
  "key": "uploads/user/<generated_code>",
  "policy": "<long_policy_string>",
  "s3Bucket": "<bucket string>",
  "s3BucketUrl": "http://<bucket_url>.s3.amazonaws.com/",
  "signature": "<hash>"
}

```

## AWS

You may have to tweak your AWS CORS policy setup to permit testing via localhost.

```xml

<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
    <CORSRule>
        <AllowedOrigin>*</AllowedOrigin>
        <AllowedMethod>GET</AllowedMethod>
        <AllowedMethod>POST</AllowedMethod>
        <AllowedMethod>PUT</AllowedMethod>
        <AllowedMethod>DELETE</AllowedMethod>
        <AllowedHeader>*</AllowedHeader>
    </CORSRule>
</CORSConfiguration>

</code>

```

In production, you will likely want to place some restrictions on the AllowedOrigin.

## See Also

You may want to use one of the handy [Jquery](http://blueimp.github.io/jQuery-File-Upload/basic-plus.html) or [Angular](http://blueimp.github.io/jQuery-File-Upload/angularjs.html) libraries to handle the direct S3 post.
