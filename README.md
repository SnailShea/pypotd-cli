# PyPOTD CLI

## Description
Using the [pypotd](https://pypi.org/project/pypotd) library, pypotd-cli is a command-line tool to generate single or multiple ARRIS/CommScope-compatible password-of-the-day strings using a default or custom seed. Output defaults to JSON. Output can be written to a file, and will not output to console unless also provided with the verbose flag.

## Installation
```
pip install pypotd-cli
```

## Usage
```
usage: python -m pypotd-cli [-d DATE] [-D] [-f {json,text}] [-h] [-o OUT_FILE] [-r START END] [-s SEED] [-v]

Password-of-the-Day Generator for ARRIS/CommScope Devices

options:
  -d DATE, --date DATE                  generate a password for the given date
  -D, --des                             output des representation of seed
  -f {json,text}, --format {json,text}  password output format, either text or json
  -h, --help                            show this help message and exit
  -o OUT_FILE, --out-file OUT_FILE      password or list will be written to given filename
  -r START END, --range START END       generate a list of passwords given start and end dates
  -s SEED, --seed SEED                  string of 4-8 characters, used in password generation to mutate output
  -v, --verbose                         print output to console even when writing to file

If your seed uses special characters, you must surround it with quotes
```

## Examples
### Print password for current day using custom seed
```
$ python -m pypotd-cli -s test
{
  "09/27/23": "FP8992KBS5"
}
```

### Print DES for a custom seed
```
$ python -m pypotd-cli -s test -D
{
  "DES": "CD.7D.DE.86.D7.04.4A.85"
}
```

### Write a list of passwords to a file and print to console
```
$ python -m pypotd-cli -s test -r 2023-09-27 2023-09-30 -o range.json -v
{
  "09/27/23": "FP8992KBS5",
  "09/28/23": "JUSHXQ2S9O",
  "09/29/23": "9OTOUA0UI3",
  "09/30/23": "EDU83VUHE5"
}

$ cat ./range.json
{
  "09/27/23": "FP8992KBS5",
  "09/28/23": "JUSHXQ2S9O",
  "09/29/23": "9OTOUA0UI3",
  "09/30/23": "EDU83VUHE5"
}
```

### Previous example, but with formatted text output
```
$ python -m pypotd-cli -s test -r 2023-09-27 2023-09-30 -o range.txt -v -f text
09/27/23: FP8992KBS5
09/28/23: JUSHXQ2S9O
09/29/23: 9OTOUA0UI3
09/30/23: EDU83VUHE5

$ cat ./range.txt
09/27/23: FP8992KBS5
09/28/23: JUSHXQ2S9O
09/29/23: 9OTOUA0UI3
09/30/23: EDU83VUHE5
```