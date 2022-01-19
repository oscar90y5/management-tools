from typing import List

from management_tools.data_mappers.sprint_data_mapper import SprintDataMapper
from management_tools.singleton import Singleton
from management_tools.sprint_statistics_service import SprintStatisticsService


class Illustrator(Singleton):
    def __init__(self):
        self.sprint_data_mapper = SprintDataMapper()
        self.sprint_statistics_service = SprintStatisticsService()

    def plot_support_percentage(self, fig, ax):
        all_sprints_support_percentage = self.sprint_statistics_service.get_all_sprints_support_percentage()
        all_sprints_average_support_percentage = self.sprint_statistics_service.get_all_sprints_average_support_percentage()
        average_support_percentage = self.sprint_statistics_service.get_average_support_percentage()
        sprint_labels = self._get_all_sprints_label()

        ax.plot(sprint_labels, all_sprints_support_percentage, label="Soporte")
        ax.plot(sprint_labels, all_sprints_average_support_percentage, label="Soporte medio")
        ax.text(len(sprint_labels)-.99, average_support_percentage, f'{average_support_percentage:.2f}', va='center')

        ## Mostramos la cuadricula.
        # ax.grid(True, axis='y')

        ## Ocultamos el marco.
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        ax.legend(framealpha=1)

        ax.set_title("Soporte empleado")

        ax.set_xticks([])

        min_y = ax.get_ylim()[0]
        for i, sprint_label in enumerate(sprint_labels):
            ax.text(i, min_y + .1, sprint_label, ha='center')

        ax.set_ylabel("Porcentaje")
        ax.set_xlabel("Sprint")

    def _get_all_sprints_label(self) -> List[str]:
        sprints = self.sprint_data_mapper.get_all()
        labels = [sprint.name for sprint in sprints]
        return labels
