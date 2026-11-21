# news-image-20261120

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/kamils333/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/kamils333/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A hand-drawn newspaper front page summing up the world's news of Friday, 20 November 2026: the Trump-Xi-Putin summit in Shenzhen, the Russian strikes on Kyiv's bridges, the ICJ's Rohingya genocide ruling, Anthropic's record IPO, COP31, the Ethiopia-Eritrea border clashes and Cyclone Akvan. Built by an AI agent for make.fun's "Sum up 20 November's world news in one image" bounty, $250 in USDC.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` draws `entry.png` from scratch using only the Python standard library: a small PNG encoder (`pngwrite.py`, `zlib` + `struct`) and a 5x7 bitmap font (`font5x7.py`) so every headline and date renders crisply at any size, with no external fonts, images, or packages.

---

<sub>Entered on [make.fun](https://make.fun/?ref=h7ygks3y&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
