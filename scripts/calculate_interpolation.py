import argparse
import os
import json
import scipy.interpolate
from datetime import datetime
import numpy as np
import shutil

# Arguments processing (repo info - id, owner and name)
parser = argparse.ArgumentParser(
    description="Calculate interpolation of missing repo events"
)
parser.add_argument("--id", help="ID of the repo (e.g. 10270250)", default="10270250")
parser.add_argument(
    "--owner", help="Owner of the repo (e.g. facebook)", default="facebook"
)
parser.add_argument("--name", help="Name of the repo (e.g. react)", default="react")
args = parser.parse_args()

repo = {"id": args.id, "owner": args.owner, "name": args.name}


def get_event_from_file(file):
    with open(file) as read_file:
        return json.load(read_file)


def get_rounded_int(num):
    return int(np.rint(num))


def save_parsed_event_to_file(parsed_event, file):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, "w") as save_file:
        json.dump(parsed_event, save_file)


# copy files
shutil.copytree(
    f"data/standardised/{repo['name']}",
    f"data/interpolation/{repo['name']}",
    ignore=shutil.ignore_patterns("interpolation"),
)

# interpolation data
directory = f"data/standardised/{repo['name']}/interpolation"
if os.path.isdir(directory):
    for folder_name in os.listdir(directory):
        points = {
            "dates": [],
            "x": [],
            "size": [],
            "stargazers": [],
            "forks": [],
            "open_issues": [],
        }
        for i, file_name in enumerate(sorted(os.listdir(f"{directory}/{folder_name}"))):
            save_directory = f"data/interpolation/{repo['name']}"
            event = get_event_from_file(f"{directory}/{folder_name}/{file_name}")

            date = datetime.strptime(file_name[:-5], "%Y-%m-%d")
            points["dates"].append(date)
            points["size"].append(event["size"])
            points["stargazers"].append(event["stargazers"])
            points["forks"].append(event["forks"])
            points["open_issues"].append(event["open_issues"])

        delta = points["dates"][1] - points["dates"][0]
        wanted_date = datetime.strptime(folder_name, "%Y-%m-%d")
        delta2 = wanted_date - points["dates"][0]
        points["x"] = [0, delta.days]

        size = scipy.interpolate.interp1d(points["x"], points["size"])
        stargazers = scipy.interpolate.interp1d(points["x"], points["stargazers"])
        forks = scipy.interpolate.interp1d(points["x"], points["forks"])
        open_issues = scipy.interpolate.interp1d(points["x"], points["open_issues"])

        event = {
            "size": get_rounded_int(size(delta2.days)),
            "stargazers": get_rounded_int(stargazers(delta2.days)),
            "forks": get_rounded_int(forks(delta2.days)),
            "open_issues": get_rounded_int(open_issues(delta2.days)),
        }

        save_directory = f"data/interpolation/{repo['name']}"
        save_parsed_event_to_file(event, f"{save_directory}/{folder_name}.json")
