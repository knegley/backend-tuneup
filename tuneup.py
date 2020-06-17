#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tuneup assignment

Use the timeit and cProfile libraries to find bad code.
"""

__author__ = "Kyle Negley"

import cProfile
import pstats
from functools import wraps
import timeit


def profile(func):
    """A cProfile decorator function that can be used to
    measure performance.
    """
    # Be sure to review the lesson material on decorators.
    # You need to understand how they are constructed and used.

    @wraps(func)
    def wrapper(*args, **kwargs):

        with cProfile.Profile() as pr:

            func(*args, **kwargs)
        pr.dump_stats("tuneup_profiler.profile")
        stats = pstats.Stats(pr).sort_stats(pstats.SortKey.CUMULATIVE)
        stats.print_stats(5)

    return wrapper


def timeit_helper(func):
    """Part A: Obtain some profiling measurements using timeit."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        setup = f"from __main__ import {func.__name__}"
        number = 5
        repeat = 7
        t = timeit.Timer(stmt="func(*args,**kwargs)", setup=setup)

        result = timeit.repeat(number=number, repeat=repeat)
        print(
            f'\nBest time across {repeat} repeats of {number} runs per repeat is {(sum(result)/len(result))*1e6:.4f} micro seconds \n')

        return func(*args, **kwargs)
    return wrapper


def read_movies(src):
    """Returns a list of movie titles."""
    print(f'Reading file: {src}')
    with open(src, 'r') as f:
        return f.read().splitlines()


def is_duplicate(title, movies):
    """Returns True if title is within movies list."""
    for movie in movies:
        if movie.lower() == title.lower():
            return True
    return False


def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list."""
    movies = read_movies(src)
    duplicates = []
    while movies:
        movie = movies.pop()
        if is_duplicate(movie, movies):
            duplicates.append(movie)
    return duplicates


@profile
@timeit_helper
def main():
    """Computes a list of duplicate movie entries."""
    result = find_duplicate_movies('movies.txt')
    print(f'Found {len(result)} duplicate movies:')
    print('\n'.join(result))


if __name__ == '__main__':
    main()
