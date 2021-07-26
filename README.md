# PyPOTD CLI
# TODO: -b -e -f -o -q -s

## Description
Using the [pypotd](https://pypi.org/project/pypotd) library, pypotd-cli is a command-line tool
to generate single or multiple ARRIS-compatible password-of-the-day strings.

## Installation
```
pip install pypotd-cli
```

## Usage
```
usage: python -m pypotd-cli [-b BEGIN] [-d DATE] [-e END] [-f FILE] [-h]
                          [-o OUTPUT_FORMAT] [-q] [-s SEED]

ARRIS Password-of-the-Day generator

optional arguments:
  -b BEGIN, --begin BEGIN
                        first date of range (requires end date)
  -d DATE, --date DATE  single date to generate password for
  -e END, --end END     last date of range (requires beginning date)
  -f FILE, --file FILE  output password content to specified filename
  -h, --help            show this help message and exit
  -o OUTPUT_FORMAT, --output-format OUTPUT_FORMAT
                        options: "text" or "json"
  -q, --quiet           used with -f, no consle output
  -s SEED, --seed SEED  string (4-8 chars), changes password output

If your seed uses special characters, you must quote it
```