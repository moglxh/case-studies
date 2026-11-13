# Evidence

All outputs come from the lab VM. Names and addresses are lab-only.

## Unbound configuration

Query logging (`query-log.conf`):

```
server:
    verbosity: 1
    log-queries: yes
```

Block list (`typo-block.conf`), one rule per name in the generated typo list (29 rules). It was generated from `typos.txt` with:

```
{ echo "server:"; sed 's/.*/    local-zone: "&.lab.test." always_nxdomain/' typos.txt; } > typo-block.conf
```

The first lines look like this:

```
server:
    local-zone: "ovabot.lab.test." always_nxdomain
    local-zone: "nvabot.lab.test." always_nxdomain
```

## Replay with the block off

```
1) DNS lookup for novabot.lab.test
   answer: 192.0.2.10
2) Connect and request the page
NovaBot official site (served for novabot.lab.test)

1) DNS lookup for nvabot.lab.test
   answer: 192.0.2.66
2) Connect and request the page
LAB DEMO: lookalike 'Security Check' page (served for nvabot.lab.test). In the real campaign a fake verification prompt appears here. This lab shows nothing to run.
```

The typo resolves and the victim reaches the lookalike page.

## Replay with the block on

```
1) DNS lookup for novabot.lab.test
   answer: 192.0.2.10
2) Connect and request the page
NovaBot official site (served for novabot.lab.test)

1) DNS lookup for nvabot.lab.test
   no answer (NXDOMAIN) - the victim never connects
```

The real site is unaffected; the typo dead-ends at the DNS step.

## What each system saw

Lookalike web server log (only the block-off visit appears):

```
[lookalike] GET / HTTP/1.1 Host=nvabot.lab.test
[lookalike] GET /verify HTTP/1.1 Host=nvabot.lab.test
```

Legitimate web server log (one visit per state):

```
[legit] GET / HTTP/1.1 Host=novabot.lab.test
[legit] GET / HTTP/1.1 Host=novabot.lab.test
```

Resolver log, typo watchlist matches during the replay (both attempts recorded, including the blocked one):

```
      2 nvabot
```
