#!/usr/bin/env python3
# The above tells bash or zah or whatever shell program you are using
# to use python3 to execute this.

from typing import Iterable, Sequence
import os
import random
import argparse
import itertools

def scan_dir(directory: str, recurse: bool) -> Iterable[str]:
    for (dirpath, _, filenames) in itertools.islice(os.walk(directory, topdown=True),
                                                    None if recurse else 1):
        yield from (os.path.join(dirpath, f) for f in filenames)

def get_files(num_samples: int, directory: str) -> Iterable[str]:
    files = scan_dir(directory, True)
    # filtering?
    return select_files(list(files), num_samples)

def select_files(filelist: Sequence[str], num: int) -> Iterable[str]:
    # Use unsafe PRNG.
    return random.sample(filelist, num)

def write_selected_files(filelist):
    with open("samples.txt", "w") as f:
        for warc in filelist:
            f.write(warc+"\n")

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--num_samples", '-n',
                        default=100,
                        type=int,
                        help="How many files to select.")
    parser.add_argument("--directory", "-d",
                        default=".",
                        type=str,
                        help="Directory to search for warc files.")
    # Recursive? Read from file? Output to file? Verbosity?
    return parser.parse_args()

def run() -> None:
    args = get_args()
    files = get_files(args.num_samples, args.directory)
    for f in files:
        print(os.path.abspath(f))


if __name__ == "__main__":
    run()

