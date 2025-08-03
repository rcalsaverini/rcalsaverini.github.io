---
title: Negative Harmony inverts brightness of modes
date: 2021-02-20T23:24:31.590Z
categories:
  - music-theory
tags:
  - Music Theory
  - Negative Harmony
  - Set Theory (Music)
author: Rafael S. Calsaverini
draft: false
slug: negative-harmony-inverts-brightness-modes
---

## Intro

Recently I've been listening to a [12tone video][12tone] on YouTube about negative harmony, a concept recently popularized by musician Jacob Collier. On the related links I found a bunch of videos from [this channel][negative-harmony-covers] with "negative harmony" versions of many popular songs.

The change in sonority of those songs clearly indicated for me a change in the _mode_ of the song, which kind of go against the grain of what I've been told about the action of those transformations. In this post I want to explore negative harmony as a transformation not only on chords but on scales, modes and melody.

### What is Negative Harmony anyway?

There are many ways to understand negative harmony and I'm not going to pretend I'm able to give a full historical background. The video by the 12tone channel that I linked above does a much better job than I ever could. Here in this post I'm mainly interested in this as a transformation that can be applied to a particular set of notes, and that's how I'm going to describe and treat it.

To understand what's the transformation being applied, consider the circle of fifths. In the key of C, the negative harmony transformation consists in swapping notes along the axis that cut the circle in half between the C and G.

{{<tikz caption="The circle of fifths highlighting the negative harmony transformation in the key of C">}}

\begin{tikzpicture}[auto,node distance=2.5cm, block/.style={color=black, align=center, minimum height=1cm, minimum width=1.5cm}, vec/.style={thick,color=black!50}]

    \def \n {12}
    \def \radius {4 cm}
    \def \margin {7}

    \def \notes {-5/D$\flat$, -4/A$\flat$, -3/E$\flat$, -2/B$\flat$, -1/F, 0/C, 1/G, 2/D, 3/A, 4/E, 5/B, 6/F$\sharp$}

    \foreach \s/\key in \notes {
      \def \start {360 * \s / \n + 15}
      \def \end {360 * (\s - 1) / \n + 15}

      \node[block, circle, color=violet] at ({90-\start}:\radius) (a\s) {\Large\key};
      \draw[vec] ({\end+\margin}:\radius) arc ({\end+\margin}:{\start-\margin}:\radius);
    }

    \draw [thick,dashed,color=violet!50] (0, -\radius) -- (0, \radius);

    \draw[latex-latex,color=violet!50,thick] (a0) to (a1);
    \draw[latex-latex,color=violet!50,thick] (a2) to (a-1);
    \draw[latex-latex,color=violet!50,thick] (a3) to (a-2);
    \draw[latex-latex,color=violet!50,thick] (a4) to (a-3);
    \draw[latex-latex,color=violet!50,thick] (a5) to (a-4);
    \draw[latex-latex,color=violet!50,thick] (a6) to (a-5);

\end{tikzpicture}

{{</tikz>}}

The arrows above indicate the notes that are to be switched. So, to apply the negative harmony transformation in the key of C, one would change C for G, D for F, etc.

### Parameterizing Negative Harmony

One aspect that is not often discussed about this transformation is that it is actually a **family of transformations** parameterized by a key center. Note that the reflection axis chosen above is only one chosen from 12 possibilities. To highlight this, notice that in the diagram above the transformation in the key of C takes F to D. In the diagram below we have transformation in the key of A, showing that in this case it takes F to A♭.

{{<tikz caption="The circle of fifths highlighting the negative harmony transformation in the key of A">}}

\begin{tikzpicture}[auto,node distance=2.5cm, block/.style={color=black, align=center, minimum height=1cm, minimum width=1.5cm}, vec/.style={thick,color=black!50}]

    \def \n {12}
    \def \radius {4 cm}
    \def \margin {7}

    \def \notes {-5/B$\flat$, -4/F, -3/C, -2/G, -1/D, 0/A, 1/E, 2/B, 3/F$\sharp$, 4/D$\flat$, 5/A$\flat$, 6/E$\flat$}

    \foreach \s/\key in \notes {
      \def \start {360 * \s / \n + 15}
      \def \end {360 * (\s - 1) / \n + 15}

      \node[block, circle,color=violet] at ({90-\start}:\radius) (a\s) {\Large\key};
      \draw[vec] ({\end+\margin}:\radius) arc ({\end+\margin}:{\start-\margin}:\radius);
    }

    \draw [thick,dashed,color=violet!30] (0, -\radius) -- (0, \radius);

    \draw[latex-latex,color=violet!50,thick] (a0) to (a1);
    \draw[latex-latex,color=violet!50,thick] (a2) to (a-1);
    \draw[latex-latex,color=violet!50,thick] (a3) to (a-2);
    \draw[latex-latex,color=violet!50,thick] (a4) to (a-3);
    \draw[latex-latex,color=violet!50,thick] (a5) to (a-4);
    \draw[latex-latex,color=violet!50,thick] (a6) to (a-5);

\end{tikzpicture}

{{</tikz>}}

## Transforming modes

Typically negative harmony is discussed [in the context of chords][brltheory], with an expectation that transformed chords has similar functions (having "equivalent tonal gravity"). I want to discuss how this transformation behaves when considering melodic elements, scales and modes.

To start, let's check what happens when we transform the seven modes of the major scale. For example, let's apply the transformation over the major scale. As an ilustration, the sequence of notes [C, D, E, F, G, A, B] (the Ionian mode of C Major), transformed in the key of C, will result in [G, F, E♭, D, C, B♭, A♭].

This sequence can be interpreted in a lot of different ways. Harmonically it is typical to consider the following argument. If the original harmony is in the key of C major, than the I chord is C major triad (C, E, G). This triad transforms to (G, E♭, C), which is an inversion of the C minor triad. Since this would also fit the role of the I chord in the new harmony, this should be interpreted as transforming from a C major harmony to a C minor one.

That's a good argument, but if we focus on the melody, the note that would be treated as the focus and resting place of the melody in the original key would be C, which would turn into G in the new melody. So, we could interpret G as the root note of the transformed sequence, which would make it a G Phrygian melody.

Let's take this second stance and see what happens with all modes. Under this interpretation this is how the modes transform:

- C Ionian transforms into G Phrygian.
- C Dorian trasforms into G Dorian.
- C Phrygian trasforms into G Ionian.
- C Lydian transforms into G Locrian.
- C Mixolydian trasforms into G Aelian.
- C Aeolian trasforms into G Mixolydian.
- C Locrian transforms into G Lydian.

### Negative Harmony inverts brightness

Finally, here's the neat and interesting pattern to notice: if we ignore the roots, the quality of the modes above is transforming up and down the [Brightness Scale][brightness].

{{<tikz>}}
\usetikzlibrary{shapes,arrows,positioning,automata}
\usetikzlibrary{matrix,arrows,decorations.pathmorphing}

\begin{tikzpicture}[auto,node distance=1.25cm, block/.style={rectangle, thick, fill=purple!20, align=center, minimum height=1cm, minimum width=2cm}, vec/.style={double,thick,color=purple!20}, connecto/.style={<->, >=latex, shorten >=2pt, shorten <=2pt, bend left=90, thick, dashed}]

    \draw[thick,dashed,color=orange] (5, 0) -- (-2, 0) node[above,color=orange] at (5, 0) {reflexion axis};
    \node[block,] at (0, 0) (dor) {\normalsize Dorian};
    \node[block,above of=dor] (mix) {\normalsize Mixolydian};
    \node[block,above of=mix] (ion) {\normalsize Ionian};
    \node[block,above of=ion] (lyd) {\normalsize Lydian};
    \node[block,below of=dor] (aeo) {\normalsize Aeolian};
    \node[block,below of=aeo] (phr) {\normalsize Phrygian};
    \node[block,below of=phr] (loc) {\normalsize Locrian};

    \draw[vec,->] (-2, -4) -- (-2, 4)
          node[above,sloped,color=purple] at (-2.5, 4) {high brightness}
          node[midway,above,sloped,color=purple] at (-2.5, 0) {\textbf{Brightness Scale}}
          node[below,sloped,color=purple] at (-2.5, -4) {low brightness};

    \draw[connecto] (lyd.east) to node[auto, swap] {} (loc.east);
    \draw[connecto] (ion.east) to node[auto, swap] {} (phr.east);
    \draw[connecto] (mix.east) to node[auto, swap] {} (aeo.east);
    \draw[connecto,bend left=90] (dor.30) to node[auto, swap] {} (dor.330);

\end{tikzpicture}
{{</tikz>}}

The effect of the transformation is to reflect the qualities of the modes around the center of the brightness scale, inverting the value of the brightness for the mode in question (the brightest mode becomes the darkest, the second brightest becomes the second darkest, etc).

## So what?

Yes, this is just a simple neat symmetry I found. I intend to write more later on some other questions:

- What happens when you transform modes of other scales?
- Modes of the major scale are closed under this transformation. But this definitely won't happen always. What does it mean when it happens?
- What happens when you transform modes under the negative harmony centered in other keys?
- Is there a "right" key to use?

Stay tuned.

[12tone]: https://www.youtube.com/watch?v=SF8CdxcdJgw
[brltheory]: https://www.brltheory.com/resources/negative-harmony-chord-chart/
[negative-harmony-covers]: https://www.youtube.com/channel/UCurOAVtqb7kM1siNlDynzFw
[brightness]: https://www.youtube.com/watch?v=9rEqrPwVITY
