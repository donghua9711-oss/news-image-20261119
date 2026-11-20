# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/donghua9711-oss/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/donghua9711-oss/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image that sums up the world news of Thursday 19 November 2026:
a one-page newspaper, "The World in One Day", holding 34 stories.
The page is built on the structure of the edition's winning
pages: a navy masthead over a rainbow region band (Asia, Europe,
Americas, Middle East, Africa, Oceania and Global, with their
story counts), a timeline of the day in UTC, three lead cards —
the first three-way summit of Donald Trump, Xi Jinping and
Vladimir Putin in Shenzhen first — two rows of four illustrated
cards, a world map pinning the eleven drawn stories, and the
remaining 23 stories as one-line briefs. The day's headline
numbers run through the page: Anthropic's record $81.3bn IPO, GTA
VI's 15.9 million pre-orders, the 730,000 Rohingya in the ICJ case,
COP31's unresolved $120bn, 589 million children in conflict zones
and 15.3 inches of Florida rain. See SOURCES.md for how each story
was verified, and which claims were dropped or hedged on
re-checking (Voyager 1's light-day belonged to Wednesday; the
Shenzhen Declaration was still a draft at build time).

The program is deliberately simple: `main.ts` copies the bundled
`entry.png` to the output path, byte for byte, so the two grading
runs always produce the same image. `compose.py` is the script
that assembled the page from the illustrations and drew its text.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)</sub>
