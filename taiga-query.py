"""taiga-query metrics tool"""

import sys
import os
import datetime
import logging
import argparse

from tabulate import tabulate
from taiga import TaigaAPI


# TripleO CI (production) 289231
PROJECT_SLUG = 'tripleo-ci-board'

def get_project(project_slug):
    """
    Retrieve project id for a given slug (board name)

    @param project_slug: Project board name

    @return: Returns a project id (integer)
    """

    project_id=api.projects.get_by_slug(project_slug).id
    message='project_id = %d, project" ' % project_id
    log.debug(message)
    message='https://tree.taiga.io/project/%s' % PROJECT_SLUG
    log.info(message)

    return project_id

def auth_taiga():
    """
    Authenticates user/password on taiga instance using pre-loaded
    env variables

    @param <none>

    @return: Returns a token id (string)
    """

    try:
        taiga_username=os.environ['TAIGA_USERNAME']
        taiga_password=os.environ['TAIGA_PASSWORD']
    except KeyError:
        log.error("Environment variables TAIGA_USERNAME and "
                  "TAIGA_PASSWORD must be set.")
        sys.exit(1)

    api.auth(username=taiga_username, password=taiga_password)

    message='User %s successfully authenticated.' % taiga_username
    log.debug(message)

    return api.token

def get_user_stories(project_id):
    """
    Retrieves user stories from Taiga

    @param project_id: Integer that uniquely identifies a project

    @return: Returns a list of user stories
    """

    return api.search(project_id).user_stories

def filter_user_stories(user_stories, **filters):
    """
    Retrieves a filtered list of user stories based on keyword args

    @param user_stories: List of user stories to filter from
    @param filters: keypair values to filter e.g. k1=v1, k2=v2 ...

    @return: Returns a list of filtered user stories
    """

    filtered_stories = []

    for us in user_stories:
        for key, value in filters.items():
            story_property = getattr(api.user_stories.get(us.id), key)
            message = 'User Story #%d : ref=%d key=%s value=%s' % (us.id,
                       us.ref, key, story_property)
            log.debug(message)
            if story_property is value:
                message = 'Adding US #%d to query result' % us.ref
                log.debug(message)
                filtered_stories.append(us)

    logging.debug('Filtered User Stories:')
    logging.debug(filtered_stories)

    return filtered_stories

def get_stories_data(user_stories, project_id, *fields):
    """
    Retrieves an user story array like:
    [["value1", "value2"], ["value3", "value4"]]
     \------ row 1 -----/  \----- row 2 ------/
    \----------------- array ------------------/

    @param user_stories: List of user stories to get data from
    @param project_id: Project id to get users and status info
    @param fields: comma separated set of fields to query

    @return: Returns an array of user story rows
    """

    users_dict = get_project_users(project_id)
    statuses_dict = get_story_statuses(project_id)

    us_array=[]
    for us in user_stories:
        us_row=[]
        for f in fields:
            us_property = getattr(api.user_stories.get(us.id), f)

            # Get status/user name from id
            if f == 'status':
                us_property = statuses_dict.get(us_property)
            if f == 'assigned_to':
                us_property = users_dict.get(us_property)

            us_row.append(us_property)
        us_array.append(us_row)

    return us_array

def print_user_stories(us_array, columns):
    """
    Prints an user story array like:
    +------------+------------+
    | column 1   | column 2   |
    +============+============+
    | value1     | value2     |
    +------------+------------+
    | value3     | value4     |
    +------------+------------+

    @param us_array: Array of user stories
    @param columns: List of columns (fields)

    @return: <none>
    """

    print tabulate(us_array, columns, tablefmt="grid")

def get_current_sprint(project_id):
    """
    Retrieves the current milestone

    @param project_id: Project identifier (integer)

    @return: Returns the current milestone
    """

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    for ms in api.milestones.list(project=project_id):
        if date > ms.estimated_start and date < ms.estimated_finish:
            sprint_url = get_sprint_board(ms)
            message='Sprint: [ %s ] | %s' % (ms.name, sprint_url)
            log.info(message)
            return ms

    return milestone

def get_sprint_stories(milestone):
    """
    Retrieves user stories belonging to a milestone

    @param milestone: milestone to get the user stories from

    @return: Returns the list of user stories from a milestone
    """

    return milestone.user_stories

def get_sprint_board(milestone):
    """
    Retrieves the taskboard link url for a milestone

    @param milestone: milestone to get the board url from

    @return: Returns the taskboard link url for a milestone
    """

    baseurl='https://tree.taiga.io/project/%s/taskboard/' % PROJECT_SLUG
    sprint_url = baseurl + milestone.slug

    return sprint_url

def get_project_users(project_id):
    """
    Retrieves all users from a project

    @param project_id: project id to get users from

    @return: Returns a dict with user full names and ids
    """

    users_dict={}

    users_list = api.users.list(project=project_id)
    for u in users_list:
        users_dict[u.id] = u.full_name

    return users_dict

def get_story_statuses(project_id):
    """
    Retrieves all user story statuses from a project

    @param project_id: project id to get users from

    @return: Returns a dict with statuses and ids
    """

    statuses_dict={}

    statuses_list = api.user_story_statuses.list(project=project_id)
    for s in statuses_list:
        statuses_dict[s.id] = s.name

    return statuses_dict

def main(argv):

    token = auth_taiga()
    project_id = get_project(PROJECT_SLUG)

    parser = argparse.ArgumentParser(
        description="Query user stories from Taiga project"
    )

    parser.add_argument(
        '-o', '--orphan',
        action='store_true',
        default=False,
        help='Search for orphan user stories (without owner/assigned_to)',
    )

    parser.add_argument(
        '-s', '--sprint',
        default='current',
        help='Specify the sprint to search'
    )

    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='Enable DEBUG mode.'
    )

    args = parser.parse_args()

    logformat = '%(asctime)s %(levelname)s %(name)s:  %(message)s'
    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format=logformat)
    else:
        logging.basicConfig(level=logging.INFO, format=logformat)

    if args.sprint == "current":
        sprint = get_current_sprint(project_id)
        user_stories = get_sprint_stories(sprint)
    else:
        user_stories = get_user_stories(project_id)

    if args.orphan:
        message = 'Getting orphan user stories...'
        log.info(message)
        user_stories = filter_user_stories(user_stories, assigned_to=None)

    us_array = get_stories_data(user_stories, project_id, 'ref', 'subject',
                                'status', 'assigned_to')
    print_user_stories(us_array, ['ref', 'subject', 'status', 'assigned_to'])

if __name__ == "__main__":
    log = logging.getLogger(__name__)
    api = TaigaAPI()
    main(sys.argv)
