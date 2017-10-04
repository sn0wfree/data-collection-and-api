# -*- coding:utf-8 -*-
import urllib2
import sys
import os
import urllib
import random
import time
import datetime
import platform
import gc

import multiprocessing as mp
#-------------------
__version__ = "1.0"
__author__ = "sn0wfree"
#-------------------


def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename


def chunk_report(bytes_so_far, chunk_size, total_size):
    percent = float(bytes_so_far) / total_size
    percent = round(percent * 100, 2)
    sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%)\r" %
                     (bytes_so_far, total_size, percent))

    if bytes_so_far >= total_size:
        sys.stdout.write('\n')


def chunk_read(response, chunk_size=8192, report_hook=chunk_report):
    total_size = int(response.info().getheader('Content-Length').strip())

    bytes_so_far = 0

    while 1:
        chunk = response.read(chunk_size)
        bytes_so_far += len(chunk)

        if not chunk:
            break

        if report_hook:
            report_hook(bytes_so_far, chunk_size, total_size)

    return bytes_so_far


def python_download(url, filename, target_path="default", symbol="UI-friendly", reporthook=chunk_report):
    #global speed
    f = time.time()
    global download_count, total_count
    # if symbol =="UI-friendly":
    #    print "Begin download with urllib"
    # else:
    #    pass
    #--------------
    if target_path == "default":
        target_path = locals_file_path = os.path.split(
            os.path.realpath(__file__))[0]
    else:
        pass

    path_filename = target_path + '/' + filename

    #f = urllib2.urlopen(url)
    # with open("code2.zip", "wb") as code:
    #    code.write(f.read())

    urllib.urlretrieve(url, path_filename, reporthook=reporthook)
    #-----------------

    #speed = time.time() - f


def progress_test(counts, lenfile, speed, w):
    bar_length = 20
    eta = time.time() + w
    precent = counts / float(lenfile)

    ETA = datetime.datetime.fromtimestamp(eta)
    hashes = '#' * int(precent * bar_length)
    spaces = ' ' * (bar_length - len(hashes))
    sys.stdout.write("""\r%d%%|%s|download %d projects|Speed : %.4f |ETA: %s """ % (
        precent * 100, hashes + spaces, counts, speed, ETA))

    #sys.stdout.write("\rthis spider has already read %d projects, speed: %.4f/projects" % (counts,f2-f1))

    #sys.stdout.write("\rPercent: [%s] %d%%,remaining time: %.4f mins"%(hashes + spaces,precent,w))
    sys.stdout.flush()


def import_data(target_year):
    dirs = os.path.split(os.path.realpath(__file__))[0]
    if "Windows" in platform.system():
        target_path = dirs + "\\logfile\\" + target_year + "\\"
        target_txt_file = target_path + "\\" + target_year + ".txt"

    elif "Darwin" in platform.system():
        target_path = dirs + "/logfile/" + target_year + "/"
        target_txt_file = target_path + "/" + target_year + ".txt"
    else:
        target_path = dirs + "/logfile/" + target_year + "/"
        target_txt_file = target_path + "/" + target_year + ".txt"

    target_url = loadingsplit.read_text_file(target_txt_file)
    target_url_a = [ur.split("\n")[0] for ur in target_url]
    return target_url_a, target_path


def transfer_url_and_download(target_url):
    url = 'https://' + target_url
    #urlretrieve(response, filename=None, reporthook=chunk_report)
    #chunk_read(response, report_hook=chunk_report)
    python_download(url, target_path=target_path, symbol="UI-friendly")
    time.sleep(5 * random.random())


if __name__ == '__main__':
    gc.enable()
    global target_path
    global download_count, total_count

    # target_year="2010"
    target_year = raw_input("which year data want to download:")

    download_count = 0

    target_urls, target_path = import_data(target_year)
    downloaded_files = os.listdir(target_path)
    # print target_url[0],type(target_url[0])
    # print target_url[0].split("/")[-1]
    need_downloand_file = []
    for target_url in target_urls:
        filenames = target_url.split("/")[-1]
        if filenames not in downloaded_files:
            need_downloand_file.append(target_url)
        else:
            pass
    total_count = len(need_downloand_file)
    pool = mp.Pool()
    pool.map(transfer_url_and_download, need_downloand_file)

    #response = urllib2.urlopen('https://'+ target_url[0])
