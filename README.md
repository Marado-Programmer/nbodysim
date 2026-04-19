# _N_-body simulation

PyCUDA

CUDA

NVIDIA

Python

C/C++

# Tests

```console
pixi run test
```

# Documentation

## Type hinting

Even though Python is a dynamic language, this project uses type hinting and
especially function annotations every time the interpreter can't infer the type.

More about that [here][hinting].

[hinting]: <https://docs.python.org/3/library/typing.html#module-typing>

## Inline Documentation

Using `docstring`s and following the [`numpy`'s style guide][style_guide]

[style_guide]: <https://numpydoc.readthedocs.io/en/latest/format.html>

Along with this, the documentation can also have some examples of code that can
be tested using the [`doctest` module][doctest].

[doctest]: <https://docs.python.org/3/library/doctest.html>

## Report

This school project requires me to create a report to document the results, the
thought process, methodology, and the studying required to carry out this
project.

It was suggested for the student to use [Typst][typst_docs], and so I gave it a
try.

[typst_docs]: <https://typst.app/docs/>

All the source files to produce the report are in the [`/docs/`](./docs/)
directory. The main file that you need to know about is
[`/docs/report.typ`](/docs/report.typ), the rest of the files - which aren't
many — you will figure out about them by yourself. There's
[`/docs/bibliography.yaml`](/docs/bibliography.yaml) for example, which is the
bibliography that then can be referenced from Typst. It uses Typst's own format,
[Hayagriva][typst_bib].

[typst_bib]: <https://github.com/typst/hayagriva/blob/main/docs/file-format.md>

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

# i18n

We use python's [`gettext` standard module][gettext] for every text string that
the user has the possibility to see. Together with that, we use
[`locale`][locale] when needed.

[gettext]: <https://docs.python.org/3/library/gettext.html>
[locale]: <https://docs.python.org/3/library/locale.html>

When in need of string templating, we use this approach:

```python
_("calculated mass: {mass} kg").format(mass=locale.format_string("%.2e", mass))
```
