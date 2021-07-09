import datetime

from IPython.display import Markdown, display
import pandas as pd


class Sprint:
    def __init__(
            self, programmers_count, hours_per_point, sprint_start_date, sprint_end_date, pre_deployment_date,
            support_percentage, pre_deployment_days, issues_df=None
    ):
        self.programmers_count = programmers_count
        self.hours_per_point = hours_per_point
        self.sprint_start_date = self.cast_str_date(sprint_start_date)
        self.sprint_end_date = self.cast_str_date(sprint_end_date)
        self.pre_deployment_date = self.cast_str_date(pre_deployment_date)
        self.support_percentage = support_percentage
        self.pre_deployment_days = pre_deployment_days
        self.issues_df = issues_df

        self.active_days_index = {0, 1, 2, 3, 4}
        self.priorities_until_pre_deployment = ['Alta', 'Inmediata', 'Urgente']

    def printmd(self, string):
        display(Markdown(string))

    def cast_str_date(self, str_date):
        return datetime.datetime.strptime(str_date, '%d/%m/%y')

    def get_all_team_points_from(self, days):
        all_team_hours = self.get_all_team_hours_from(days)
        all_team_points = all_team_hours / self.hours_per_point

        return all_team_points

    def get_all_team_hours_from(self, days):
        hours = days * 8
        all_team_hours = hours * self.programmers_count
        return all_team_hours

    def without_support(self, measure):
        return measure * (1 - self.support_percentage / 100)

    def only_support(self, measure):
        return measure * self.support_percentage / 100

    def get_active_days(self, start_date, end_date, interval='[]'):
        assert len(interval) == 2
        assert interval[0] in ('(', '[')
        assert interval[1] in (')', ']')

        one_day = datetime.timedelta(days=1)

        if interval[0] == '(':
            start_date += one_day

        if interval[1] == ')':
            end_date -= one_day

        active_days = 0
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() in self.active_days_index:
                active_days += 1
            current_date += one_day

        return active_days

    def calculate_estimated_points_until_pre_deployment(self):
        active_days = self.days_until_pre_deployment()

        team_points = self.get_all_team_points_from(active_days)

        team_points_without_support = self.without_support(team_points)

        return team_points_without_support

    def days_until_pre_deployment(self):
        return self.get_active_days(self.sprint_start_date, self.pre_deployment_date, interval='[)')

    def calculate_points_post_pre_deployment(self):
        active_days = self._get_days_post_pre_deployment()

        team_points = self.get_all_team_points_from(active_days)

        team_points_without_support = self.without_support(team_points)

        return team_points_without_support

    def _get_days_post_pre_deployment(self):
        pre_deployment_days = datetime.timedelta(days=self.pre_deployment_days)
        end_pre_deployment_date = self.pre_deployment_date + pre_deployment_days

        return self.get_active_days(end_pre_deployment_date, self.sprint_end_date)

    def calculate_all_sprint_active_days(self):
        active_days = self.get_active_days(self.sprint_start_date, self.sprint_end_date)

        return active_days

    def calculate_all_sprint_support_hours(self):
        active_days = self.calculate_all_sprint_active_days()

        all_team_hours = self.get_all_team_hours_from(active_days)

        all_team_support_hours = self.only_support(all_team_hours)

        return all_team_support_hours

    def calculate_all_sprint_support_points(self):
        return self.calculate_all_sprint_support_hours() / self.hours_per_point

    def show_planning_variables(self):
        active_days = self.calculate_all_sprint_active_days()
        points_until_pre_deployment = self.calculate_estimated_points_until_pre_deployment()
        points_post_pre_deployment = self.calculate_points_post_pre_deployment()
        all_sprint_support_hours = self.calculate_all_sprint_support_hours()
        all_sprint_support_points = self.calculate_all_sprint_support_points()

        self.printmd(
            f"### Sprint '{self.sprint_start_date}' - '{self.sprint_end_date}' "
            f"({active_days} días | {self.programmers_count} cracks | {self.hours_per_point} h/punto):\n"
            f" * Puntos hasta el pase (**ALTA** o más): **{points_until_pre_deployment}** puntos.\n"
            f" * Puntos después del pase (**NORMAL**): **{points_post_pre_deployment}** puntos.\n"
            f" * Puntos si no soporte (**BAJA**): **{all_sprint_support_points}** puntos.\n"
            f" * Tiempo **máximo soporte**: **{all_sprint_support_hours}**h.\n"
        )

    def show_support_percentage(self):
        assert self.issues_df is not None

        support_hours = self._get_actual_support_hours()

        support_percentage = self._calculate_support_percentage()

        self.printmd(f"Horas de soporte realizadas: **{support_hours}h** (**{support_percentage}%**).")

    def _calculate_support_percentage(self):
        active_days = self.calculate_all_sprint_active_days()

        all_team_hours = self.get_all_team_hours_from(active_days)

        actual_support_hours = self._get_actual_support_hours()

        return actual_support_hours / all_team_hours * 100

    def _get_actual_support_hours(self):
        return self.issues_df[self.issues_df['Tipo'] == 'Soporte']['Tiempo dedicado'].sum()

    def show_points_per_hour(self):
        assert self.issues_df is not None

        optimistic_calculus = self._calculate_points_per_hour_optimistic_input_hours()

        pessimistic_calculus = self._calculate_points_per_hour_pessimistic_input_hours()

        self.printmd(
            f"### Horas por punto:\n"
            f"* Cálculo para horas bien imputadas: **{optimistic_calculus:.2f} h/punto**.\n"
            f"* Cálculo para horas bien imputadas solo en soporte: **{pessimistic_calculus:.2f} h/punto**."
        )

    def _calculate_points_per_hour_optimistic_input_hours(self):
        return self._get_non_support_hours() / self._get_non_support_points()

    def _get_non_support_points(self):
        return self.issues_df[self.issues_df['Tipo'] != 'Soporte']['Story points'].sum()

    def _get_non_support_hours(self):
        return self.issues_df[self.issues_df['Tipo'] != 'Soporte']['Tiempo dedicado'].sum()

    def _calculate_points_per_hour_pessimistic_input_hours(self):
        active_days = self.days_until_pre_deployment() + self._get_days_post_pre_deployment()

        all_team_hours = self.get_all_team_hours_from(active_days)

        support_hours = self._get_actual_support_hours()

        non_support_hours = all_team_hours - support_hours

        return non_support_hours / self._get_non_support_points()

    def plot_burndown(self, ax):
        assert self.issues_df is not None

        points_until_pre_deployment = self._get_points_until_pre_deploy()
        active_days = self.days_until_pre_deployment()

        points_per_day = points_until_pre_deployment / active_days

        one_day = datetime.timedelta(days=1)

        x = list()
        reference_y = list()
        cumulative_y = points_until_pre_deployment

        current_date = self.sprint_start_date
        while current_date <= self.pre_deployment_date:
            x.append(current_date)
            reference_y.append(cumulative_y)
            if current_date.weekday() in self.active_days_index:
                cumulative_y -= points_per_day
            current_date += one_day

        ax.plot(x, reference_y, color='k', linestyle='--', label="Objetivo")

        grouped_tasks = self._get_tasks_until_pre_deploy().groupby(pd.Grouper(key='Cerrada', freq='d')).sum()
        x = grouped_tasks.index

        y = self.patata(grouped_tasks['Story points'])

        ax.plot(x, y, label="Realidad")
        ax.fill_between(x, y, alpha=.5)

        print(points_until_pre_deployment)
        print(grouped_tasks['Story points'].sum())

    def _get_points_until_pre_deploy(self):
        return self._get_tasks_until_pre_deploy()['Story points'].sum()

    def _get_tasks_until_pre_deploy(self):
        return self.issues_df[self.issues_df['Prioridad'].isin(self.priorities_until_pre_deployment)]

    def patata(self, day_grouped_solved_points):
        points_until_pre_deployment = self._get_points_until_pre_deploy()
        day_grouped_unsolved_points = list()
        solved_points = 0

        for current_day_solved_points in day_grouped_solved_points:
            solved_points += current_day_solved_points
            current_day_unsolved_points = points_until_pre_deployment - solved_points
            day_grouped_unsolved_points.append(current_day_unsolved_points)

        return day_grouped_unsolved_points
