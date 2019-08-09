import matplotlib.pyplot as plt
import requests
import urllib.request
from IPython.core.debugger import Tracer

url_form = "https://conferences.ieee.org/conferences_events/conferences/search?q=*&subsequent_q=&date=all&from=&to=&region=all&country=all&pos={0}&sortorder=asc&sponsor=&sponsor_type=all&state=all&field_of_interest=all&sortfield=dates&searchmode=basic"
DATA_DIR = './data/html/'

if __name__ == '__main__':
    for i in range(1691, 1948):
        url = url_form.format(i)
        handle = urllib.request.urlopen(url)
        html = handle.read()
        html = html.decode('utf8')
        #r = requests.get(url)
        fname = "{data_dir}/{page}.html".format(data_dir=DATA_DIR,page=str(i))
        with open(fname, 'wb') as f:
            f.write(html.encode('UTF-8'))
        print("getting {0}...".format(i))
