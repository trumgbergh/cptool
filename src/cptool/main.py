import argparse
import os
import subprocess
import time
from datetime import datetime
from typing import Sequence, Optional
from cptool import handler
from cptool import cf

def elo_range(s: str) -> int:
    try:
        value = int(s)
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected interger, got {s!r}")

    if not 800 <= value <= 3500:
        raise argparse.ArgumentTypeError("out of range elo")
    return value

def problem_cnt(s: str) -> int:
    try:
        value = int(s)
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected interger, got {s!r}")

    if value < 0:
        raise argparse.ArgumentTypeError("number of problems have to be positive")
    return value


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command", required=True)
    train_parser = subparsers.add_parser("train")
    train_parser.add_argument('--min-elo',
                              type = elo_range,
                              default = 1500,
                              help = "Set the minimum difficulty of the problems (default = %(default)s, min 800 max 3500)",
                              )

    train_parser.add_argument('--max-elo',
                              type = elo_range,
                              default = 1900,
                              help = "Set the maximum difficulty of the problems (default = %(default)s, min 800 max 3500)",
                              )

    train_parser.add_argument('--dest',
                              type = str,
                              default = "~/competitive_programming/train_station",
                              help = "Set the destination folder for the training session")

    train_parser.add_argument('--cnt',
                              type = problem_cnt,
                              default = 1,
                              help = "Number of problems to solve in a training session (default = %(default)s, min 1 max inf)")

    args = parser.parse_args(argv)


    if args.command == "train":
        if args.min_elo > args.max_elo:
            raise argparse.ArgumentTypeError(f"Invalid range: min elo ({args.min_elo}) is higher than max elo ({args.max_elo}).")
        print("Starting training session...")
        print("Creating training folder...")
        folder_name = datetime.now().strftime("training_session-%Y-%m-%d_%H-%M")
        path = f"{args.dest}/{folder_name}"
        try:
            os.makedirs(path)
            print(f"Folder '{folder_name}' created successfully!")
        except FileExistsError:
            print(f"Folder '{folder_name}' already exists")
        # cf.update_problem_list((args.min_elo, args.max_elo))
        # cf.update_solved_problem_list()
        # for i in range(args.cnt):
        #     problem = cf.get_random_problem()
        #     problem_id = f"{problem['contestId']}{problem['index']}"
        #     problem_link = f"https://codeforces.com/contest/{problem['contestId']}/problem/{problem['index']}"
        #     print(f"Problem {i + 1}: {problem_id}  {problem['name']}")
        #     print(f"Problem link: {problem_link}")
        #     print(f"Setting up working folder...")
        #     template_path = os.path.expanduser(f"{args.dest}/template")
        #     work_path = os.path.expanduser(f"{path}/{problem_id}")
        #
        #     subprocess.run(["cp", "-r", template_path, work_path], check=True)
        #     print(f"Use the competitive companion on the webbrowser - Listening for input and output...")
        #     handler.listen_once()
        #
        #     print("GLHF")
        #     while cf.get_verdict(problem_id) is not True:
        #         time.sleep(5)
        # print("gg")
    return 0

if __name__ == "__main__":
    exit(main())
