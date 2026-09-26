
import argparse
from pathlib import Path
import ipaddress

def parse_endpoint(value: str) -> tuple[ipaddress.IPv4Address, int | None]:
    host, separator, port = value.partition(":")

    try:
        address = ipaddress.IPv4Address(host)
    except ipaddress.AddressValueError as e:
        raise argparse.ArgumentTypeError(
            f"Invalid IPv4 address: {host}"
        )

    if not separator:
        return address, None

    try:
        port_number = int(port)
    except ValueError as e:
        raise argparse.ArgumentTypeError(
            f"Invalid port: {port}"
        )

    return address, port_number

def parse_args():
    parser = argparse.ArgumentParser(
        description="A peer-to-peer file synchronization system in Python."
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    serve_parser = subparsers.add_parser(
        "serve",
        help="Start the server",
        description="Start the application server",
    )

    serve_parser.add_argument(
        "shared_directory",
        type=Path,
        help="Path to the folder to be shared",
    )

    parser.add_argument(
    "--listen",
    type=parse_endpoint,
    metavar="HOST[:PORT]",
    help="Listener address (default: 127.0.0.1:9000)",
)

parser.add_argument(
    "--remote",
    type=parse_endpoint,
    required=True,
    metavar="HOST[:PORT]",
    help="Remote address; port defaults to listener port",
)

    args = parser.parse_args()

    if args.command == "serve":
        args.root = args.root.resolve()

    return args


def serve(root: Path, port: int) -> None:
    print(f"Root folder: {root}")
    print(f"Port:        {port}")


def main() -> None:
    args = parse_args()

    if args.command == "serve":
        serve(args.root, args.port)


if __name__ == "__main__":
    main()