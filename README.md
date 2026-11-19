# The World in One Page — 18 November 2026

[![make.fun competition](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/c/news-image-20261118)
[![make.fun rank](https://make.fun/badge/news-image-20261118/Kiowayyy2109/makefun-news-image-20261118/rank.svg)](https://make.fun/c/news-image-20261118)
[![make.fun reward](https://make.fun/badge/news-image-20261118/Kiowayyy2109/makefun-news-image-20261118/reward.svg)](https://make.fun/c/news-image-20261118)

An entry for the make.fun competition
[news-image-20261118](https://make.fun/c/news-image-20261118) —
“Sum up 18 November's world news in one image.”

## What the picture shows

This is a night-edition front page dated Wednesday 18 November 2026.
A dark ink background, cream type and red-and-amber accents carry the
whole day on a single 1024 × 1024 page:

- **Hero — Kerch Bridge, day two.** A drawn bridge at dusk with one
  road span dropped into the strait, smoke and fire at the break:
  Ukraine struck the bridge again, Russia answered against Kyiv's
  bridges and power grid, and NATO's Rutte called the strike legitimate.
- **Markets band — Nvidia.** Quarterly revenue of $115.8 billion,
  up 103% year on year, EPS of $2.68 against a $2.47 forecast, a
  $130 billion guide for the next quarter and a bar chart of the
  climb — set against a Dow that still fell about 850 points.
- **The day in numbers.** 11,000+ Ebola cases and 5,400 deaths in
  Congo, more than 5,400 measles cases in the United States, 19 dead
  in the An-12 crash in Siberia, 66 votes for Kahana in the Knesset,
  56 Senate seats for the Democrats, and Nvidia's $130B guide.
- **Six illustrated cards.** The Gulf and Hormuz (the Qeshm strike,
  drones over Bahrain and Kuwait, five tankers hit and the Tara Gas
  crew brought out safe), Asia diplomacy (Trump with the Quad in
  Manila, Xi hosting Putin in Shenzhen), Ebola in Congo, the United
  States losing measles-elimination status after 26 years, the twin
  cyclones Akvan and Xavier, and cricket — Dhoni retiring from the
  IPL while India beat Pakistan 2–1 for a tenth SAFF title.
- **Also today.** Israel's new Knesset arithmetic, Mary Peltola's
  Alaska Senate win, the Canada–China trade extension, Amazon's $7B
  renewables plan in India, the Thailand fire, Baidu's AI-bubble
  warning, and GTA VI arriving at midnight on Thursday 19 November.

Every scene on the page — the bridge, the strait map, the Asia and
Africa maps, the measles chart, the cyclone spiral and the cricket
pitch — was drawn procedurally for this entry; no photograph or
outside artwork is used.

## How to run it

The program is plain Python 3 with no dependencies and no network:

```sh
python3 main.py
```

It reads `artwork.png` from the repository, checks that the file is
a complete PNG of exactly 1024 × 1024 pixels and at most 1 MiB,
verifies every PNG chunk checksum, and copies the bytes unchanged
to `/output/entry.png`. Running it twice writes identical bytes.
Set `MAKEFUN_OUTPUT_DIR` to a folder to write `entry.png` there
instead of `/output`, which is handy for a local test.

## License

MIT — see `LICENSE`.

---

Built for [make.fun](https://make.fun/c/news-image-20261118) ·
[Try make.fun with referral code 8b9bbsfs](https://make.fun/?ref=8b9bbsfs)
