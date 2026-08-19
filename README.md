# Go Goals! — SDG Board Game

A digital adaptation of the UN's **"Go Goals!"** board game about the 17 Sustainable
Development Goals, reworked so teams play as **nations racing the same 2030 deadline
from very different starting lines**.

**▶️ Play it: https://go-goals-game-live.web.app**

## How it plays

- Teams draw a random **nation** that permanently sets how fast they move (×2, normal,
  or ÷2 dice speed) and which of the 17 goals they already have infrastructure for.
- Resourced for a goal? One correct answer clears it. Not resourced? Two in a row.
- Every correct answer secretly adopts a real behavior society needs for that goal —
  none of it shown until 2030.
- Reaching 2030 doesn't win. It's a **deadline**: it triggers one final round, then the
  reveal shows which goals the world actually achieved and how each nation's starting
  privilege shaped that.

## Three ways to run it

| Mode | Use it for |
|---|---|
| **One Device** | Everyone around one screen. Fully offline — no internet needed. |
| **Host for Teams** | Teacher creates a game, shares a 5-letter code, watches a live board. |
| **Join a Game** | Each team enters the code on their own Chromebook and claims a slot. |

In hosted games only the acting team's device gets live controls; everyone else sees the
same board with a waiting banner. If a device closes or crashes, reopening the site
offers to **rejoin the game exactly where it left off** — state lives in Firestore.

## Development

Single self-contained `go-goals-game.html` — no build step. Open it directly, or:

```bash
firebase deploy --project go-goals-game-live
```

`firestore.rules` scopes all access to the `games/` collection. Game codes are the only
access control (classroom trust model); see the comments in that file.

---

Adapted from the official "Go Goals!" board game by the United Nations Regional
Information Centre (UNRIC) with artist Yacine Aït Kaci (YAK) — [go-goals.org](https://go-goals.org).
Unofficial fan-made educational version; not affiliated with or endorsed by the UN.
