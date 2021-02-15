import argparse
import os
import json
from datetime import datetime

# Arguments processing (repo info - id, owner and name)
parser = argparse.ArgumentParser(
    description="Join all events files into one file separated by dates"
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


def save_parsed_event_to_file(parsed_event, file):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, "w") as save_file:
        json.dump(parsed_event, save_file)


repo_events = []
directory = f"data/interpolation/{repo['name']}"
for file_name in os.listdir(directory):
    if file_name.endswith(".json"):
        event = get_event_from_file(f"{directory}/{file_name}")
        event["date"] = file_name[:-5]
        repo_events.append(event)
sorted_repo_events = sorted(
    repo_events, key=lambda e: datetime.strptime(e["date"], "%Y-%m-%d")
)
save_parsed_event_to_file(sorted_repo_events, f"data/final/{repo['name']}.json")
