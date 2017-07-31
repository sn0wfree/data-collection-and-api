import webbrowser
import time


def re(f):
    u = []
    with open(f, 'r') as urls:
        urls = urls.readlines()
        for url in urls:
            u.append(url.strip())
    return u


def count(i):
    if i <= 10:
        i = i + 1
        return i
    else:
        time.sleep(1)

        return 0


if __name__ == '__main__':
    c = webbrowser.get('safari')
    urlpath = '/Users/sn0wfree/Documents/python_projects/data_collection/API/Google_trend/urls.txt'
    urls = re(urlpath)
    counts = 0
    for url in urls:
        c.open(url)
        counts = count(counts)

        time.sleep(0.5)
