import re, json

# the bookmarks file exported from your browser
html = 'bookmarks.html'
# the new bookmarks file we want to get
html_new = 'bookmarks_new.html'
# init list
link_list = []
link_list_new = [[] for i in range(6)]
# config file of classifier
category_dict = json.load(open('classify.txt', 'r'))
# config file of classifier type
type_dict = json.load(open('classify_type.txt', 'r'))
# reverse the dict above
type_dict_reverse = dict(zip(type_dict.values(), type_dict.keys()))


# the classifier of bookmarks
def classify(list):
    for domain, link, text in list:
        if domain not in category_dict:
            cate = 'other'
        else:
            cate = category_dict[domain]
        link_item_new = (link, text)
        link_list_new[type_dict[cate]].append(link_item_new)
    print(link_list_new)
    print('classify:' + str(len(link_list_new)))


# read the original bookmarks html, filter the link and text of <a>
with open(html, 'r') as f_origin:
    lines = re.findall('<DT>(.*?)<DT>', f_origin.read(), re.S)
    print('Total:' + str(len(lines)))
    for line in lines:
        domain = re.findall('://[a-zA-Z0-9]*\.(.*?)\.', line, re.S)
        link = re.findall('HREF="(.*?)"', line, re.S)
        text = re.findall('">(.*?)</A>', line, re.S)
        if len(domain) > 0 and len(link) > 0 and len(text) > 0:
            link_item = (domain[0], link[0], text[0])
            link_list.append(link_item)
    print(link_list)
    print('Filter:' + str(len(link_list)))
    classify(link_list)

# write the results to a new bookmarks html
with open(html_new, 'w') as f_new:
    group = '<!DOCTYPE NETSCAPE-Bookmark-file-1>\n' \
            + '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\n' \
            + '<TITLE>Bookmarks</TITLE>\n' \
            + '<H1>Bookmarks</H1>\n' \
            + '<DL><p>\n'
    for i, item in enumerate(link_list_new):
        group += '\t<DT><H3 ADD_DATE="" LAST_MODIFIED="">' + type_dict_reverse[i] + '</H3>\n\t<DL><p>\n'
        for j in item:
            one = '\t\t<DT><A HREF="' + j[0] + '" ADD_DATE="" ICON="">' + j[1] + '</A>\n'
            group += one
        group += '\t</DL><p>\n'
    group += '</DL><p>\n'
    f_new.write(group)
