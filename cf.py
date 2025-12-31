import pprint
import random
from typing import Optional, Sequence

import requests

user = "Voltair"
problem = set()
CFAPI = "https://codeforces.com/api"


def greetings():
    print("Hi ", user, "\n")


def space(cnt):
    return " " * cnt


def get_solved():
    r = requests.get(f"{CFAPI}/user.status?handle=" + user + "&from=1")
    f = r.json()
    cntp = 0
    for sub in f["result"]:
        cntp += 1
        if sub["verdict"] == "OK":
            s = str(sub["contestId"]) + str(sub["problem"]["index"])
            problem.add(s)
    return problem


def get_submission(cnt):
    s = str(cnt)
    print("Last " + s + " submission(s):\n")
    r = requests.get(f"{CFAPI}/user.status?handle=" + user + "&from=1&count=" + s)
    f = r.json()
    if f["status"] != "OK":
        print("Failed to get submission data saj")
        return

    for submission in f["result"]:
        idx = submission["problem"]["index"]
        name = submission["problem"]["name"]
        verdict = submission["verdict"]
        if verdict == "OK":
            print(f"{idx}. {name}   |    Verdict: {verdict}")
        else:
            test_passed = submission["passedTestCount"]
            print(
                f"{idx}. {name}   |    Verdict: {verdict}, Test passed: {test_passed}"
            )


def get_random_problem(elo_range: tuple[int, int] = (1500, 1900)):
    r = requests.get(f"{CFAPI}/problemset.problem")
    f = r.json()
    solved_problems = get_solved()
    print(solved_problems)
    if f["status"] != "OK":
        return
    all_problems = f["result"]["problems"]
    # valid_problems = []
    # for p in all_problems:

    # problem = random.choice(valid_problems)


def main(agrv: Optional[Sequence[str]] = None) -> int:
    # getSubmission(2)
    getRandomProblem()


if __name__ == "__main__":
    exit(main())
