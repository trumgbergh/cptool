import pprint
import random
import csv
import time
import os.path
from typing import Optional, Sequence

import requests

user = "Voltair"
CFAPI = "https://codeforces.com/api"

def get_submission(cnt):
    s = str(cnt)
    print("Last " + s + " submission(s):\n")
    r = requests.get(f"{CFAPI}/user.status?handle=" + user + "&from=1&count=" + s)
    f = r.json()
    print(f["status"])
    if f["status"] != "OK":
        print("Failed to get submission data saj")
        return

    # for submission in f["result"]:
    #     idx = submission["problem"]["index"]
    #     name = submission["problem"]["name"]
    #     verdict = submission["verdict"]
    #     if verdict == "OK":
    #         print(f"{idx}. {name}   |    Verdict: {verdict}")
    #     else:
    #         test_passed = submission["passedTestCount"]
    #         print(
    #             f"{idx}. {name}   |    Verdict: {verdict}, Test passed: {test_passed}"
    #         )
    return f["result"]

def get_verdict(problem_id):
    last_sub = -1
    r = requests.get(f"{CFAPI}/user.status?handle=" + user + "&from=1&count=1")
    f = r.json()
    if f["status"] != "OK":
        print("Failed to get submission data saj")
        return
    sub = f["result"]
    recent_prob = f"{sub['problem']['contestId']}{sub['problem']['index']}"
    if recent_prob != problem_id or sub["id"] == last_sub:
        return
    last_sub = sub["id"]
    idx = sub["problem"]["index"]
    name = sub["problem"]["name"]
    verdict = sub["verdict"]
    if verdict == "OK":
        print(f"{idx}. {name}   |    Verdict: {verdict}")
        return True
    else:
        test_passed = sub["passedTestCount"]
        print(
            f"{idx}. {name}   |    Verdict: {verdict}, Test passed: {test_passed}"
        )
    return False



def update_solved_problem_list():
    r = requests.get(f"{CFAPI}/user.status?handle=" + user + "&from=1")
    f = r.json()

    solved_problem = set()
    for sub in f["result"]:
        if sub["verdict"] == "OK":
            s = str(sub["contestId"]) + str(sub["problem"]["index"])
            solved_problem.add(s)
    with open('solved_list.csv', 'w', newline = '') as file:
        writer = csv.writer(file)
        writer.writerow(["problem_id"])

        for problem_id in solved_problem:
            writer.writerow([problem_id])

def get_solved():
    if not os.path.exists('./solved_list.csv'):
        print("There is no solved problem list, creating one now...")
        update_solved_problem_list()
        print("Created solved_list.csv.")
    solved_problem = set()
    with open("solved_list.csv", "r", newline="") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            solved_problem.add(row[0])
    return solved_problem

def update_problem_list(elo_range: tuple[int, int] = (1500, 1900)):
    solved_problems = get_solved()
    r = requests.get(f"{CFAPI}/problemset.problems")
    if r.status_code != 200:
        print("Failed to get problemset data")
        return
    print("Got problemset data")
    f = r.json()
    if f["status"] != "OK":
        return

    all_problems = f["result"]["problems"]
    valid_problems = []
    for p in all_problems:
        if "rating" in p and (elo_range[0] <= p["rating"] <= elo_range[1]):
            problem_name = f"{p['contestId']}{p['index']}"
            if problem_name not in solved_problems:
                valid_problems.append(p)
    fieldnames = ["contestId", "index", "name", "rating"]

    with open("problem_list.csv", mode = "w", newline = "") as file:
        writer = csv.DictWriter(file, fieldnames = fieldnames, extrasaction = 'ignore')
        writer.writeheader()
        writer.writerows(valid_problems)

def get_problem_list():
    if not os.path.exists('./problem_list.csv'):
        print("There is no problem list, creating one now...")
        update_problem_list()
        print("Created problem_list.csv.")
    problem_list = []
    with open("problem_list.csv", "r", newline="") as file:
        reader = csv.DictReader(file)
        problem_list = list(reader)
    return problem_list

def get_random_problem():
    valid_problems = get_problem_list()
    problem = random.choice(valid_problems)
    return problem

def main(agrv: Optional[Sequence[str]] = None) -> int:
    get_random_problem()

if __name__ == "__main__":
    exit(main())
