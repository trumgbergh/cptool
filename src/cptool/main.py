import argparse
from typing import Sequence
from cptool import handler
from cptool import cf

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command", required=True)
    train_parser = subparsers.add_parser("train")

