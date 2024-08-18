from invoke import task, Context
from typing import List, Optional
import os
import sys
from libasm_wrapper.tags import (
    LibASMTag,
    all_tags,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

_static_lib_filename = "libasm.a"
_shared_lib_filename = "libasm.so"
_rootdir = "libasm_test_suite"

# strdup related:
_run_strdup_src_filename = "run_ft_strdup.c"
_run_strdup_src_path = os.path.join(
    os.path.join(BASE_DIR, "libasm_test_suite/bin_tools"),
    _run_strdup_src_filename,
)
_run_strdup_path = _run_strdup_src_path.replace(".c", "")


@task(
    name="build",
)
def _build(c: Context, /, *, path: str = ".") -> None:
    """
    The build task takes a libasm repository path and runs its Makefile to
    build the libasm static library (libasm.a). It then builds the shared
    library (libasm.so) out of it.
    """
    # Get paths:
    repo_path: str = os.path.abspath(path)
    static_lib_path: str = os.path.join(repo_path, _static_lib_filename)
    shared_lib_path: str = os.path.join(repo_path, _shared_lib_filename)
    makefile_path: str = os.path.join(repo_path, "Makefile")

    c.run('echo "Running build task"')

    # Ensuring that the Makefile exists:
    # TODO: Better error handling perhaps?
    try:
        assert os.path.isfile(
            makefile_path
        ), f"Error: File {makefile_path} not found."
    except AssertionError as e:
        print(e)
        sys.exit(1)

    # Run make:
    c.run(f'echo "Creating {_static_lib_filename} by running the Makefile."')
    # TODO: add other rules as options.
    c.run(f"make -C {repo_path}")

    # Ensure that libasm.a was created:
    assert os.path.isfile(
        static_lib_path
    ), f"Error: File {static_lib_path} not found."

    # Strdup-related build:
    c.run(
        f"gcc -o {_run_strdup_path} -L {repo_path} {_run_strdup_src_path} "
        f"{static_lib_path}"
    )

    # Build shared library from the static one (if libasm.so is older than
    # libasm.so):
    c.run(
        f'echo "Creating {_shared_lib_filename}'
        f' out of {_static_lib_filename}."'
    )
    if not os.path.isfile(shared_lib_path) or os.path.getmtime(
        static_lib_path
    ) > os.path.getmtime(shared_lib_path):
        c.run(
            f"gcc -shared -o {shared_lib_path} -Wl,--whole-archive"
            f" {static_lib_path} -Wl,--no-whole-archive"
        )
    else:
        c.run(
            f'echo "{shared_lib_path} younger than {static_lib_path}.'
            f' Nothing to do."'
        )


functions_tree = {
    "mandatory": {
        "ft_strlen",
        "ft_strcpy",
        "ft_strcmp",
        "ft_write",
        "ft_read",
        "ft_strdup",
    },
    "bonus": {
        "ft_atoi_base",
        "ft_list_push_front",
        "ft_list_size",
        "ft_list_sort",
        "ft_list_remove_if",
    },
}


@task(
    name="test",
    default=True,
    help={
        "path": "path to the libasm repo.",
        "clean": "remove the shared library (libasm.so) after the tests.",
        "build": "build the static library (libasm.a).",
        # TODO: Improve description.
        # "includes": "directory containing the libasm.h",
        "tests": (
            "Marks to designate tests to run. Available choices are : "
            "{tags}. This option can be specified several times to specify "
            "several tests to run. No test specified will result in running "
            "all available tests."
        ).format(tags=", ".join([tag.value for tag in all_tags])),
    },
    iterable=["tests"],
)
def test(
    c: Context,
    path: str = ".",  # Path to repository to test.
    clean: bool = False,
    build: bool = True,
    debug: bool = False,
    tests: Optional[List[LibASMTag]] = None,
) -> None:
    """
    Runs the test suite after building the shared library (if necessary).
    """

    if tests is None:
        tests = []

    pytest_config_file: str = os.path.join(
        BASE_DIR, "ft_asm_pytester_pytest.ini"
    )

    repo_path: str = os.path.abspath(path)
    shared_lib_path: str = os.path.join(repo_path, _shared_lib_filename)
    pytest_args: List = []
    d = " --pdb " if debug else ""

    c.run('echo "Running test task"')

    if build:
        _build(c, path=repo_path)

    # Ensuring that the shared library exists:
    assert os.path.isfile(
        shared_lib_path
    ), f"File {shared_lib_path} not found."

    # Run tests:
    # TODO: consider using a python pytest invoaction :
    # https://docs.pytest.org/en/6.2.x/usage.html#calling-pytest-from-python-code
    # Or is it better to keep the command line invocation?

    tests_flags: str = '-m "' + " or ".join(flag for flag in tests) + '"'

    with c.cd(BASE_DIR):
        c.run(
            (
                f"pytest -c {pytest_config_file} -sv --maxfail=42"
                f" --libasm={shared_lib_path}"
                f" --color=yes {d} {''.join(pytest_args)}"
                f" {tests_flags}"
            ),
            pty=True,
        )

    if clean:
        os.remove(shared_lib_path)


@task
def checks(c: Context):
    c.run("tox -e py310", pty=True)
