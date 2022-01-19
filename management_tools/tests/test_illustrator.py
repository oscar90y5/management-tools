from unittest import TestCase
from unittest.mock import patch

import mpld3
import pandas

from management_tools.data_mappers.sprint_data_mapper import SprintDataMapper
from management_tools.illustrator import Illustrator

from matplotlib import pyplot as plt

from management_tools.tests.factories.sprint_factory import SprintFactory


class TestIllustrator(TestCase):

    @patch.object(SprintDataMapper, 'get_all')
    def test_plot_support_percentage(self, mocked_function):
        mocked_function.return_value = self._get_test_sprints()

        fig, ax = plt.subplots()
        illustrator = Illustrator()

        illustrator.plot_support_percentage(fig, ax)

        mpld3.show(fig)
        # fig.show()

    def _get_test_sprints(self):
        sprints = list()
        sprints.append(SprintFactory(
            name="2021 1-2",
            issues_df=self._get_issues(8)
        ))
        sprints.append(SprintFactory(
            name="2021 3-4",
            issues_df=self._get_issues(20)
        ))
        sprints.append(SprintFactory(
            name="2021 5-6",
            issues_df=self._get_issues(8)
        ))

        return sprints

    def _get_issues(self, time: int):
        issues_dict = {
            'Story points': [1],
            'Prioridad': ['Alta'],
            'Cerrada': ['2021-5-03 12:00'],
            'Estado': ['Cerrada'],
            'Tiempo dedicado': time,
            'Tipo': ['Soporte']
        }
        issues_df = pandas.DataFrame.from_dict(issues_dict)
        issues_df['Cerrada'] = pandas.to_datetime(issues_df['Cerrada'])

        return issues_df
