---
title: How do I conceptualize Messiaen Mode 3 for composition?
date: 2021-07-02T00:00:00.000Z
categories:
  - music-theory
tags:
  - music theory
  - composition
  - messiaen modes
  - modes of limited transposition
author: Rafael S. Calsaverini
draft: true
slug: conceptualize-messiaen-mode-3-composition
lastmod: 2022-03-13T17:33:18.495Z
---

## Introduction

As always, 12tone released a wonderful new video about Modes of Limited Transposition or Messiaen Modes, which are an extremely thought provoking set of scales. In the end he challenged listeners to write something using those scales and I decided to bite the bullet.

I'm not going to explain a lot how modes of limited transposition are defined, since 12tone's video is already so good. But in essence those are scales that when transposed by certain intervals smaller than an octave, produce a scale with the same interval patterns over a different "root". This symmetry kinds of make the root very ambiguous and mess up our sense of tonality. But at the same time there's a lot of "familiar" structure about those scales.

## Starting

So, to start out I wanted to create a bit of structure because a lot of what I usually do when I try to write won't work. For example, choosing a root doesn't make a lot of sense since many different notes have completely simmetric patterns around them.

I started by choosing Messiaen Mode 3 starting from the note `C`, which is comprised of the following notes: `C D Eb E F# G Ab Bb B` [^footnote1]. This mode repeats the same pattern of intervals after being transposed by a major third. So either `C`, `E` or `Ab` could be a "root".

Moreover, there are really just three classes of notes here, judging by how the other notes are related to them. We have:

- the "roots": `C`, `E` and `Ab`;
- the "seconds": `D`, `F#` and `Bb`;
- and the "thirds": `Eb`, `G` and `B`.

If you start on any of the roots, the pattern of intervals you see going up is: major second, minor third, major third, diminished fifth, fifth, augmented fifth, minor seventh and major seventh; for any of them. Similarly in the table below you can see the patterns of intervals going up from each of the classes:

{{< columntable caption="Interval structure" >}}

headers: [Class ,Note,b2/b9,2/9,3m/#9,3M/b11,4/11,b5/#11,5 ,/#5/b13,6/13,7m/#13,7M]

rows:

    - [Roots/3, C, -, D, Eb, E, -, F#, G, Ab, -, Bb, B]
    - [E, -, F#, G, Ab, -, Bb, B, C, -, D, Eb]
    - [Ab, -, Bb, B, C, -, D, Eb, E, -, F#, G]
    - [Seconds/3, D, Eb, E, -, F#, G, Ab, -, Bb, B, C, -]
    - [F#, G, Ab, -, Bb, B, C, -, D, Eb, E, -]
    - [Bb, B, C, -, D, Eb, E, -, F#, G, Ab, -]
    - [Thirds/3, Eb, E, -, F#, G, Ab, -, Bb, B, C, -, D]
    - [G, Ab, -, Bb, B, C, -, D, Eb, E, -, F#]
    - [B, C, -, D, Eb, E, -, F#, G, Ab, -, Bb]

{{< /columntable >}}

Since the structures are identical, we can focus on exploring the roots, seconds and thirds without worrying about the specific notes.

## Harmony

Conjuring up chords from the table above is almost trivial, practically a matter of enumerating the intervals. Here are the chords that can be created for each class:

{{< columntable caption="Interval structure" tag="code">}}

headers: [Class, Triads, Suspended Chords, 7th Chords, Suspended 7th Chords]

rows:

    - [Roots/4, I, Isus2/2, I7 IMaj7, I7sus2/2]
    - [IMin, IMin7 IMinMaj7]
    - [I˚, n/a/3 , IMin7(b5), n/a/3]
    - [I+, I+Maj7]
    - [Seconds, II+, II7(#5)]
    - [Thirds/3, IIIb, IIIbsus4/2, IIIbMaj7, IIIbsus4Maj7/2]
    - [IIIbMin, IIIbMinMaj7]
    - [IIIb+, n/a, IIIb+Maj7, n/a]

{{< /columntable >}}

[^footnote1]: Since there are 9 tones in this scale, choosing the right letter notation is tricky so I just arbitrarily decided to not use double or unusual accidentals. I'm also not too concerned about calling intervals by the natural relative names. So instead of calling the fourth degree `Fb`, I'm just going to call it `E` and instead of saying it is a diminished fourth from the first degree, I'll just say it's a minor third from it.
