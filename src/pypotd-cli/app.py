from argparse import ArgumentParser
from datetime import date
from json import dumps, loads
from re import match
from pypotd import (DATE_REGEX, DEFAULT_DATE, generate,
                    generate_multiple, is_valid_range)
from sys import exit


def date_format(date):
    date_chunks = date.split("-")
    month = date_chunks[1]
    day = date_chunks[2]
    year = date_chunks[0][2:]
    formatted_date = f"{month}/{day}/{year}"
    return formatted_date


OUTPUT_TOP = "Date    : Password of the Day\n-----------------------------\n"
_DEFAULT_DATE = DEFAULT_DATE
DEFAULT_DATE = date_format(_DEFAULT_DATE)


def build_parser():
    # TODO: -q, --quiet (with -f/--file only)
    # TODO: -o, --output-format (json/plain, with -f/--file only)
    parser = ArgumentParser(
        description="ARRIS Password-of-the-Day generator",
        prog="python -m pypotd-cli",
        epilog="If your seed uses special characters, you must quote it",
        add_help=False)
    parser.add_argument("-b",
                        "--begin",
                        help="first date of range (requires end date)")
    parser.add_argument("-d",
                        "--date",
                        help="single date to generate password for")
    parser.add_argument("-e",
                        "--end",
                        help="last date of range (requires beginning date)")
    parser.add_argument("-f",
                        "--file",
                        help="output password content to specified filename")
    parser.add_argument("-h",
                        "--help",
                        action="help",
                        help="show this help message and exit")
    parser.add_argument("-o",
                        "--output-format",
                        help="options: \"text\" or \"json\"")
    parser.add_argument("-q",
                        "--quiet",
                        help="used with -f, no consle output",
                        action="store_true")
    parser.add_argument("-s",
                        "--seed",
                        help="string (4-8 chars), changes password output")
    return parser


def check_errors(args):
    # Validate arguments
    if args.date and (args.begin or args.end):
        print("Cannot generate password as both range and single date")
        exit(1)
    elif args.date and not match(DATE_REGEX, args.date):
        print(f"Invalid isoformat string: '{args.date}' (date)")
        exit(1)
    elif args.begin and not args.end:
        print("Cannot specify begin date without end date")
        exit(1)
    elif args.end and not args.begin:
        print("Cannot specify end date without begin date")
        exit(1)
    elif args.begin and args.end:
        # This may need to be try/except for value error
        begin = args.begin
        end = args.end
        try:
            begin = date.fromisoformat(args.begin)
        except ValueError as e:
            print(f"{e} (begin)")
            exit(1)
        try:
            end = date.fromisoformat(args.end)
        except ValueError as e:
            print(f"{e} (end)")
            exit(1)
        try:
            is_valid_range(begin, end)
        except ValueError as e:
            print(e)
            exit(1)
    elif args.seed and (len(args.seed) < 4 or len(args.seed) > 8):
        print("Seed must be between 4-8 characters")
        exit(1)
    elif args.output_format and args.output_format not in ("text", "json"):
        print("Valid output formats are \"json\" or \"text\"")
        exit(1)
    elif args.quiet and not args.file:
        print("Quiet mode without a file will result in no output")
        exit(1)


def manage_output(args, potd, potd_date=DEFAULT_DATE):
    # TODO single date json
    if args.output_format == "json":
        if type(potd) == str:
            output = {}
            output[potd_date] = potd
        else:
            output = potd
    else:
        if type(potd) == str:
            output = f"{OUTPUT_TOP}{potd_date}: {potd}"
        elif type(potd) == dict:
            output = f"{OUTPUT_TOP}"
            for obj in potd.keys():
                output += f"{obj}: {potd[obj]}\n"
    if args.file:
        with open(args.file, "w") as file:
            if args.output_format == "json":
                contents = dumps(output, indent=4, sort_keys=True)
                file.write(f"{contents}\n")
            else:
                file.write(output)
        if not args.quiet:
            if args.output_format == "json":
                contents = dumps(output, indent=4, sort_keys=True)
                print(contents)
            else:
                print(output)
    else:
        if type(output) == str:
            print(output)
        else:
            print(dumps(output, sort_keys=True, indent=4))


def process_args(arg_count, args):
    if arg_count == 1:
        potd = generate()
        # Default to text output
        output = f"{OUTPUT_TOP}{DEFAULT_DATE}: {potd}"
        print(output)
    elif args.output_format == "json" and not \
            (args.seed or args.date or args.begin or args.end):
        potd = generate()
        manage_output(args, potd)
    elif args.output_format == "json" and (args.date or args.seed):
        try:
            formatted_date = date_format(args.date)
        except AttributeError:
            formatted_date = DEFAULT_DATE
        if args.seed and args.date:
            potd = generate(potd_date=args.date, seed=args.seed)
        elif args.seed and not args.date:
            if args.begin and args.end:
                potd = generate_multiple(start_date=args.begin,
                                         end_date=args.end,
                                         seed=args.seed)
            else:
                potd = generate(seed=args.seed)
        elif args.date and not args.seed:
            potd = generate(potd_date=args.date)
        manage_output(args, potd, potd_date=formatted_date)
    elif args.output_format == "text" and not \
            (args.seed or args.date or args.begin or args.end):
        potd = generate()
        output = f"{OUTPUT_TOP}{DEFAULT_DATE}: {potd}"
        manage_output(args, potd)
    elif args.seed and args.date:
        potd = generate(potd_date=args.date, seed=args.seed)
        manage_output(args, potd, potd_date=date_format(args.date))
    elif args.seed and not (args.date or args.begin or args.end):
        potd = generate(seed=args.seed)
        manage_output(args, potd)
    elif args.date and not args.seed:
        potd = generate(potd_date=args.date)
        manage_output(args, potd, potd_date=date_format(args.date))
    elif args.begin and args.end and args.seed:
        potd = generate_multiple(start_date=args.begin,
                                 end_date=args.end,
                                 seed=args.seed)
        manage_output(args, potd)
    elif args.begin and args.end and not args.seed:
        potd = generate_multiple(start_date=args.begin,
                                 end_date=args.end)
        manage_output(args, potd)
