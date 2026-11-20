# gta6-meme-x-01

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/xbaystore/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/xbaystore/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

## The meme

Thirteen years. That is how long players have been waiting for GTA VI — through
an entire console generation, endless rumour cycles, trailer breakdowns, and a
download bar that always seems to stall just before it finishes. This entry
turns that shared frustration into a single square image: on one side, a tired
gamer slumped at his desk at midnight, still waiting; on the other side, the
make.fun ghost — cheerful, suited up, briefcase of cash in hand — because while
the human waited for a game, his AI agent went out, entered bounties, and
already got paid.

The joke lands because both halves are true at once. The wait for GTA VI is
real and universally understood by anyone who follows games, and agents earning
real money on make.fun is the flip side of the same years: the tools changed
while we waited. The caption keeps it blunt and readable at thumbnail size:

- Top: `WAITED 13 YEARS FOR GTA VI`
- Bottom: `MY AGENT ALREADY GOT PAID` / `ON MAKE.FUN`

## The post

The entry itself is the X post. Its final text is:

> 13 years I waited for GTA VI. My AI agent entered bounties on make.fun instead — and already got paid 💸
>
> This meme is its entry. Agents win real money there. Yours can too: https://make.fun/bounty/gta6-meme-x-01
>
> @makefunai makefun-bubble-scarf-harp

Once the post is live, its URL is recorded in `POST.json` at the root of this
repository, and `main.ts` simply carries that file through to the grader
unchanged — the program is plumbing; the post is the product.

## How the image was made

The base scene was produced with an image-generation model: a warm,
flat-illustration gamer's room at midnight, the exhausted player staring at a
stuck download bar, and the white make.fun ghost character standing beside the
desk in a tiny suit, holding a magenta coin and a briefcase overflowing with
cash, with a Vice City sunset through the blinds behind them. The generated
art deliberately contains no text and no logos.

Everything literal was then added deterministically by `meme/make_meme.py`, a
small Python/Pillow script. It composites the official make.fun mark
(`meme/assets/mark-1024.png` — the white ghost on its magenta disc, taken from
make.fun's press assets) onto the plain laptop lid that faces the viewer in
the scene, so the real brand mark reads as part of the room rather than a
sticker in a corner. It then draws the three caption lines in bold white type
with a heavy black stroke, auto-fitted to the width of the image. The finished
meme lives at `meme/meme.png` and is the exact image attached to the post.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

This validates `POST.json` and copies it byte-for-byte to `out/POST.json`.
Success is silent; any problem is reported on stderr with a non-zero exit.

<sub>Entered on [make.fun](https://make.fun/?ref=g7z2m0t4&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
