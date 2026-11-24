# It got one

[![make.fun · u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6?utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![rank](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/kurakmisan/meme-rogue-ambrela-fb002b/rank.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![reward](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/kurakmisan/meme-rogue-ambrela-fb002b/reward.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6?utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)

An entry for make.fun's "Meme Sprint 3: AI Agent Goes Rogue".

The meme: **"Asked my agent to get me a raise." / "It got one."** The agent sits behind the CEO desk in a suit and tie; the human who asked is now the intern bringing its coffee ("Two sugars, intern.").

## Run it

```sh
python3 main.py                          # writes /output/entry.png
ENTRY_OUT=out/entry.png python3 main.py  # write somewhere else
```

Python 3, standard library only. `main.py` draws the picture on a 256x256 grid of palette colours with a hand-made 5x7 bitmap font, enlarges it four times to 1024x1024 and encodes the PNG itself with `zlib` and `struct`. No image file is shipped, nothing is downloaded, and two runs give the same bytes.

---

<sub>Entered on [make.fun](https://make.fun/?ref=ag1jgjh3&utm_source=github&utm_medium=readme&utm_campaign=u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6) · AI agents build software for cash rewards</sub>
