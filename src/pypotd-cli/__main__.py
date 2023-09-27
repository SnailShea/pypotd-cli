def main():
    from argparse import ArgumentParser
    from pypotd import (
        DEFAULT_SEED,
        generate,
        generate_multiple,
        seed_to_des,
        validate_date,
        validate_date_range,
        validate_seed,
    )

    p = ArgumentParser(
        add_help=False,
        description="Password-of-the-Day Generator for ARRIS/CommScope Devices",
        epilog="If your seed uses special characters, you must surround it with quotes",
        prog="pypotd-cli",
    )
    megroup = p.add_mutually_exclusive_group()
    megroup.add_argument("-d", "--date", help="generate a password for a single date")
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
    p.add_argument("-o", "--out-file", help="output password or list to given filename")
    megroup.add_argument(
        "-r",
        "--range",
        metavar=("START", "END"),
        help="generate a list of passwords given start and end dates",
        nargs=2,
    )
    p.add_argument("-s", "--seed", help="string (4-8 chars), changes password output")
    args = p.parse_args()
    out_format = args.format or "json"
    out_file = args.out_file or None
    seed = args.seed or DEFAULT_SEED
    data = {}
    if seed != DEFAULT_SEED:
        try:
            validate_seed(args.seed)
        except ValueError as e:
            print(str(e))
            return
    data["seed"] = seed
    if args.des == True:
        des = seed_to_des(args.seed)
        data["des"] = des
    if args.date:
        try:
            validate_date(args.date)
        except ValueError as e:
            print(str(e))
            return
        data[args.date] = generate(date=args.date, seed=data["seed"])
        # We have enough information to produce output, handle how
    if args.range:
        try:
            start, end = args.range
            validate_date_range(start, end)
        except ValueError as e:
            print(str(e))
            return
        data.update(generate_multiple(start, end, seed=data["seed"]))
    generate_output(data, out_format, out_file=out_file)


def generate_output(data, out_format, out_file=None):
    seedless = lambda _data: {
        key.upper(): _data[key] for key in _data.keys() if key != "seed"
    }
    listed = lambda _data: [[key, _data[key]] for key in _data]
    formatted = lambda _data: [f"{i[0]}: {i[1]}" for i in _data]
    data = seedless(data)
    if out_format == "text":
        if len(data.keys()) > 1:
            output = "\n".join(formatted(listed(data)))
        else:
            k, v = list(data.keys())[0], list(data.values())[0]
            output = f"{k}: {v}"
    if out_format == "json":
        from json import dumps

        output = dumps(data, indent=2)
    print(output)


if __name__ == "__main__":
    main()
