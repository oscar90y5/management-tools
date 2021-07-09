from unittest import TestCase

from sprint import Sprint
from tests.factories.sprint_factory import SprintFactory


class TestSprintFactory(TestCase):
    def test(self):
        sprint = SprintFactory()
        self.assertIsInstance(sprint, Sprint)
