#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
用Python实现的书签分类器
http://www.jianshu.com/p/7041b812e811
'''

import json
import re
import codecs

# the classifier of bookmarks
def classify(list_link, type_dict, category_dict):
    # init list
    list_link_new = [[] for i in range(len(type_dict))]
    for domain, link, text in list_link:
        if domain not in category_dict:
            cate = 'other'
        else:
            cate = category_dict[domain]
        link_item_new = (link, text)
        list_link_new[type_dict[cate]].append(link_item_new)
    # print('classify:' + str(len(link_list_new)))
    return list_link_new

# read the original bookmarks html, filter the link and text of <a>
def analysis_bookmarks(html):
    # init list
    list_link = []
    with codecs.open(html, 'r', 'UTF-8') as f_origin:
        lines = re.findall('<DT>(.*?)<DT>', f_origin.read(), re.S)
        # print('Total:' + str(len(lines)))
        for line in lines:
            domain = re.findall('://[a-zA-Z0-9]*\.(.*?)\.', line, re.S)
            link = re.findall('HREF="(.*?)"', line, re.S)
            text = re.findall('">(.*?)</A>', line, re.S)
            if len(domain) > 0 and len(link) > 0 and len(text) > 0:
                link_item = (domain[0], link[0], text[0])
                # print(link_item)
                list_link.append(link_item)
        # print('Filter:' + str(len(link_list)))
    return list_link

# write the results to a new bookmarks html
def create_new_html(html_new, link_list_new, type_dict):
    # reverse the dict above
    type_dict_reverse = dict(zip(type_dict.values(), type_dict.keys()))
    with codecs.open(html_new, 'w', 'UTF-8') as f_new:
        group = '<!DOCTYPE NETSCAPE-Bookmark-file-1>\n' \
                + '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n' \
                + '<TITLE>Bookmarks</TITLE>\n' \
                + '<H1>Bookmarks</H1>\n' \
                + '<DL><p>\n'
        for i, item in enumerate(link_list_new):
            group += '\t<DT><H3 ADD_DATE="" LAST_MODIFIED="">' + \
                     type_dict_reverse[i] + '</H3>\n\t<DL><p>\n'
            for j in item:
                one = '\t\t<DT><A HREF="' + j[0] + '" ADD_DATE="" ICON="">' + j[
                    1] + '</A>\n'
                group += one
            group += '\t</DL><p>\n'
        group += '</DL><p>\n'
        f_new.write(group)

def main():
    # the bookmarks file exported from your browser
    html = 'bookmarks.html'
    # the new bookmarks file we want to get
    html_new = 'bookmarks_new.html'
    # config file of classifier type
    type_dict = json.load(open('classify_type.txt', 'r'))
    # config file of classifier
    category_dict = json.load(open('classify.txt', 'r'))

    list_link = analysis_bookmarks(html)
    list_link_new = classify(list_link, type_dict, category_dict)
    create_new_html(html_new, list_link_new, type_dict)


if __name__ == "__main__":
    main()
