CHANGELOG
=======

# 2022.04.02

## BREAKING CHANGES - Python 3.7 Support Deprecated

- Due to an inherit [`pandas` dependency, python 3.7 support has been deprecated](https://pandas.pydata.org/docs/whatsnew/v1.4.0.html#increased-minimum-version-for-python)

## Version bumps

- bandit 1.7.0 to 1.7.4
- black 21.9b0 to 22.3.0
- click 7.1,<8.1 to 7.1,<8.2
- jinja 3.0.1 to 3.1.1
- mypy 0.910 to 0.942
- nox 2021.10.1 to 2022.1.7
- pandas 1.3.3 to 1.4.1
- pylama 7.7.1 to 8.3.8
- pytest 6.2.5 to 7.1.1


## Github Actions setup python upgrade

- Upgraded setup python from v2 to v3.1.0

# 2021.10.17

## Type hints

Type hinting has been added across the codebase [(#150)](https://github.com/writememe/motherstarter/pull/150) which closes long standing issue [(#19)](https://github.com/writememe/motherstarter/issues/19).

- Added type hints to codebase
- Refactored some unit tests
- Added `mypy` to CI testing

## Version bumps

- black 21.5b1 to 21.9b0
- click max version from <=7.2 to <8.1
- jinja2 2.11.3 to 3.0.1
- mypy 0.812 to 0.910
- nox 2020.12.31 to 2021.10.1
- openpyxl 3.0.7 to 3.0.9
- pandas 1.2.4 to 1.3.3
- pytest 6.2.3 to 6.2.5
- pytest-cov 2.11.2 to 3.0.0
- yamllint 1.26.1 to 1.26.3

## Codecov Github Actions upgrade

- Upgraded [Codecov action](https://github.com/codecov/codecov-action) from 1.4.1 to 2.1.0

# 2021.05.11

## Version bumps

- black 20.8b1 to 21.5b1
- openpyxl 3.0.6 to 3.0.7
- pandas 1.2.3 to 1.2.4
- pytest 6.2.2 to 6.2.3
- yamllint 1.26.0 to 1.26.1

# 2021.03.05

## Version bumps

- jinja 2.11.2 to 2.11.3
- pytest 6.2.1 to 6.2.2
- pandas 1.2.1 to 1.2.3
- mypy 0.800 to 0.812

# 2021.02.07

## Version bumps

- yamllint 1.25.0 to 1.26.0
- mypy 0.790 to 0.800
- pandas 1.2.0 to 1.2.1
- pytest-cov 2.10.1 to 2.11.1
- openpyxl 3.0.5 to 3.0.6

## Testing documentation uplift

- Added more comments to tests
- Updated tests documentation

## Added NOTICE

- Added NOTICE file to project

# 2021.01.16

## BREAKING CHANGES - Python 3.6 Support Depcrecated

- Due to an inherit [`pandas` dependency, python 3.6 support has been deprecated](https://pandas.pydata.org/pandas-docs/stable/whatsnew/v1.2.0.html#increased-minimum-version-for-python).

## Version bumps

- pandas 1.1.5 to 1.2.0
- nox 2020.8.22 to 2020.12.31

## Test Coverage Optimisations

- Ignore `codecov` analysis on motherstarter `setup.py` and `noxfile.py` files

# 2020.12.23

## Version bumps
- bandit 1.6.2 to bandit 1.7.0
- pandas 1.1.4 to 1.1.5
- pytest 6.1.2 to 6.2.1
- xlrd 1.20 to 2.0.1

## motherstarter excel functionality
- Migrated motherstarter input/output xlsx functions from `xlrd` to `openpyxl`

# 2020.11.16

- Uplifted documentation, including overview diagram, advanced usage and links to how-to videos.
- Resolved [pytest 6.1.2 issue](https://github.com/writememe/motherstarter/pull/29) by not calling pylama directly with the `make pytest` target.

# 2020.11.15
- Restoring changes implemented in 2020.11.13

# 2020.11.14
- Minor version bump to kickoff pypi packaging.
- Updating `TESTS.md` with extra aspects which need to be done.

# 2020.11.13
- Fixing issues whereby `source_dir` or `template_dir` did not work with the default supplied files provided inside the motherstarter package.
- Adjusted unit tests to replicate these changes

# 2020.11.10
- Updated README documentation to indicate it's installable via `pip`
- Removed old `templates/core/outputs` folder, not needed.
- Added `CONTRIBUTORS` documentation
- Added `MANIFEST.in` to make sure that the package_data is included.

# 2020.11.09
- Initial beta release, now ready for public visibility. Unit tests written, will need to be tested more thoroughly.
