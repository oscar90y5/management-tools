from unittest import TestCase

from management_tools.data_mappers.sprint_data_mapper import SprintDataMapper
from management_tools.sprint import Sprint


class TestSprintDataMapper(TestCase):
    def setUp(self) -> None:
        self.sprint_data_mapper = SprintDataMapper()
        self.sprint_data_mapper.SPRINT_RECORD_FILE_PATH = 'test_sprint_record.txt'

    def test_without_issues(self):
        sprint = self.sprint_data_mapper.get(name='test_without_issues')
        print(sprint.__dict__)

    def test_with_issues(self):
        sprint = self.sprint_data_mapper.get(name='test_with_issues')
        print(sprint.__dict__)
        print(sprint.issues_df)

    def test_select_all(self):
        sprints = self.sprint_data_mapper.get_all()
        self.assertIsInstance(sprints, list, "SprintDataMapper.get_all() tiene que devolver una lista.")
        self.assertEqual(len(sprints), 2)
        self.assertIsInstance(sprints[0], Sprint, "Los elementos de SprintDataMapper.get_all() tienen que ser de tipo Sprint.")

