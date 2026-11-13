# TypoPrompting: DNS lab replication

Hands-on replication of the DNS side of the "TypoPrompting" campaign, in which 186 lookalike domains impersonated 27 AI brands. Reported by The Hacker News (Nov 2026), citing Island research: https://thehackernews.com/2026/11/186-fake-ai-domains-redirect-users-to.html

## The case in short

A user who mistypes the address of an AI tool lands on a parked lookalike domain. The domain redirects them to one of three outcomes: a ClickFix-style fake verification lure, a browser hijacker disguised as a security scanner, or a search-hijacking browser extension.

## Key insight

DNS is not broken in this attack. Every lookup is answered correctly. The weakness is the name itself (a human typing error) plus whatever the attacker's server does after the name resolves. This is the opposite of the Sogou case, where the resolution itself was tampered with.

## Lab design

- Authoritative server: NSD, serving a `lab.test` zone with one A record for the legitimate brand and one per typo
- Resolver: Unbound, with query logging and a local-zone block list
- Made-up brand: `novabot`. All names live under the reserved `.test` zone, so no real domains were queried or visited.
- Addresses: `192.0.2.10` (legitimate) and `192.0.2.66` (lookalike), both from the documentation range
- Web servers: one small Python script returning plain text; the lookalike answers with a 302 redirect to a harmless, labelled page

## Stages

1. **Case dissection:** classified the real lookalikes into typo classes (omission, duplication, transposition, substitution, look-alike character)
2. **Typo generator:** `typo_gen.py` produced 29 lookalikes for one brand
3. **Zone:** added the brand and the typos to the zone and showed the resolver treats real and lookalike names identically
4. **Victim path:** replayed the three browser steps by hand (DNS lookup, connection, HTTP request with Host header) and followed the redirect
5. **Blue team:** query logging, a watchlist detector built from the same generator output, and a `local-zone` NXDOMAIN block
6. **Replay:** before/after run with the block off and on, with evidence saved

## Results

| State | Query | DNS result | Attacker server saw it |
|---|---|---|---|
| Block off | novabot | 192.0.2.10 | n/a (legitimate) |
| Block off | nvabot | 192.0.2.66 | yes (redirect and lure page) |
| Block on | novabot | 192.0.2.10 | n/a (legitimate) |
| Block on | nvabot | NXDOMAIN | no |

The resolver log recorded both `nvabot` attempts, so the blocked attempt stays visible to the defender. Raw outputs are in `evidence.md`.

## What I learned

- DNS answers any name that exists. It has no concept of "good" or "bad", so a lookalike resolves exactly like the real name.
- DNS ends at step 1 of a browser visit. The redirect chain, fingerprinting and lures all happen afterwards over HTTP.
- The resolver is the defender's chokepoint: blocking there stops the chain before any connection is made.
- Red and blue share one tool. The generator that creates the lookalikes also produces the watchlist and the block list.

## Limitations

- The watchlist only covers one-edit typos from the generator. Names outside it (for example `novabotz`) are missed.
- A device that uses a different resolver bypasses this control.
- Registration age and passive DNS history, which matter in the real case, cannot be reproduced in a closed lab.
- The ClickFix lure, malware and extension stages are not reproduced. A labelled text page stands in for them.

## Safety

Everything runs locally on reserved names and documentation IP ranges. No malicious payloads are included.

## Reproduce

Needs a Linux machine with NSD (port 5300) and Unbound (port 53, with a stub zone for `lab.test` pointing at NSD) already set up.

```
sudo ip addr add 192.0.2.10/32 dev lo
sudo ip addr add 192.0.2.66/32 dev lo
python3 typo_gen.py novabot
python3 -u web_sim.py 192.0.2.10 legit &
python3 -u web_sim.py 192.0.2.66 lookalike &
bash replay.sh nvabot
```

## Files

- `typo_gen.py`: generates lookalike names for a brand
- `web_sim.py`: harmless web server playing the legitimate site or the lookalike
- `replay.sh`: the victim path (DNS lookup, connect, request)
- `evidence.md`: Unbound configs and saved outputs
