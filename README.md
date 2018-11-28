## How to deploy:

```
virtualenv run

source run/bin/activate

pip install -r requirements.txt

python main.py
```

## API URLS:

***GET /file_info/<file_id>***

_Get JSON with file_information:_
```
{
    "fileName": "dby40pu-05981e7e-cdce-45fc-ae7f-490c9864ce34.jpg",
    "type": "image/jpeg",
    "fileId": "3f61cf85ced54f89b39e3a8ebc4f7cfd"
}
```

***GET /file_info***

_Get JSON with all files information_
```
[
  {
    "fileName": "dby40pu-05981e7e-cdce-45fc-ae7f-490c9864ce34.jpg",
    "type": "image/jpeg",
    "fileId": "3f61cf85ced54f89b39e3a8ebc4f7cfd"
  },
  {
    "fileName": "photo_2018-11-01_13-14-50.jpg",
    "type": "image/jpeg",
    "fileId": "9677daefd0c84b7fbdf5038315b7511f"
  }
]
```

***POST /upload_file***

_Endpoint for file upload form_
_Returns file info JSON_

***GET /file/<file_name>***

_Endpoint for serving files by name_
