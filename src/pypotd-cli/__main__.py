def main():
    from pypotd import DEFAULT_SEED

    p = build_parser()
    args = p.parse_args()
    out_format = args.format or "json"
    out_file = args.out_file or None
    seed = args.seed or DEFAULT_SEED
    verbose = args.verbose or False
    data = parse_arguments(args, seed)
    generate_output(data, out_format, out_file=out_file, verbose=verbose)


def build_parser():
    from argparse import ArgumentParser, HelpFormatter
    from functools import partial

    p = ArgumentParser(
        add_help=False,
        description="Password-of-the-Day Generator for ARRIS/CommScope Devices",
        epilog="If your seed uses special characters, you must surround it with quotes",
        prog="python -m pypotd-cli",
    )
    p.formatter_class = partial(HelpFormatter, max_help_position=80)
    megroup = p.add_mutually_exclusive_group()
    megroup.add_argument("-d", "--date", help="generate a password for the given date")
    megroup.add_argument(
        "-D", "--des", help="output des representation of seed", action="store_true"
    )
    p.add_argument(
        "-f",
        "--format",
        choices=["json", "text"],
        help="password output format, either text or json",
    )
    p.add_argument(
        "-h", "--help", action="help", help="show this help message and exit"
    )
    p.add_argument(
        "-o", "--out-file", help="password or list will be written to given filename"
    )
    megroup.add_argument(
        "-r",
        "--range",
        metavar=("START", "END"),
        help="generate a list of passwords given start and end dates",
        nargs=2,
    )
    p.add_argument(
        "-s",
        "--seed",
        help="string of 4-8 characters, used in password generation to mutate output",
    )
    p.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="print output to console even when writing to file",
    )
    return p


def parse_arguments(args, seed):
    from datetime import datetime
    from pypotd import (
        DEFAULT_SEED,
        generate,
        generate_multiple,
        seed_to_des,
        validate_date,
        validate_seed,
        validate_date_range,
    )
    from sys import exit

    data = {}
    if seed != DEFAULT_SEED:
        try:
            validate_seed(args.seed)
        except ValueError as e:
            exit(e)
    data["seed"] = seed
    if args.des == True:
        des = seed_to_des(args.seed)
        data["des"] = des
    fmt = lambda _date: datetime.fromisoformat(_date).strftime("%m/%d/%y")
    if args.date:
        try:
            validate_date(args.date)
        except ValueError as e:
            exit(e)
        data[fmt(args.date)] = generate(date=args.date, seed=data["seed"])
    if args.range:
        try:
            start, end = args.range
            validate_date_range(start, end)
        except ValueError as e:
            exit(e)
        data.update(generate_multiple(start, end, seed=data["seed"]))
    if args.date == None and args.range == None and args.des == False:
        date = datetime.now().isoformat()[:10]
        data[fmt(date)] = generate(date=date, seed=data["seed"])
    return data


def generate_output(data, out_format, out_file=None, verbose=False):
    seedless = lambda _data: {
        key.upper(): _data[key] for key in _data.keys() if key != "seed"
    }
    data = seedless(data)
    output = format_output(data, out_format)
    if out_file:
        if verbose == True:
            print(output.rstrip("\n"))
        write_output(output, out_file)
    else:
        print(output.rstrip("\n"))


def format_output(data, out_format):
    from json import dumps

    if out_format == "text":
        if len(data.keys()) > 1:
            formatted = lambda _data: [f"{i[0]}: {i[1]}" for i in _data]
            listed = lambda _data: [[key, _data[key]] for key in _data]
            output = "\n".join(formatted(listed(data)))
            return f"{output}\n"
        else:
            key = next(iter(data))
            value = data[key]
            output = f"{key}: {value}\n"
            return output
    if out_format == "json":
        output = f"{dumps(data, indent=2)}\n"
        return output


def write_output(output, out_file):
    from os.path import exists, isfile
    from sys import exit

    if exists(out_file):
        if not isfile(out_file):
            exit(f"{out_file} exists and is not a file, refusing to write.")
        cont = input(
            f"{out_file} already exists, submit 'y' to continue or the enter key to abort: "
        )
        if cont != "y":
            exit(f"Unable to write to {out_file}, file exists.")
    try:
        with open(out_file, "w") as file:
            file.write(output)
    except PermissionError as e:
        exit(f"Permission denied, unable to write to {out_file}")


if __name__ == "__main__":
    main()
