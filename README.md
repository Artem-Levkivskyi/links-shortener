# Links shortener. Service for create short links for URL's.
## Functional:
### You can do next actions:
* Shortening some URL.
* Go to websites by your short link
---
## How it work:
### Get short link for your URL:
* If you enter your URl in form in service, system check it's database for availability this link.
* If link is present in database, system send you short link with key from database.
* Else - system generates short link for your URL, put it in database and send you it.
* If you enter some string, was not a link, system send you an error.
### Get website for your shortlink:
* If you enter in address row some short link, system check if it short link is correct.
* If database don't containe key from your short link, ystem send you error
* Else - you get URL for you key and will be redirect to website.
