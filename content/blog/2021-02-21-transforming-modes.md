---
title: Transforming modes
date: 2021-02-22T00:03:05.420Z
categories:
  - music-theory
tags:
  - Music Theory
  - Negative Harmony
  - Set Theory (Music)
  - Neo-Riemannian Theory
  - Chord transformations
author: Rafael S. Calsaverini
draft: true
slug: transforming-modes
lastmod: 2022-03-13T17:21:07.039Z
---

## Intro

I want to continue the discussion in the [last post](/blog/negative-harmony-inverts-brightness-modes/) about transformations of modes and sets of tones. I want to explore the following question: what are transformations that make sense and what are they effect on scales, tone sets and modes.

### The Transformations

I want to get back to the circle of fifths and define a few transformations and analise their implications. The transformations that I'm interested in are based in the idea of the negative harmony. As defined in the previous post, the negative harmony in a given key is obtained by reflecting the circle of fifths along an axis midway between the key and the its fifth. For example, here's a diagram of the negative harmony in the key of C:

{{<tikz>}}
\begin{tikzpicture}[auto,node distance=2.5cm, block/.style={color=black, align=center, minimum height=1cm, minimum width=1.5cm}, vec/.style={thick,color=black!50}]

    \def \n {12}
    \def \radius {4 cm}
    \def \margin {7}

    \def \notes {1,...,12}

    \foreach \s in \notes {
      \def \start {360 * \s / \n + 15}
      \def \end {360 * (\s - 1) / \n + 15}

      \node[block, circle, color=violet] at ({90-\start}:\radius) (a\s) {\Large $X_{\s}$};
      \draw[vec] ({\end+\margin}:\radius) arc ({\end+\margin}:{\start-\margin}:\radius);
    }


    \foreach \x in {1, 2, ..., 6} {
        \def \a {\x * 30 - 30}
        \draw [thick,dashed,color=violet!50] (\a:-\radius-20) -- (\a:\radius + 20)
            node[above,sloped,color=purple] at (\a:\radius + 20) {$\mathcal{N}_{\x}$};
    }

\end{tikzpicture}

{{</tikz>}}

We will identify those transformations by $N_{x}$ where $x \in \{C, D\flat, \ldots, B\flat, B\}$

[12tone]: https://www.youtube.com/watch?v=SF8CdxcdJgw
[brltheory]: https://www.brltheory.com/resources/negative-harmony-chord-chart/
[negative-harmony-covers]: https://www.youtube.com/channel/UCurOAVtqb7kM1siNlDynzFw
[brightness]: https://www.youtube.com/watch?v=9rEqrPwVITY
