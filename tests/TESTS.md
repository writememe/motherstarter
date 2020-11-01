# Testing Documentation

This page is here to document how testing is performed for `motherstarter`. It forms as a living documentation for status of tests written.

## Testing Structure

Unit tests
End-to-end tests
Output tests

### Test inputs

- Perform tests for the following scenarios:
    - Test log level (default)
    - Test log level (all types)
    - Take bad log level input
    - Test source_directory (default)
    - Test source_directory (custom)
    - Test bad source_directory input
    - Test source_type (default)
    - Test source_type (all types)
    - Test bad source_directory input
    - Test output type (custom)
    - Test output type (all types)
    - Test bad output type

### Test outputs
- Perform tests for the following scenarios:
    - Test output files are present
    - Test output files are valid by reading content
    - Test output files that input details much output values (i.e. input inventory[0] == output inventory[0])
    - Test output files that input details much output count (4 devices read in, there should be 4 devices outputted)

### Test logging
    - Test log file is logging correctly by generating a log file
    - Read log file and look for certain values in the file
    - Not sure if much else is needed here?