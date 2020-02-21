# Preparing and uploading new versions to PyPI

## Prepare

1.  Make sure that the program passes all build checks and is clean and ready for a new release

2.  Run `pip3 install -U bump2version setuptools wheel twine` to download and update all required packages

3.  Bump the program version with `bump2version <type>` where `<type>` is either `major`, `minor`, or `patch`

    `major` = The program functions in an entirely new way, needed the user to change a significant amount of syntax or
    delete existing generated data to function (this should rarely if ever happen)

    `minor` = There are mainly new additions and minor removals to the program that keep the program pretty much the same
    but modify some functionality

    `patch` = There are mainly fixes to bugs and issues with very few additions / removals

4.  Create a new entry in `HISTORY.md` with the new version number and list all notable changes to **code** (not docs,
    tests, or build files). Include notable bug fixes, improvements, and new or removed features as bullet points using
    the commit history as a guide: `https://github.com/UNCG-DAISY/psi-collect/compare/v<old version>...v<new version>`

5.  Commit and push changes made by *bump2version*'s updates to the repo along with any other final changes you want to
    include in the new version, making sure to push the new version tag (e.g. `git push --follow-tags`)

6.  Make sure build checks pass either by `Travis-CI` or run `tox` (`pip3 install tox`) locally to be safe

!!! note "Before You Continue"

    Travis-CI should automatically build and upload a new package to pypi when a new version tag is created and pushed
    to the master branch, within a few minutes of the pull request being merged. If this doesn't happen follow the
    remaining steps, otherwise skip to the validation step!

## Build

1.  Run `python3 setup.py sdist bdist_wheel`

    Two new packages should have appeared in a directory called `dist` named something like `psi-collect-<version>.tar.gz`
    and `psi-collect-<version>-py3-none-any.whl`.

    *If there are no files no response after running commands, try executing all commands mentioned, with `pip` instead
    of `pip3` and `python` instead of `python3`. This likely means you don't have Python 2 installed.*

## Create Access Token

*Skip this section if you have a token setup and ready.*

1. Login to your account on https://pypi.org/manage/account/token/

2. Create a token with any name and select `Project: psi-collect` under **Scope**

3. Copy the token including `pypi-`


## Upload

1.  Run `python3 -m twine upload dist/* --skip-existing` then enter your PyPI access token (including `pypi-`) as the
    password and `__token__` as the username if asked

## Validating

1.  Visit https://pypi.org/project/psi-collect/ and you should see the latest version on the main page in a few moments

2.  Try `pip3 install -U psi-collect`. It may take a few minutes before pip recognizes its existence locally, if it
    doesn't when you try, make sure you include the `-U` and try again after a few minutes.

3.  Do some basic testing to make sure the commands still work
