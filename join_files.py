import os
import json
from datetime import datetime

repos = [
    {
        "name": "vue"
    },
    {
        "name": "react"
    },
    # {
    #     "name": "angular"
    # },
    # {
    #     "name": "laravel"
    # },
    # {
    #     "name": "next.js"
    # },
]


def get_event_from_file(file):
    with open(file) as read_file:
        return json.load(read_file)


def save_parsed_event_to_file(parsed_event, file):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, 'w') as save_file:
        json.dump(parsed_event, save_file)


for repo in repos:

    repo_events = []
    directory = f"downloaded_data/step3/{repo['name']}"
    for file_name in os.listdir(directory):
        if file_name.endswith(".json"):
            event = get_event_from_file(f"{directory}/{file_name}")
            event["date"] = file_name.removesuffix(".json")
            repo_events.append(event)
    sorted_repo_events = sorted(
        repo_events,
        key=lambda e: datetime.strptime(e['date'], '%Y-%m-%d')
    )
    save_parsed_event_to_file(sorted_repo_events, f"downloaded_data/step4/{repo['name']}.json")
