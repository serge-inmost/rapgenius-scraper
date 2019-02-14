# rapgenius-scraper
Download lyrics from your favorite artists at genius.com

The script uses the Genius landing page of each artist to gather links to
individual songs, then browse each song page to gather lyrics and new song
links.

## Directions

Provide list of artists in file artists.txt, separated by line break (\n).
Each artist name must match his name on the website.
Examples:
- Pete Rock & C.L. Smooth as "Pete-rock-and-cl-smooth"
- Mos Def as "Yasiin-bey"

Provide your uner agent in user_agent, you can find it on
https://www.whatismybrowser.com/detect/what-is-my-user-agent

Provide proxy information (if needed) in proxies.

Output produced in output.txt
