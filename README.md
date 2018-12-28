# taiga-query
Query Taiga Project

taiga-query is a CLI based tool for getting data from Taiga board.
It runs python-taiga API to build queries for retrieving data from
Taiga endpoints. The tool can be used for collecting statistics and
metrics from projects tracked in Taiga.

     _        _
    | |_ __ _(_) __ _  __ _        __ _ _   _  ___ _ __ _   _
    | __/ _` | |/ _` |/ _` |_____ / _` | | | |/ _ \ '__| | | |
    | || (_| | | (_| | (_| |_____| (_| | |_| |  __/ |  | |_| |
     \__\__,_|_|\__, |\__,_|      \__, |\__,_|\___|_|   \__, |
                |___/                |_|                |___/

                    taiga-query, a metrics tool
            https://github.com/rafaelfolco/taiga-query

## Output sample
```sh
python taiga-query.py -o
2018-12-27 23:55:23,263 INFO __main__:  Sprint: [ Unified Sprint 3 ] | https://tree.taiga.io/project/tripleo-ci-board/taskboard/unified-sprint-3
2018-12-27 23:55:23,264 INFO __main__:  Getting orphan user stories...
+-------+------------------------------------------------------------------------------------------+----------+---------------+
|   ref | subject                                                                                  | status   | assigned_to   |
+=======+==========================================================================================+==========+===============+
|   528 | Regression Tests on Reproducer                                                           | To Do    |               |
+-------+------------------------------------------------------------------------------------------+----------+---------------+
|   333 | Letfovers from #192 Iterate on fedora 28 standalone job to bring it to completion        | To Do    |               |
+-------+------------------------------------------------------------------------------------------+----------+---------------+
|   531 | Add standalone scenario001 across TripleO projects make it voting and qe/sanity check it | To Do    |               |
+-------+------------------------------------------------------------------------------------------+----------+---------------+
|   532 | Add standalone scenario002 across TripleO projects                                       | To Do    |               |
+-------+------------------------------------------------------------------------------------------+----------+---------------+
|   533 | Add standalone scenario003 across TripleO projects                                       | To Do    |               |
+-------+------------------------------------------------------------------------------------------+----------+---------------+
```

## Install
git clone git@github.com:rafaelfolco/taiga-query.git
cd taiga-query
pip install -r requirements.txt

## Requirements
* requirements.txt
* python 2.7

## Setup
Set `TAIGA_USERNAME` and `TAIGA_PASSWORD` environment variables
to authenticate on Taiga.

```sh
    source credentials.sh
```
See credentials.sh for an example.

## Usage
```sh
    taiga-query.py
```
This retrieves all user stories from current sprint.

### Flags
```
python taiga-query.py -h
usage: taiga-query.py [-h] [-o] [-s SPRINT] [-d]

Query user stories from Taiga project

optional arguments:
  -h, --help            show this help message and exit
  -o, --orphan          Search for orphan user stories (without
                        owner/assigned_to)
  -s SPRINT, --sprint SPRINT
                        Specify the sprint to search
  -d, --debug           Enable DEBUG mode.
```

### Orphan user stories
```sh
    taiga-query.py --orphan
```
This gets only user stories that have no owner (`assigned_to=None`).

## Limitations

* Queries are limited to current sprint (`--sprint` does NOT work)
* Performance

## Future Implementations

### Feature Requests (TODOs)

* List sprints
* Query tasks and epics
* Query Issues
* Query stories from a given sprint
* Query stories from a date range
* Retrieve more data from stories
* Query completed and unfinished work from sprint
* Query last modified tasks
* Report with all work items from a sprint
* Query unclosed items from previous sprints
* HTML reports with hyperlinks

### Structural

* Code class design
* Split functions into separate files
* Performance improvements for queries
* Unit tests
* Python3

