import io
from typing import List, Optional

import pandas
import requests

import json

from management_tools.sprint import Sprint


class SprintDataMapper:
    REDMINE_URL = '...'
    SPRINT_RECORD_FILE_PATH = '../sprints_record.txt'
    AUTOLOGIN_COOKIE = '0e965f8e6cd5e7565c6aea6fbde64f0623d41698'

    def get_all(self) -> List[Sprint]:
        sprints = list()

        with open(self.SPRINT_RECORD_FILE_PATH) as sprints_record_file:
            sprints_record = json.load(sprints_record_file)

            for sprint_name, sprint_record_data in sprints_record.items():
                sprints.append(
                    self._build_sprint_from_record_data(name=sprint_name, sprint_record_data=sprint_record_data)
                )

        return sprints

    def get(self, name: str) -> Sprint:
        with open(self.SPRINT_RECORD_FILE_PATH) as sprints_record_file:
            sprints_record = json.load(sprints_record_file)

            if name in sprints_record:
                sprint_record_data = sprints_record[name]
                sprint = self._build_sprint_from_record_data(name=name, sprint_record_data=sprint_record_data)

                return sprint

            else:
                raise ValueError(f'There is not Sprint with name "{name}".')

    def _build_sprint_from_record_data(self, name: str, sprint_record_data: dict) -> Sprint:
        redmine_id = sprint_record_data.pop('redmine_id', None)
        issues_df = self._get_issues_df(redmine_id)

        sprint = Sprint(name=name, issues_df=issues_df, **sprint_record_data)

        return sprint

    def _get_issues_df(self, redmine_id: int) -> Optional[pandas.DataFrame]:
        if redmine_id is None:
            return None

        response = self._request_issues(redmine_id)

        issues_df = pandas.read_csv(io.StringIO(response.text), sep=";")

        issues_df = self._preprocess_issues_df(issues_df)

        return issues_df

    def _request_issues(self, redmine_id):
        url = f"http://10.0.20.21/projects/spinner/issues.csv?utf8=%E2%9C%93&set_filter=1&f%5B%5D=agile_sprints&op%5Bagile_sprints%5D=%3D&v%5Bagile_sprints%5D%5B%5D={redmine_id}&c%5B%5D=id&c%5B%5D=tracker&c%5B%5D=status&c%5B%5D=subject&c%5B%5D=assigned_to&c%5B%5D=story_points&c%5B%5D=spent_hours&c%5B%5D=closed_on&sort=id%3Adesc&c%5B%5D=all_inline&encoding=UTF-8"
        # headers = {'Cookie': f'autologin={self.AUTOLOGIN_COOKIE};'}
        headers = {'Cookie': '_redmine_session=QjRVb2NPN2dLTlBYNEF4MXBzMjBqT2ZtbFhrYjRPUDNVM1pwYkFFMFVOQmsyTjR0Z2VxdTVZWFVjR3JHTGRlM3QrdCs0WEhmckFmN215dFZlcHBxR1F2SXA1WXlkWVVsMDk2NFVhSnBNcUJxVUdxY0tibkpKbVFXaEp6UFkxUnZWZmc5WjZrUGpsUytSd0VnOFNoaVQyU1J5cTFQMU1mNFJ0WWZMcFZocC9jM2xISDlFYmtIbi9TSlgwZ1ZVQ2x4dkZmeHE1cDV1bm1PNDhDZE5oT0pueExueWkxL3NheDllL2RKYW9XUVV3WT0tLXRITC90dWY4Q2hFQjNFU1FJR2NNTEE9PQ%3D%3D--614c97ce6c3e468186694776891f22c700d6d7f8'}

        response = requests.get(url, headers=headers)

        return response

    def _preprocess_issues_df(self, issues_df):
        issues_df['Tiempo dedicado'] = issues_df['Tiempo dedicado'].str.replace(',', '.').astype(float)
        issues_df['Cerrada'] = pandas.to_datetime(issues_df['Cerrada'])

        return issues_df
