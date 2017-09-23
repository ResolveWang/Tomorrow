[![Build Status](https://travis-ci.org/ResolveWang/Tomorrow.svg?branch=master)](https://travis-ci.org/ResolveWang/Tomorrow)

# Tomorrow
**Magic decorator syntax for asynchronous code in Python 3.**


**Please don't actually use this in production.  It's more of a thought experiment than anything else, and relies heavily on behavior specific to Python's old style classes.  Pull requests, issues, comments and suggestions welcome.**

Installation
------------

Tomorrow is conveniently available via pip:
```
pip install tomorrow
```

or installable via `git clone` and `setup.py`
```
git clone https://github.com/ResolveWang/Tomorrow.git
sudo python setup.py install
```

To ensure Tomorrow is properly installed, you can run the unittest suite from the project root:
```
nosetests -v 
```

Usage
-----
The tomorrow library enables you to utilize the benefits of multi-threading with minimal concern about the implementation details.

Behind the scenes, the library is a thin wrapper around the `Future` object in `concurrent.futures` that resolves the `Future` whenever you try to access any of its attributes.

Enough of the implementation details, let's take a look at how simple it is to speed up an inefficient chunk of blocking code with minimal effort.


Naive Web Scraper
-----------------
You've collected a list of urls and are looking to download the HTML of the lot.  The following is a perfectly reasonable first stab at solving the task.

For the following examples, we'll be using the top sites from the Alexa rankings.

```python
urls = [
    'http://baidu.com',
    'http://python.org',
    'http://github.com',
    'http://bing.com',
    'http://yahoo.com',
]
```

Right then, let's get on to the code.

```python
import time
import requests

def download(url):
    return requests.get(url)

if __name__ == "__main__":

    start = time.time()
    responses = [download(url) for url in urls]
    html = [response.text for response in responses]
    end = time.time()
    print("Time: %f seconds" % (end - start))
```

More Efficient Web Scraper
--------------------------

Using tomorrow's decorator syntax, we can define a function that executes in multiple threads.  Individual calls to `download` are non-blocking, but we can largely ignore this fact and write code identically to how we would in a synchronous paradigm. 

```python
import time
import requests

from tomorrow import threads

@threads(5, run_mode='sync')
def download(url):
    return requests.get(url)

@threads(5, run_mode='async')
def gdownload(url):
    return requests.get(url)

if __name__ == "__main__":
    start = time.time()
    responses = [download(url) for url in urls]
    html = [response.res.text for response in responses]
    end = time.time()
    print("Multi thread running time: %f seconds" % (end - start))

    start = time.time()
    responses = [gdownload(url) for url in urls]
    html = [response.res.text for response in responses]
    end = time.time()
    print("Time: %f seconds" % (end - start))

```

Awesome!  With a single line of additional code (and no explicit threading logic) we can now download websites ~10x as efficiently.But note that it has side effects.The result that the function returns is the tomorrow obj.In order to get the result,
we need to get the `res` attr.

The program will run with multithread in 'sync' mode, while in 'async' mode, it will run with gevent.

You can also optionally pass in a timeout argument, to prevent hanging on a task that is not guaranteed to return.

```python
import time

from tomorrow import threads

@threads(1, timeout=0.1)
def raises_timeout_error():
    time.sleep(1)

if __name__ == "__main__":
    print(raises_timeout_error().res)
```

How Does it Work?
-----------------

Feel free to read the source for a peek behind the scenes -- it's less than 100 lines of code.
