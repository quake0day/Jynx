
import urllib,time

import requests
for i in xrange(2, 152):
    url = URL = 'http://pokemongo.gamepress.gg/sites/default/files/styles/pokemon_small/public/2016-07/'+str(i)+".png"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    response = requests.get(url, headers=headers)


    f = open("./thumbnail/"+str(i)+'.png','wb')
    
    f.write(response.content)
    f.close()
    time.sleep(1)