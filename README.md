# Patterns for Documenting Open Source Frameworks

## Requirements

* Python 3.6+
* <a href="https://python-poetry.org/docs/">Poetry</a>

## Installation

```shell
poetry install
```
## Metrics:
1. **Get events:**

   ```shell
   poetry run python3 scripts/get_events.py --id 11730342 --owner vuejs --name vue
   ```

2. **Standardize the events:**

    ```shell
    poetry run python3 scripts/standardise_data.py --id 11730342 --owner vuejs --name vue
    ```
    
3. **Calculate interpolation:**

    ```shell
    poetry run python3 scripts/standardise_data.py --id 11730342 --owner vuejs --name vue
    ```

 4. **Join previous events with interpolated events:**

    ```shell
    poetry run python3 scripts/join_files.py --id 11730342 --owner vuejs --name vue
    ```

### Notes:
* Lower bound: Repository creation date
* Upper bound: 2021-04-30
* Step-value: 3 months.
* The final JSON files are located in ```/data/final/{repository_name}.json```
* The data is downloaded from <a href="https://www.gharchive.org/">GH Archive</a>

## Visualization:
* The visualization notebooks (pattern adoption analysis and repository metrics) are located in ```/notebooks/```.

## Related documents:
* [A Review of Pattern Languages for Software Documentation](https://doi.org/10.1145/3424771.3424786) (EuroPLoP '20)
* [Patterns for Documenting Open Source Frameworks](https://hdl.handle.net/10216/135711) (Thesis)
* [Patterns for Documenting Open Source Frameworks](https://doi.org/10.48550/arXiv.2203.13871) (PLoP'21)
