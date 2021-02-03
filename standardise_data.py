import os
import json

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

def get_parsed_event(event):
    return {
        "size": event["size"],
        "stargazers": event.get('stargazers_count', False) or event["stargazers"],
        "forks": event["forks"],
        "open_issues": event["open_issues"]
    }


def get_event_from_file(file):
    with open(file) as read_file:
        return json.load(read_file)


def save_parsed_event_to_file(parsed_event, file):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, 'w') as save_file:
        json.dump(parsed_event, save_file)


for repo in repos:
    directory = f"downloaded_data/step1/{repo['name']}"
    for file_name in os.listdir(directory):
        if file_name.endswith(".json"):
            event = get_event_from_file(f"{directory}/{file_name}")
            parsed_event = get_parsed_event(event)
            save_directory = f"downloaded_data/step2/{repo['name']}"
            save_parsed_event_to_file(parsed_event, f"{save_directory}/{file_name}")

    # interpolation data
    directory = f"downloaded_data/step1/{repo['name']}/interpolation"
    for folder_name in os.listdir(directory):
        for file_name in os.listdir(f"{directory}/{folder_name}"):
            event = get_event_from_file(f"{directory}/{folder_name}/{file_name}")
            parsed_event = get_parsed_event(event)
            save_directory = f"downloaded_data/step2/{repo['name']}/interpolation/{folder_name}"
            save_parsed_event_to_file(parsed_event, f"{save_directory}/{file_name}")
