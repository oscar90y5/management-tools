from unittest import TestCase

import pandas
from matplotlib import pyplot as plt

from management_tools.tests.factories.sprint_factory import SprintFactory


class TestZipimport(TestCase):
    def setUp(self) -> None:
        self._init_past_sprint()

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

    def test(self):
        import zipimport

        importer = zipimport.zipimporter('../../management_tools.zip')
        sprint_data_mapper = importer.load_module('management_tools/data_mappers/sprint_data_mapper')

        # sprint_data_mapper = mineo_import('management_tools/data_mappers/sprint_data_mapper.py')
        SprintDataMapper = sprint_data_mapper.SprintDataMapper

        sprint = SprintDataMapper().get(name='2021 29-30')

        fig, ax = plt.subplots()

        sprint.plot_burndown(fig, ax)

        fig.show()