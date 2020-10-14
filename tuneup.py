#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tuneup assignment

Use the timeit and cProfile libraries to find bad code.
"""

__author__ = "Timothy Reynoso and John"

import cProfile
import pstats
from pstats import SortKey
from functools import wraps
import timeit
from collections import Counter


def profile(func):
    """A cProfile decorator function that can be used to
    measure performance.
    """
    # Be sure to review the lesson material on decorators.
    # You need to understand how they are constructed and used.
    # raise NotImplementedError("Complete this decorator function")

    @wraps(func)
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        # print(pr)
        pr.enable()
        func(*args, **kwargs)
        pr.disable()
        sortby = SortKey.CUMULATIVE
        ps = pstats.Stats(pr).strip_dirs().sort_stats(sortby)
        ps.print_stats()
        # print(ps)
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
    # Not optimized
    movies = read_movies(src)
    duplicates = []
    while movies:
        movie = movies.pop()
        if is_duplicate(movie, movies):
            duplicates.append(movie)
    return duplicates

#
# Students: write a better version of find_duplicate_movies
#


def optimized_find_duplicate_movies(src):
    # Your code here
    movies = read_movies(src)
    c = Counter(movies)
    duplicates = []
    for movie in c:
        if c[movie] > 1:
            duplicates.append(movie)
    return duplicates

# Your code here
    # print(f'Reading file: {src}')
    # with open(src, 'r') as f:
    # => movies = f.read().splitlines()

    # duplicates = set(movies)
    # # for movie in movies:
    # #     movies.remove(movie)
    # #     if movie in movies:
    # #         duplicates.append(movie)
    # return [line for line in sorted(duplicates)]


def timeit_helper(func_name, func_param):
    """Part A: Obtain some profiling measurements using timeit"""
    assert isinstance(func_name, str)
    stmt = f"{func_name}('{func_param}')"
    setup = f"from {__name__} import {func_name}"
    t = timeit.Timer(stmt, setup)
    runs_per_repeat = 3
    num_repeats = 5
    result = t.repeat(repeat=num_repeats, number=runs_per_repeat)
    time_cost = min(result) / float(num_repeats)
    print(f"""
    func={func_name}
    num_repeats={num_repeats}
    runs_per_repeat={runs_per_repeat}
    time_cost={time_cost:.3f} sec""")
    return t


def main():
    """Computes a list of duplicate movie entries."""
    # Students should not run two profiling functions at the same time,
    # e.g. they should not be running 'timeit' on a function that is
    # already decorated with @profile

    filename = 'movies.txt'

    print("--- Before optimization ---")
    result = find_duplicate_movies(filename)
    print(f'Found {len(result)} duplicate movies:')
    print('\n'.join(result))

    print('--------------------------------------\n\n')
    print("--- after optimization ---")
    result = optimized_find_duplicate_movies(filename)
    print(f'Found {len(result)} duplicate movies:')
    print('\n'.join(result))

    print("\n--- Timeit results, before optimization ---")
    timeit_helper('find_duplicate_movies', filename)

    print("\n--- Timeit results, after optimization ---")
    timeit_helper('optimized_find_duplicate_movies', filename)

    print("\n--- cProfile results, before optimization ---")
    profile(find_duplicate_movies)(filename)

    print("\n--- cProfile results, after optimization ---")
    profile(optimized_find_duplicate_movies)(filename)


if __name__ == '__main__':
    main()
    print("Completed.")
