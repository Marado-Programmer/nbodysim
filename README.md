# _N_-body simulation

PyCUDA

CUDA

NVIDIA

Python

C/C++

# Tests

# Documentation

## Inline Documentation

## Report

This school project requires me to create a report to document the results, the
thought process, methodology, and the studying required to carry out this
project.

It was suggested for the student to use [Typst][typst_docs], and so I gave it a
try.

All the source files to produce the report are in the [`/docs/`](./docs/)
directory. The main file that you need to know about is
[`/docs/report.typ`](/docs/report.typ), the rest of the files - which aren't
many — you will figure out about them by yourself. There's
[`/docs/bibliography.yaml`](/docs/bibliography.yaml) for example, which is the
bibliography that then can be referenced from Typst. It uses Typst's own format,
[Hayagriva][typst_bib].

From experience, there's not much to know about when it comes to write Typst. If
you don't know how to do something, just use the search bar in the docs, and
you'll find out how to do it.

To compile the report file, use:

```console
typst c -f pdf report.typ
```

I'm trying out [`typstyle`](https://typstyle-rs.github.io/typstyle/) as a
formatter:

```console
typstyle -i report.typ && typst c -f pdf report.typ
```
