from unittest import TestCase
from unittest.mock import patch

from management_tools.sprint_statistics_service import SprintStatisticsService


class TestSprintStatisticsService(TestCase):

    @patch.object(SprintStatisticsService, 'get_all_sprints_support_percentage', return_value=[30, 20, 40, 20, 20, 30])
    def test_get_all_sprints_average_support_percentage(self, mocked_function):
        sprint_statistics_service = SprintStatisticsService()

        expected_all_sprints_average_support_percentage = [30, 25, 30, 27, 24.9, 26.43]
        all_sprints_average_support_percentage = sprint_statistics_service.get_all_sprints_average_support_percentage()

        for value, expected_value in zip(all_sprints_average_support_percentage, expected_all_sprints_average_support_percentage):
            self.assertAlmostEqual(value, expected_value, delta=0.001)
