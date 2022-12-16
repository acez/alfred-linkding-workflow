import http.client
import json
import os


class AlfredItem:
    def __init__(self, title: str, subtitle: str = None, arg: str = None, quicklookurl: str = None):
        self._title = title
        self._subtitle = subtitle
        self._arg = arg
        self._quicklookurl = quicklookurl

    def __dict__(self):
        return {
            "title": self._title,
            "subtitle": self._subtitle,
            "quicklookurl": self._quicklookurl,
            "arg": self._arg,
            "icon": {
                "type": "fileicon",
                "path": "/Applications/Safari.app"
            }
        }


class AlfredOutputFormatter:
    def __init__(self, items: [AlfredItem]):
        self._items = items

    def print(self):
        output_format = {
            "items": self._items
        }
        output = json.dumps(output_format, default=lambda o: o.__dict__())
        print(output)


class LinkdingBookmark:
    def __init__(self, bookmark):
        self._url: str = bookmark["url"] or ""
        self._title: str = bookmark["title"] or bookmark["website_title"] or bookmark["url"]
        self._tags: [str] = bookmark["tag_names"]

    def to_alfred_item(self) -> AlfredItem:
        return AlfredItem(title=self._title, subtitle=self._url, arg=self._url, quicklookurl=self._url)

    def matches_query(self, query: str) -> bool:
        query = query.lower()
        if query.strip() == "":
            return True
        if self._title.lower().find(query) != -1:
            return True
        if self._url.lower().find(query) != -1:
            return True
        return False


class LinkdingClient:
    def __init__(self, host: str, token: str):
        self._host = host
        self._token = token

    def _request(self, path: str) -> {}:
        conn = http.client.HTTPSConnection(self._host)
        headers = {'Authorization': "Token %s" % self._token}
        conn.request("GET", path, headers=headers)
        res = conn.getresponse()
        data = res.read()
        parsed = json.loads(data)
        return parsed

    def bookmarks(self, query: str) -> [LinkdingBookmark]:
        data = self._request(path="/api/bookmarks/")
        alfred_bookmark_items = []
        for row in data["results"]:
            bookmark = LinkdingBookmark(bookmark=row)
            if bookmark.matches_query(query=query):
                alfred_bookmark_items.append(bookmark)
        return alfred_bookmark_items


if __name__ == "__main__":
    query = "{query}"
    token = os.environ["linkding_token"]
    host = os.environ["linkding_host"]
    client = LinkdingClient(host=host, token=token)
    items = list(map(lambda v: v.to_alfred_item(), client.bookmarks(query=query)))
    AlfredOutputFormatter(items=items).print()
