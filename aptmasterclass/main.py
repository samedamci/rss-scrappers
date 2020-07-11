#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import rfeed
from datetime import datetime

FEED_TITLE = "APT Master Class Protips"
FEED_DESCRIPTION = "Przydatne lub mniej przydatne one-linery w PWSH, BASH i innych."
FEED_LINK = "https://samedamci.me/o/aptmc_protips/feed.xml"

document_main = requests.get("https://aptmasterclass.com/protip/history").content
html_main = BeautifulSoup(document_main, "html.parser")


def get_description(link):
    document = requests.get(link).content
    html = BeautifulSoup(document, "html.parser")
    content = html.find_all("div", {"class": "text-muted"})

    return "".join([str(item) for item in content])


def main():
    links, titles, items = [], [], []

    for id in html_main.find_all("div", {"class": "mt-2 pt-2 text-right"}):
        id = id.get_text().split("aptm.in/protip/")[1].split(" »")[0]
        links.append(f"https://aptmasterclass.com/protip/{id}")

    for title in html_main.find_all("h1", {"class": "heading mb-3"}):
        title = title.get_text().split("\n")[1].strip()
        titles.append(title)

    for i in range(len(links)):
        items.insert(
            i,
            rfeed.Item(
                title=titles[i], link=links[i], description=get_description(links[i])
            ),
        )

    feed = rfeed.Feed(
        title=FEED_TITLE,
        description=FEED_DESCRIPTION,
        link=FEED_LINK,
        language="pl",
        lastBuildDate=datetime.now(),
        items=items,
    )

    with open("feed.xml", "w") as f:
        f.write(feed.rss())


if __name__ == "__main__":
    main()
