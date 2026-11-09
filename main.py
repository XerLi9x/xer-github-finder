import argparse

from cli import main as cli_main
from web import app


def main():
    parser = argparse.ArgumentParser(
        description="Xer GitHub Finder"
    )

    mode = parser.add_mutually_exclusive_group(required=True)

    mode.add_argument(
        "--cli",
        action="store_true",
        help="Run terminal interface"
    )

    mode.add_argument(
        "--web",
        action="store_true",
        help="Run web dashboard"
    )

    args = parser.parse_args()

    if args.cli:
        cli_main()

    elif args.web:
        print("Starting Xer GitHub Finder Web Dashboard...")
        app.run(
            host="127.0.0.1",
            port=5000,
            debug=False
        )


if __name__ == "__main__":
    main()

