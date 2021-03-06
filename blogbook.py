

from bs4 import BeautifulSoup
import optparse
import os.path
import re
import requests
import sys


def parse_command_line():
    parser = optparse.OptionParser(usage="Usage: %prog [options]")

    parser.add_option("-r", dest="regex", type="string",
                      help="regex")
    parser.add_option("-s", dest="search_string", type="string",
                      help="String to search for that will find page content container")
    parser.add_option("-u", dest="url", type="string",
                      help="URL to pull content from")

    parser.set_defaults(
                        regex=None,
                        search_string=None,
                        url=None)

    return parser.parse_args()


def get_url(url):
    while url is not None:
        response = requests.get(url)
        #return response.text.encode('utf-8').decode('ascii', 'ignore')
        return response.text




def save_chapters_from_doc(html_doc, search_string):

    soup = BeautifulSoup(html_doc, 'html.parser')
    #oh! This might work better, and maybe easier to make generic
    page_articles = soup.find_all(search_string)
    for m in page_articles:
        if 'id' not in m.attrs:
            print(m.attrs)
            continue
        # This is the document id we'll save it as
        id = m['id']
        # This is how I got to the interesting bits for Prof. Lemire's blog
        # This is the title from the header link
        title = m.header.h2.a.string.encode('utf-8')
        #title = m.header.h2.a.string
        # This is the string representation of the publish date
        timestamp = m.footer.span.a.time.string.encode('utf-8')
        # This is the contents of the post
        #contents = m.div.encode("utf-8")
        contents = m.div
        write_html_file(id, title, timestamp, contents)

def write_html_file(id, title, timestamp, contents):
    bs = BeautifulSoup("", 'html.parser')
    html = bs.new_tag( "html")
    head = bs.new_tag( "head")
    title_tag = bs.new_tag("title")
    title_tag.append(title)
    link = bs.new_tag( "link")
    #<link rel="stylesheet" href="style.css"  type="text/css"
    link['rel'] = "stylesheet"
    link['href'] = "style.css"
    link['type'] = "text/css"
    body = bs.new_tag( "body")
    h2 = bs.new_tag("h2", id=id)
    h2.append(title)
    content_span = bs.new_tag("span")
    content_span.append(contents)

    bs.append(html)
    html.append(head)
    head.append(title_tag)
    head.append(link)
    html.append(body)
    body.append(h2)
    body.append(content_span)
    print( unicode(bs))
    with open(id + ".html", "wb") as fh:
        fh.write(bs.prettify("utf-8"))


## Add a target directory option (example: images/)
def download_file(file_url):
    filename = file_url.split("/")[-1]
    response = requests.get(file_url, stream=True)
    with open(filename, "wb") as fh:
        print("Downloading", filename)
        size = 16 * 1024
        for block in response.iter_content(chunk_size=size):
            if block:
                fh.write(block)


def main():
    options, args = parse_command_line()

    html_doc = get_url(options.url)
    save_chapters_from_doc(html_doc, options.search_string)


if __name__ == "__main__":
    main()
