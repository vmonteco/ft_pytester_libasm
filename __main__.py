#!/usr/bin/env python3.10

from invoke import Program, Collection
import tasks

# TODO: Perhaps find a DRY-way for the version?
# TODO: refacto: everything not directly linked to invoke should be a level
#       lower in directories.
program = Program(namespace=Collection.from_module(tasks), version="0.0.0")

if __name__ == "__main__":
    program.run()
