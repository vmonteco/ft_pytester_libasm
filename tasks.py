from invoke import task, Context
from typing import List
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

_static_lib_filename = "libasm.a"
_shared_lib_filename = "libasm.so"
_rootdir = "ft_pytester_libasm/libasm_test_suite"


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

    # Build shared library from the static one (if libasm.so is older than
    # libasm.so):
    c.run(
        f'echo "Creating {_static_lib_filename}'
        f' out of {_shared_lib_filename}."'
    )
    if not os.path.isfile(shared_lib_path) or os.path.getmtime(
        static_lib_path
    ) > os.path.getmtime(shared_lib_path):
        c.run(
            f"gcc -shared -o {shared_lib_path} -Wl,--whole-archive"
            f"{static_lib_path} -Wl,--no-whole-archive"
        )
    else:
        c.run(
            f'echo "{shared_lib_path} younger than {static_lib_path}.'
            f' Nothing to do."'
        )


@task(
    name="test",
    default=True,
    help={
        "path": "path to the libasm repo.",
        "clean": "remove the shared library (libasm.so) after the tests.",
        "build": "build the static library (libasm.a).",
    },
)
def test(
    c: Context,
    path: str = ".",  # Path to repository to test.
    clean: bool = False,
    build: bool = True,
    debug: bool = False,
) -> None:
    """
    Runs the test suite after building the shared library (if necessary).
    """

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

    with c.cd(BASE_DIR):
        c.run(
            (
                f"pytest -c {pytest_config_file} -v --maxfail=42"
                f" --libasm={shared_lib_path}"
                f" --color=yes {d} {''.join(pytest_args)}"
            ),
            pty=True,
            echo=True,
        )

    if clean:
        os.remove(shared_lib_path)


@task
def checks(c: Context):
    c.run("tox -e py310", pty=True)
