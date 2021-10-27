from typing import List

from management_tools.data_mappers.sprint_data_mapper import SprintDataMapper
from management_tools.singleton import Singleton


class SprintStatisticsService(Singleton):
    def __init__(self):
        self.sprint_data_mapper = SprintDataMapper()

    def get_all_sprints_support_percentage(self) -> List[int]:
        sprints_support_percentage = list()

        sprints = self.sprint_data_mapper.get_all()

        for sprint in sprints:
            sprints_support_percentage.append(
                sprint.calculate_support_percentage()
            )

        return sprints_support_percentage

    def get_all_sprints_average_support_percentage(self) -> List[int]:
        standard_average_threshold = 3
        last_sprint_average_weight_percentage = .3

        all_sprints_average_support_percentage = list()

        all_sprints_support_percentage = self.get_all_sprints_support_percentage()

        for i, support_percentage in enumerate(all_sprints_support_percentage):
            if i < standard_average_threshold:
                list_section = all_sprints_support_percentage[:i+1]
                average_support_percentage = sum(list_section)/len(list_section)
            else:
                average_support_percentage = \
                    support_percentage * last_sprint_average_weight_percentage + \
                    all_sprints_average_support_percentage[-1] * (1 - last_sprint_average_weight_percentage)

            all_sprints_average_support_percentage.append(average_support_percentage)

        return all_sprints_average_support_percentage

    def get_average_support_percentage(self):
        return self.get_all_sprints_average_support_percentage()[-1]
