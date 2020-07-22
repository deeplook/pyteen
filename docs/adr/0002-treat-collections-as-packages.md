# 2. Treat collections as packages

Date: 2020-08-21

## Status

Accepted

## Context

Managing a snippet collection should work for different collections, and it should be simple to reuse and add individual snippets.

## Decision

Collections of snippets are required to be a regular Python package, organized in a way every Python developer is familiar with.
Each snippet is contained in one Python module. All operations on a collection of snippets, like search and validation are performd by code outside the collection itself.

## Consequences

This follows common practice in various other available collectione online, although rarely with the intention to import individual snippets.
It is easy to reuse a snippet as-is, simply by importing it.
Ideally this requires the snippet code to be placed inside a function, but it's not strictly needed, depending on the kind of reuse.
Collections can be easily published, distributed, installed and reused.
