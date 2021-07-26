from .app import build_parser, check_errors, process_args
from sys import argv


def main():
    parser = build_parser()
    args = parser.parse_args()

    check_errors(args)
    process_args(len(argv), args)


if __name__ == "__main__":
    main()
