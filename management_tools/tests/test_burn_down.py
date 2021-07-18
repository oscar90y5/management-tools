from unittest import TestCase

import pandas

from management_tools.tests.factories.sprint_factory import SprintFactory

from matplotlib import pyplot as plt
from freezegun import freeze_time


class TestBurnDown(TestCase):
    def setUp(self) -> None:
        self._init_past_sprint()
        self._init_current_sprint()

    def _init_past_sprint(self):
        issues_dict = {
            'Story points': [1] * 7,
            'Prioridad': ['Alta'] * 7,
            'Cerrada': [
                '2021-5-03 12:00', '2021-5-04 12:00', '2021-5-05 12:00', '2021-5-06 12:00',
                '2021-5-07 12:00', '2021-5-10 12:00', '2021-5-11 12:00',
            ]
        }
        issues_df = pandas.DataFrame.from_dict(issues_dict)
        issues_df['Cerrada'] = pandas.to_datetime(issues_df['Cerrada'])

        self.past_sprint = SprintFactory(
            start_date='3/5/21',
            pre_deployment_date='12/5/21',
            end_date='14/5/21',
            issues_df=issues_df
        )

    def _init_current_sprint(self):
        issues_dict = {
            'Story points': [1] * 7,
            'Prioridad': ['Alta'] * 7,
            'Cerrada': [
                '2021-5-03 12:00', '2021-5-04 12:00', '2021-5-05 12:00',
            ] + 4 * [None]
        }
        issues_df = pandas.DataFrame.from_dict(issues_dict)
        issues_df['Cerrada'] = pandas.to_datetime(issues_df['Cerrada'])

        self.current_sprint = SprintFactory(
            start_date='3/5/21',
            pre_deployment_date='12/5/21',
            end_date='14/5/21',
            issues_df=issues_df
        )

    def test_burn_down_past_sprint(self):
        fig, ax = plt.subplots()

        self.past_sprint.plot_burndown(fig, ax)

        fig.show()

    @freeze_time("2021-05-05")
    def test_burn_down_current_sprint(self):
        fig, ax = plt.subplots()

        self.current_sprint.plot_burndown(fig, ax)

        fig.show()
