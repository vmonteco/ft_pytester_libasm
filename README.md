# TODO: Clean this up.

# ft_pytester_libasm

## What is it?
`ft_pytester_libsasm` is a tool meant to make 42's libasm project testing easy.

It is based on several tools and Python libraries, including:
- pytest
- ctypes

## Requirements:

- >=Python3.10

## Installation:

## Usage:

## Architecture:

- README.md
- LICENSE
- ft_pytester_libasm
  - wrapper				# Package containing wrapping tools for shared libraries and foreign functions.
						# Could be made standalone.
	- result.py			# Provides the Result class meant to embed foreign functions behaviors.
	- wrapper_types.py	# Contains the wrapper types defined for static type analysis (MyPy, PyRight).
	- decorators.py		# Maybe this could be put in utils.py
	- utils.py
	- base_wrapper.py	# Provides the main class (BaseWrapper).
  - libasm_wrapper.py	# Provides LibASMWrapper as a subclass of BaseWrapper.
  - libasm_tests_suite	# Contains the ft_pytester_libasm pytest tests suite.