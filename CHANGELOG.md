CHANGELOG
=======

# 2020.12.23

## Version bumps
- bandit 1.6.2 to bandit 1.7.0
- pandas 1.1.4 to 1.1.5
- pytest 6.1.2 to 6.2.1
- xlrd 1.20 to 2.0.1

## motherstarter excel functionality
- Migrated motherstarter input/output xlsx functions from `xlrd` to `colorama`

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