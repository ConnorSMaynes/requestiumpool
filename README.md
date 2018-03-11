# Requestium Pool
#### Requestium ( requests + selenium + parsel )
#### Pooling

![Requestium](https://user-images.githubusercontent.com/14966348/32966130-8bb15b00-cbb7-11e7-9faf-85963ec5bd82.png)
![Selenium](http://selenium-python.readthedocs.io/_static/logo.png)

Very simple pooling scheme for working with multiple requestium Sessions. Reduce your time costs when running multiple sessions, while sticking to a number of instances you know your machine can handle.

## Methods

- `acquire()` : get a requestium Session. Sessions are built on demand, meaning that none will be created until they are requested. If pool maxed out and all Sessions are being used, ``acquire_wait_timeout`` sets how long you will wait for a free Session before giving up. 
- `release` : release the Session and return it to the pool, so that other processes can use it.
- `destroy` : destroy the Session you pass to it.
- `stop` : kill all Sessions. Multithreaded.

## Installation

```bash
pip install requestiumpool
```

or

```bash
pip install git+git://github.com/ConnorSMaynes/requestiumpool
```

## Usage

```python
from threading import Thread
from requestiumpool import RequestiumPool

requestium_args = {
    'webdriver_path' : DRIVER_PATH
    ,'browser':BROWSER_NAME
    ,'default_timeout':15
    }
# for headless -> 'webdriver_options':{'arguments':['headless'] }

RPool = RequestiumPool( requestium_args, pool_size=2 )

def acquireAndFollow( url ):
    R = RPool.acquire(60)
    if R != None:
        print(url)
        R.driver.get( url )
        RPool.release( R )
    else:
        print( R )           # print None if no browser acquired within timeout

URLs = [ 'https://www.google.com/', 
            'https://www.stackoverflow.com/', 
            'https://www.github.com/' ]
threads = []
for i in range( 5 ):        
    for url in URLs:
        t = Thread( target=acquireAndFollow, args=(url,) )
        threads.append(t)
        t.start()

for t in threads:           # wait for all urls to be visited
    t.join()

RPool.stop()                # kill all requestium instances
```

### NOTES

    stop() is multithreaded, but it can take a while with a lot of instances.
    By reusing browsers that are already open, you can significantly reduce time costs.

## Similar Projects

This project was inspired by another project,
[Webdriver Pool](https://github.com/Jiramew/webdriver_pool), but for the requestium wrapping around [Requests](https://github.com/requests/requests), [Selenium](https://github.com/SeleniumHQ/selenium), and [Parsel](https://github.com/scrapy/parsel).

## License

Copyright © 2018, [ConnorSMaynes](https://github.com/ConnorSMaynes). Released under the [MIT](https://github.com/ConnorSMaynes/requestiumpool/blob/master/LICENSE).