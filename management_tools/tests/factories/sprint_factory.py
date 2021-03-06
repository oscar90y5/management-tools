from management_tools.sprint import Sprint


class SprintFactory:
    def __new__(
            cls,
            name="Sprint name",
            programmers_count=1,
            hours_per_point=1,
            start_date='6/9/21',
            pre_deployment_date='15/9/21',
            end_date='17/9/21',
            support_percentage=30,
            pre_deployment_days=2,
            issues_df=None
    ):
        return Sprint(
            name=name,
            programmers_count=programmers_count,
            hours_per_point=hours_per_point,
            start_date=start_date,
            pre_deployment_date=pre_deployment_date,
            end_date=end_date,
            support_percentage=support_percentage,
            pre_deployment_days=pre_deployment_days,
            issues_df=issues_df
        )

