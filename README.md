# Project - NIM

![Nim Logo](/images/nim_logo_256.png?raw=true)

The famous math game written in python.

### P.S. :

Why I only use one underscore instead of two for non-public attributes:

-   [PEP8 - Method Names and Instance Variables](https://www.python.org/dev/peps/pep-0008/#method-names-and-instance-variables)
-   [PEP8 - Designing for Inheritance](https://www.python.org/dev/peps/pep-0008/#designing-for-inheritance)

example:

```python
Foo._nonPublic   # Instead of
Foo.__nonPublic  # Will actually be Foo._Foo__nonPublic
```
