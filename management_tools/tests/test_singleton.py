
from unittest import TestCase

from management_tools.sprint_statistics_service import SprintStatisticsService


class TestSingleton(TestCase):
    def test(self):
        s1 = SprintStatisticsService()
        s2 = SprintStatisticsService()
        self.assertIs(s1, s2)
