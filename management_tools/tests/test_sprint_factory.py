from unittest import TestCase

from management_tools.sprint import Sprint
from management_tools.tests.factories.sprint_factory import SprintFactory


class TestSprintFactory(TestCase):
    def test(self):
        sprint = SprintFactory()
        self.assertIsInstance(sprint, Sprint)
