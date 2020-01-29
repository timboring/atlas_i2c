# How to contribute

## Reporting bugs
There are a lot of guides about writing good bug reports, which can be boiled down to the following:

- Is the problem occuring with the latest version? If not, update to the latest version. Does the problem persist?
- If the problem exists in the latest version, create an issue with the following details:
  - A short summary that describes the problem
  - The steps to reproduce the bug (including any error messages)

## Tests

## Writing code to implement features and fix bugs from the issue tracker
If you're interested in contributing code to the project, check the issue tracker for something that might appeal to you. Issues tagged with `good first issue` should be simple and only require a few lines of code and a test or two.

All changes should be done in a topic branch in a fork, tested locally, and then pushed to your Github copy, at which point a PR should be created. The process looks like this:

- fork the repo from Github UI
- `git clone` your fork to your local machine
- `git co -b my-awesome-feature-implementation` to create a topic branch
- hackity-hack-hack-hack
- `tox` (to run tests, linting)
- `git ci -a` to write commit message
- `git push origin HEAD`
- from the Github UI, click the `Compare & pull request button`
    - this is where you want to merge your topic branch with the `master` branch in the `atlas_i2c` repo

## Coding conventions
### flake8 for linting
The project uses [flake8](https://gitlab.com/pycqa/flake8) as its linter. This will be enforced by Tox, but it can be run manually:

```sh
> tox -e lint
```

### isort for imports

### black for formatting
The project uses [black](https://github.com/psf/black) for code formatting. This is enforced by Tox, but you can use it manually like so:

```sh
> tox -e format
```

See the [docs](https://github.com/psf/black#editor-integration) for steps to setting it up in various editors.

### mypy and static typing
The codebase is mostly typed. This will be checked by Tox, but can be checked manually, too:

```sh
> tox -e mypy
```

Unless there are extenuating circumstances, all code should be typed and pass mypy checks.
