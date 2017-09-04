#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多线程爬取电影天堂最新电影列表

1.电影列表地址：'http://www.ygdy8.net/html/gndy/dyzz/list_23_{0}.html'.format(str(page))
2.电影详情地址：从上面网址中截取
3.访问详情地址，提取电影信息

"""
import os
import threading
import time
from queue import Queue

import requests

from me.lonny.logger import get_logger
from me.lonny.re_utils import *

logger = get_logger('movie', 'debug.log')


class Spider(threading.Thread):
    """
    1.从输入队列中提取电影详情url请求并提取有效信息
    2.将有效信息放入输出队列中供输出线程记录
    """

    def __init__(self, in_queue, out_queue):
        super(Spider, self).__init__()
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        while True:
            if self.in_queue.empty():
                logger.debug('in_queue empty.{0} exiting...'.format(threading.current_thread().getName()))
                break
            else:
                url = self.in_queue.get()

            if url:
                result = Spider.process(url)
                self.out_queue.put(result)

    @staticmethod
    def process(url):
        html = do_request(url.strip())
        return extract_details(html)


class Writer(threading.Thread):
    """
    输出线程：不断从队列中取出处理完的信息并记录到文件
             直到取到的元素为退出标识为止
    """
    __exit = True

    def __init__(self, queue, filename):
        super(Writer, self).__init__()
        self.queue = queue
        self.filename = filename

    def stop(self):
        self.queue.put(self.__exit)

    def run(self):
        with open(self.filename, 'wb') as f:
            while True:
                data = self.queue.get()
                if not data:
                    continue
                if data is self.__exit:
                    break
                f.write(data.encode('utf8'))
                logger.debug('write file:{0}'.format(data))


def do_request(url):
    logger.debug('request url:{0}'.format(url))
    try:
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Host": "www.ygdy8.net",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"
        }
        resp = requests.get(url, headers=headers, timeout=10)
        resp.encoding = 'gb18030'
        logger.debug('status code:{0}'.format(resp.status_code))
        return resp.text
    except requests.exceptions.RequestException as e:
        logger.debug('{0}:request exception {1}'.format(url, e.response))
        return ''


# 提取影片url
def fetch_movie_urls(filename):
    if not os.path.isfile(filename):
        with open(filename, 'w') as file_url:
            base_url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_{0}.html'
            for page in range(1, 165):
                html = do_request(base_url.format(str(page)))
                urls = extract_urls(html)
                file_url.write(urls)


# 入口
def main():
    directory = 'data'
    if not os.path.isdir(directory):
        os.makedirs(directory)
    # 电影地址文件
    path_urls = os.path.join(directory, 'movie_urls.txt')
    # 电影详情文件
    path_movies = os.path.join(directory, 'movies.txt')

    # 主线程爬取电影地址
    fetch_movie_urls(path_urls)

    # 多线程爬取电影详情
    start = time.time()
    in_queue = Queue()
    out_queue = Queue()
    with open(path_urls, 'r') as f:
        lines = f.readlines()
        for line in lines:
            in_queue.put(line)

    # 启动记录线程
    writer = Writer(out_queue, filename=path_movies)
    writer.start()

    # 启动爬虫线程
    spiders = [Spider(in_queue, out_queue) for i in range(20)]
    for s in spiders:
        s.start()
    for s in spiders:
        s.join()

    # 爬虫线程结束，向输出线程发出结束信号
    writer.stop()
    writer.join()

    logger.debug('all done({0}s).'.format(time.time() - start))


if __name__ == '__main__':
    main()
