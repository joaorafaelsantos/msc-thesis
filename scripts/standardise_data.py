import argparse
import os
import json

# Arguments processing (repo info - id, owner and name)
parser = argparse.ArgumentParser(
    description="Standardise repo events into one unique format"
)
parser.add_argument("--id", help="ID of the repo (e.g. 10270250)", default="10270250")
parser.add_argument(
    "--owner", help="Owner of the repo (e.g. facebook)", default="facebook"
)
parser.add_argument("--name", help="Name of the repo (e.g. react)", default="react")
args = parser.parse_args()

repo = {"id": args.id, "owner": args.owner, "name": args.name}


def get_parsed_event(event):
    return {
        "size": event["size"],
        "stargazers": event.get("stargazers_count", False)
        or event.get("stargazers", 0),
        "forks": event["forks"],
        "open_issues": event["open_issues"],
    }


def get_event_from_file(file):
    with open(file) as read_file:
        return json.load(read_file)


def save_parsed_event_to_file(parsed_event, file):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, "w") as save_file:
        json.dump(parsed_event, save_file)


directory = f"data/raw/{repo['name']}"
for file_name in os.listdir(directory):
    if file_name.endswith(".json"):
        event = get_event_from_file(f"{directory}/{file_name}")
        parsed_event = get_parsed_event(event)
        save_directory = f"data/standardised/{repo['name']}"
        save_parsed_event_to_file(parsed_event, f"{save_directory}/{file_name}")

# interpolation data
directory = f"data/raw/{repo['name']}/interpolation"
if os.path.isdir(directory):
    for folder_name in os.listdir(directory):
        for file_name in os.listdir(f"{directory}/{folder_name}"):
            event = get_event_from_file(f"{directory}/{folder_name}/{file_name}")
            parsed_event = get_parsed_event(event)
            save_directory = (
                f"data/standardised/{repo['name']}/interpolation/{folder_name}"
            )
            save_parsed_event_to_file(parsed_event, f"{save_directory}/{file_name}")
