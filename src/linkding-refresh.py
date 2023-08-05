#!/usr/bin/env python3
# linkding-refresh.py
# created by Christian Wilhelm
import urllib.request
import os
import json
import pathlib


class LinkdingClient:
    def __init__(self, host: str, token: str):
        self._host = host
        self._token = token

    def _request(self, url: str) -> {}:
        req = urllib.request.Request(url)
        req.add_header('Authorization', 'Token %s' % self._token)
        req.add_header('User-Agent', 'Mozilla/5.0')
        r = urllib.request.urlopen(req)
        parsed = json.loads(r.read())
        return parsed

    def _load_page(self, url: str) -> ({}, str):
        data = self._request(url)
        return data["results"], data["next"]

    def collect_bookmarks(self):
        url = "%s/api/bookmarks/" % self._host
        all_bookmarks = []
        while url is not None:
            bookmarks, url = self._load_page(url)
            all_bookmarks = all_bookmarks + bookmarks
        return all_bookmarks


def main():
    env_token = os.environ["linkding_token"]
    env_host = os.environ["linkding_host"]
    env_cache_dir = os.environ["alfred_workflow_cache"]
    bookmark_cache_file = os.path.join(env_cache_dir, "bookmarks.json")
    cache_path = pathlib.Path(env_cache_dir)
    cache_path.mkdir(parents=True, exist_ok=True)
    client = LinkdingClient(host=env_host, token=env_token)
    bookmarks = client.collect_bookmarks()
    with open(bookmark_cache_file, mode="w") as f:
        f.write(json.dumps(bookmarks))


if __name__ == "__main__":
    main()
