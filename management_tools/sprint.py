import datetime

from IPython.display import Markdown, display
import pandas as pd

day_of_week_map = ['L', 'M', 'X', 'J', 'V', 'S', 'D']

class Sprint:
    def __init__(
            self, programmers_count, hours_per_point, start_date, pre_deployment_date, end_date,
            support_percentage, pre_deployment_days, issues_df=None
    ):
        self.programmers_count = programmers_count
        self.hours_per_point = hours_per_point
        self.start_date = self.cast_str_date(start_date)
        self.pre_deployment_date = self.cast_str_date(pre_deployment_date)
        self.end_date = self.cast_str_date(end_date)
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
        return self.get_active_days(self.start_date, self.pre_deployment_date, interval='[)')

    def calculate_points_post_pre_deployment(self):
        active_days = self._get_days_post_pre_deployment()

        team_points = self.get_all_team_points_from(active_days)

        team_points_without_support = self.without_support(team_points)

        return team_points_without_support

    def _get_days_post_pre_deployment(self):
        pre_deployment_days = datetime.timedelta(days=self.pre_deployment_days)
        end_pre_deployment_date = self.pre_deployment_date + pre_deployment_days

        return self.get_active_days(end_pre_deployment_date, self.end_date)

    def calculate_all_sprint_active_days(self):
        active_days = self.get_active_days(self.start_date, self.end_date)

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
            f"### Sprint '{self.start_date}' - '{self.end_date}' "
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

    def _get_total_points(self):
        return self.issues_df[self.issues_df['Prioridad'].isin(self.priorities_until_pre_deployment)]['Story points'].sum()

    def plot_burndown(self, fig, ax):
        assert self.issues_df is not None

        total_points = self._get_total_points()

        active_days = self.days_until_pre_deployment()

        points_per_day = total_points / active_days

        one_day = datetime.timedelta(days=1)

        x = list()
        reference_y = list()
        cumulative_y = total_points

        current_date = self.start_date
        while current_date <= (self.end_date + datetime.timedelta(days=1)):
            x.append(current_date)
            if current_date <= self.pre_deployment_date:
                reference_y.append(cumulative_y)
                if current_date.weekday() in self.active_days_index:
                    cumulative_y -= points_per_day
            else:
                reference_y.append(0)
            current_date += one_day

        ax.plot(x, reference_y, color='k', linestyle='--', label="Objetivo")

        self._label_x_axis(ax, x)

        points_on_progress_and_comments = self.issues_df[
            self.issues_df['Prioridad'].isin(self.priorities_until_pre_deployment)
            & self.issues_df['Estado'].isin(['En curso', 'Comentarios'])
        ]['Story points'].sum()

        points_solved_and_in_revision = self.issues_df[
            self.issues_df['Prioridad'].isin(self.priorities_until_pre_deployment)
            & self.issues_df['Estado'].isin(['Resuelta', 'En revisiÃ³n'])
        ]['Story points'].sum()

        # Plot issues with status 'Nueva'.
        new_issues_x, new_issues_y = self._get_new_issues_x_y()
        new_issues_y[-1] -= (points_on_progress_and_comments + points_solved_and_in_revision)

        ax.plot(new_issues_x, new_issues_y, label="Nuevas", marker='o')
        ax.fill_between(new_issues_x, new_issues_y, alpha=.5)

        # Plot issues with status 'En curso' and 'Comentarios'.
        on_progress_and_comments_issues_y = new_issues_y.copy()
        on_progress_and_comments_issues_y[-1] += points_on_progress_and_comments

        ax.plot(new_issues_x, on_progress_and_comments_issues_y, label="En curso / Comentarios", marker='o')
        ax.fill_between(new_issues_x, new_issues_y, on_progress_and_comments_issues_y, alpha=.5)

        # Plot issues with status 'Resuelta' and 'En revisión'.
        solved_and_in_revision_issues_y = on_progress_and_comments_issues_y.copy()
        solved_and_in_revision_issues_y[-1] += points_solved_and_in_revision

        ax.plot(new_issues_x, solved_and_in_revision_issues_y, label="En revisión / Resuelta", marker='o')
        ax.fill_between(new_issues_x, on_progress_and_comments_issues_y, solved_and_in_revision_issues_y, alpha=.5)

        ## Mostramos la cuadricula.
        ax.grid(True, axis='x')

        ## Ocultamos el marco.
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        ax.set_xlim(self.start_date, (self.end_date + datetime.timedelta(days=1)))
        ax.set_ylim(0)

        ax.legend(framealpha=1)

        ax.set_ylabel("Puntos restantes")

    def _get_points_until_pre_deploy(self):
        return self._get_tasks_until_pre_deploy()['Story points'].sum()

    def _get_tasks_until_pre_deploy(self):
        return self.issues_df[self.issues_df['Prioridad'].isin(self.priorities_until_pre_deployment)]

    def _get_new_issues_x_y(self):
        total_points = self._get_total_points()

        grouped_story_points = None

        try:
            grouped_tasks = self._get_tasks_until_pre_deploy().groupby(pd.Grouper(key='Cerrada', freq='d')).sum()
            grouped_story_points = grouped_tasks['Story points']
        except AttributeError:
            pass

        x = list()
        y = list()

        remaining_points = total_points

        current_date = self.start_date
        while current_date <= (datetime.datetime.today() + datetime.timedelta(days=1)) and current_date <= (self.end_date + datetime.timedelta(days=1)):
            x.append(current_date)
            y.append(remaining_points)

            if grouped_story_points is not None and current_date in grouped_story_points.index:
                remaining_points -= grouped_story_points.loc[current_date]

            current_date += datetime.timedelta(days=1)

        return x, y

    def _label_x_axis(self, ax, x):
        interval_centered_x = [date + datetime.timedelta(hours=12) for date in x]
        str_x = [f'{day_of_week_map[date.weekday()]}' for date in x]

        ax.set_xticks(x)
        ax.set_xticklabels([])

        ax.set_xticks(interval_centered_x, minor=True)
        ax.set_xticklabels(str_x, minor=True)
