import gzip
import json
import os
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta

repos = [
    # {
    #     "id": 11730342,
    #     "owner": "vuejs",
    #     "name": "vue"
    # },
    # {
    #     "id": 10270250,
    #     "owner": "facebook",
    #     "name": "react"
    # },
    # {
    #     "id": 24195339,
    #     "owner": "angular",
    #     "name": "angular"
    # },
    {
        "id": 1863329,
        "owner": "laravel",
        "name": "laravel"
    },
    # {
    #     "id": 70107786,
    #     "owner": "vercel",
    #     "name": "next.js"
    # },
]

allowed_event_types = ["PullRequestEvent", "PullRequestReviewCommentEvent"]
# end_date = datetime.strptime("2020-12-31T14:46:03Z", "%Y-%m-%dT%H:%M:%SZ")
end_date = datetime.strptime("2012-12-04T14:46:03Z", "%Y-%m-%dT%H:%M:%SZ")


def get_events_with_metrics(event, repo_id, date):
    if date <= datetime(2014, 12, 31):
        if "repository" in event and "id" in event["repository"] and event["repository"]["id"] == repo_id:
            return event["repository"]
        elif "repo" in event and "id" in event["repo"] and event["repo"]["id"] == repo_id:
            return event
    else:
        if event["repo"]["id"] == repo_id and event["type"] in allowed_event_types:
            return event["payload"]["pull_request"]["base"]["repo"]

    return None


def get_day_events(day, repo):
    events = []
    for hour in range(24):
        archive_url = f"https://data.gharchive.org/{day.strftime('%Y-%m-%d')}-{hour}.json.gz"
        gz_file = requests.get(archive_url, stream=True)

        try:
            with gzip.open(gz_file.raw, 'rt', encoding='UTF-8') as ndjson:
                for line in ndjson:
                    event = json.loads(line)
                    event = get_events_with_metrics(event, repo["id"], current_date)
                    if event is not None:
                        events.append(event)
        except ValueError as e:
            # current_date = current_date + relativedelta(days=+1)
            break

    return events


def save_events_to_file(events, filename, date):
    print(f"Data found for {date}")

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as file:
        json.dump(events[-1], file)


for repo in repos:
    url = f"https://api.github.com/repos/{repo['owner']}/{repo['name']}"

    payload = requests.get(url)
    created_at = payload.json()["created_at"]
    # created_at = "2019-05-24T16:15:54Z"
    created_at = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
    # The first day to be crawled is exactly 3 months after the initial repository date
    current_date = created_at + relativedelta(months=+3)

    while (end_date - current_date).total_seconds() > 0:
        print(f"Trying to get {current_date}")
        events = get_day_events(current_date, repo)

        if len(events) > 0:

            filename = f"downloaded_data/step1/{repo['name']}/{current_date.strftime('%Y-%m-%d')}.json"
            save_events_to_file(events, filename, current_date)
            current_date += relativedelta(months=+3)

        else:
            print(f"Not found data for {current_date}")
            has_events_immediately_before = False
            has_events_immediately_after = False
            day_immediately_before = current_date
            day_immediately_after = current_date

            while not has_events_immediately_before:
                day_immediately_before += relativedelta(days=-1)
                print(f"Trying to get {day_immediately_before} * before")
                events = get_day_events(day_immediately_before, repo)
                if len(events) > 0:
                    filename = f"downloaded_data/step1/{repo['name']}/interpolation/{current_date.strftime('%Y-%m-%d')}/{day_immediately_before.strftime('%Y-%m-%d')}.json"
                    save_events_to_file(events, filename, day_immediately_before)
                    has_events_immediately_before = True

            while not has_events_immediately_after:
                day_immediately_after += relativedelta(days=+1)
                print(f"Trying to get {day_immediately_after} * after")
                events = get_day_events(day_immediately_after, repo)
                if len(events) > 0:
                    filename = f"downloaded_data/step1/{repo['name']}/interpolation/{current_date.strftime('%Y-%m-%d')}/{day_immediately_after.strftime('%Y-%m-%d')}.json"
                    save_events_to_file(events, filename, day_immediately_after)
                    has_events_immediately_after = True

            if has_events_immediately_before and has_events_immediately_after:
                current_date += relativedelta(months=+3)
