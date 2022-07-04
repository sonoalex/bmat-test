
import os
import requests

def main(filename, url):

    content_path = os.path.abspath(filename)

    f = open(content_path, 'rb')
    headers = {}

    file = {'file': f}
    try:
        r = requests.put(url+filename, files=file, headers=headers)
        print(r.json())

    except Exception as e:
        print(str(e))
    
if __name__ == '__main__':
    url = 'http://127.0.0.1:8000/task/upload/'
    main('test_upload.csv', url)
