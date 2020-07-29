.. Pyteen documentation master file, created by
   sphinx-quickstart on Mon Jul 27 20:52:09 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pyteen
======

.. toctree::
   :maxdepth: 2
   :caption: Contents:

This is a tiny collection of self-contained, short Python code snippets that are (1) all tested and validated, (2) easy to contribute to, and (3) simple to reuse.

Code size
---------

The main aspect here is code size which at the start was a strict limit of ten lines of code because in Python this already allows for solving useful little tasks, and the first chosen project name was "tenliners" (not so funky, agreed). Of course, some code is more useful than some other, hence it makes little sense to count comments or docstrings or empty lines (non-code). In fact, you soon realize you only really care about "effective code", that has the most effect (or value) to solve your task or demonstrate something. And there is very little effect in lines with only opening or closing brackets, braces or parentheses often typed to manually make data structures more readable. Same with imports which only enable you to use some modules. What is left is code that really *does* something when it executes. And this is what we are trying to measure here.

Now the number ten is somewhat arbitrary (why not 11?) and it can be hard or impossible to express some interesting things with ten or less lines, even in Python. Therefore "ten" was stretched a bit into "teen" leading to the name "Pyteen" and a limit of 19 lines of effective code. Let's see where that goes!
