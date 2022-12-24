alfred-linkding-workflow
=========

Alfred workflow to search for bookmarks on your local linkding instance.

Configuration
-------

* Import linkding.alfredworkflow into Alfred
* Configure the workflow settings
  * Linkding instance - The URL to your linkding instance
  * Linkding token - The auth token from your linkding instance

Usage
-----

* First refresh your local linkding bookmark cache
  * Keyword: ldrefresh
* Search in your locally cached linkding bookmarks
  * Keyword: ld
  * Use "#<tag-name>" to search for tags
  * Other parts of your search query are checked against title and url
  * Example: "ld #my-tag github.com my-repository"

License
-------

* [MIT](LICENSE.md)
