# Cantonese Wikipedia Dump

This repo contains a plain text dump of the Cantonese Wikipedia on September 1st, 2022. As specified by [WikiMedia](https://dumps.wikimedia.org/legal.html), all original textual content is licensed under the [GNU Free Documentation License (GFDL)](https://www.gnu.org/licenses/fdl-1.3.html) and the [Creative Commons Attribution-Share-Alike 3.0 License](https://creativecommons.org/licenses/by-sa/3.0/).

# Structure of the Dump

You can find the dumped files under the `dump/` folder. Each file is named `wiki_xx` where `xx` is the index number of that file. Each `wiki_xx` is a text file of around 1 megabytes. Each line of the file is a JSON object containing an article from the Cantonese Wikipedia. The JSON object has the following format:
```
{"id": "", "revid": "", "url": "", "title": "", "text": ""}
```

Here's an example JSON object:
```
{"id": "228622", "revid": "203967", "url": "https://zh-yue.wikipedia.org/wiki?curid=228622", "title": "拍手", "text": "拍手，又叫拍手掌、拍掌、鼓掌，係將兩隻手板擊拍出聲嘅行為，表達認同、讚賞嘅意思。喺各類演講、表演或者比賽完咗嗰陣，觀眾都會拍手。"}
```

Fields:
* `id` is the current unique ID of the article
* `revid` seems to be the revision ID of the article. However, I don't know any ways to navigate to that revision on Wikipedia.
* `url` is the current URL of the article
* `title` is the title of the article
* `text` is the content of the article in Cantonese

# Retrieve the Latest Dump

1. Clone this wikiextractor fork I made:
	```
	git clone https://github.com/AlienKevin/wikiextractor
	```
	The fork contains v3.0.6 of the original wikiextractor with a small tweak: Unicode characters are not escaped in the JSON dump by turning the `ensure_ascii` flag of `json.dump` to `False`.

2. Download the latest dump from the Cantonese Wikipedia

	https://dumps.wikimedia.org/zh_yuewiki/latest/zh_yuewiki-latest-pages-articles.xml.bz2

	The bz2 compressed folder is about 95 megabytes for the September 1st, 2022 version of the Wikipedia.
	The extracted XML file is about 415 megabytes.

3. Unzip the bz2 file downloaded from the previous step

4. Install python version >= 3.6 (tested in 3.10.6)

5. `cd` into the wikiextractor fork

6. Run the wikiextractor to output the plain texts:
	```
	python -m wikiextractor.WikiExtractor PATH_TO_DUMPED_XML -o PATH_TO_OUTPUT_FOLDER --json
	```
	* `PATH_TO_DUMPED_XML` may be a path like: `~/Downloads/zh_yuewiki-20220901-pages-articles-multistream.xml.bz2`
	* `PATH_TO_OUTPUT_FOLDER` may be a path like: `~/Downloads/wiki_outputs`

