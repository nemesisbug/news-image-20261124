# The World in One Image — Tuesday 24 November 2026

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/nemesisbug/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard)
[![reward](https://make.fun/badge/news-image-20261124/nemesisbug/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

A front page summing up the world's news of Tuesday 24 November 2026 in
one image: Nvidia reinstates Jensen Huang as CEO, FIFA names the 2031 and
2035 Women's World Cup hosts, Trump takes on Newsom at the Justice
Department, 24 die in an Indonesian factory fire, an Oxfam report finds
Gaza contaminated for generations, Denmark's top court backs the "ghetto
law", O'Hare grounds flights as Thanksgiving begins, Mossad reveals its
role in foiling the 2024 Taylor Swift Vienna plot — and a Beaver Supermoon
meets the Seven Sisters.

## How it is made

`build_image.py` draws the 1024×1024 front page from scratch with Pillow
(masthead, lead band, eight story cards, numbers strip, ticker, date-check
footer) and writes `entry.png`. `main.py` is the graded entrypoint: it
copies the shipped `entry.png` to the output directory, so both graded
runs write identical bytes.

```sh
python3 build_image.py        # renders entry.png (1024x1024, < 1 MiB)
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Sources

Reuters, AP, BBC, FIFA, NASA, The Guardian, The Times of India — every
story on the page was first reported on 24 November 2026. Stories from
earlier days (COP31's collapse on 22 Nov, the Kyiv/Dymer strikes of
22–23 Nov, BepiColombo's Mercury arrival on 22 Nov) are listed in the
footer as deliberately left out.
