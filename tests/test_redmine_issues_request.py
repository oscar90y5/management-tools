from unittest import TestCase
import requests
import pandas
import io


class TestRedmineIssuesRequest(TestCase):
    def test_request(self):
        response = self._make_request()
        print(response.text)

    def test_cast_to_data_frame(self):
        response = self._make_request()

        issues = pandas.read_csv(io.StringIO(response.text), sep=";")

        print(issues.head())

    def _make_request(self):
        url = "http://10.0.20.21/projects/rubik/issues.csv?utf8=%E2%9C%93&set_filter=1&f%5B%5D=agile_sprints&op%5Bagile_sprints%5D=%3D&v%5Bagile_sprints%5D%5B%5D=206&c%5B%5D=id&c%5B%5D=tracker&c%5B%5D=status&c%5B%5D=subject&c%5B%5D=assigned_to&c%5B%5D=story_points&c%5B%5D=spent_hours&c%5B%5D=closed_on&sort=id%3Adesc&c%5B%5D=all_inline&encoding=UTF-8"
        headers = {'Cookie': 'autologin=fbedf9b9a07303a021a290f02f5294c60268dc23;'}

        response = requests.get(url, headers=headers)

        return response
