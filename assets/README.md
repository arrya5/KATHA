# Katha — Assets (drop generated art here)

The app serves this folder at `/assets/…` and uses real images **if present**, otherwise it
falls back to the procedural look. No code change — generate, name correctly, drop in, reload.

```
backgrounds/<scene>.jpg            1080×1920 JPG. <scene> = the tale's `background` id:
                                     cremation-ground-night, ujjain-court-day,
                                     river-ghat-night, palace-gate-midnight,
                                     cremation-ground-circle-night
characters/<speaker>_<expr>.png    ~800×1000 transparent PNG. <expr> = amused|intense|grave|neutral
characters/<speaker>.png             expression-less fallback (e.g. kshantishila.png, betaal.png)
ui/                                  optional frames/ornaments
sound/<scene>.mp3                    optional per-scene ambient loop (future)
```

Speaker ids: `betaal`, `kshantishila`, `madanasundari`, `dhavala`, `tree_climber`,
`first_brahmin`, `ash_keeper`, `reviver`, `maiden`, `viravara`, `son`, `boy`, `father`.

Start small: `betaal_amused/intense/grave.png` + the 5 backgrounds give the biggest lift.
