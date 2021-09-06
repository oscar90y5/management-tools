import io

import pandas
import requests

import json

from management_tools.sprint import Sprint


class SprintDataMapper:
    REDMINE_URL = '...'
    SPRINT_RECORD_FILE_PATH = '../sprints_record.txt'
    AUTOLOGIN_COOKIE = '0e965f8e6cd5e7565c6aea6fbde64f0623d41698'

    def get(self, name: str) -> Sprint:
        with open(self.SPRINT_RECORD_FILE_PATH) as sprints_record_file:
            sprints_record = json.load(sprints_record_file)

            if name in sprints_record:
                sprint_record_data = sprints_record[name]
                sprint = self._build_sprint_from_record_data(sprint_record_data)

                return sprint

            else:
                raise ValueError(f'There is not Sprint with name "{name}".')

    def _build_sprint_from_record_data(self, sprint_record_data: dict) -> Sprint:
        redmine_id = sprint_record_data.pop('redmine_id', None)
        issues_df = self._get_issues_df(redmine_id)

        sprint = Sprint(issues_df=issues_df, **sprint_record_data)

        return sprint

    def _get_issues_df(self, redmine_id: int) -> pandas.DataFrame:
        if redmine_id is None:
            return None

        response = self._request_issues(redmine_id)

        issues_df = pandas.read_csv(io.StringIO(response.text), sep=";")

        issues_df = self._preprocess_issues_df(issues_df)

        return issues_df

    def _request_issues(self, redmine_id):
        url = f"http://10.0.20.21/projects/rubik/issues.csv?utf8=%E2%9C%93&set_filter=1&f%5B%5D=agile_sprints&op%5Bagile_sprints%5D=%3D&v%5Bagile_sprints%5D%5B%5D={redmine_id}&c%5B%5D=id&c%5B%5D=tracker&c%5B%5D=status&c%5B%5D=subject&c%5B%5D=assigned_to&c%5B%5D=story_points&c%5B%5D=spent_hours&c%5B%5D=closed_on&sort=id%3Adesc&c%5B%5D=all_inline&encoding=UTF-8"
        headers = {'Cookie': f'autologin={self.AUTOLOGIN_COOKIE};'}

        response = requests.get(url, headers=headers)

        return response

    def _preprocess_issues_df(self, issues_df):
        issues_df['Tiempo dedicado'] = issues_df['Tiempo dedicado'].str.replace(',', '.').astype(float)
        issues_df['Cerrada'] = pandas.to_datetime(issues_df['Cerrada'])

        return issues_df
