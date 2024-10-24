from typing import List, Optional

from ninja_extra import api_controller, route, status
from ninja_extra.exceptions import APIException

from api.comments.schemas import CommentDailyBreakdownSchema
from api.comments.services import AnalyticsService


@api_controller("/comments-daily-breakdown", tags=["Comments Daily Breakdown"])
class AnalyticsController:
    """
    Controller for analytics functionality.

    Attributes:
        - get_comments_daily_breakdown (method): Get daily breakdown of comments.
    """

    @route.get("/", response={status.HTTP_200_OK: List[CommentDailyBreakdownSchema]})
    async def get_comments_daily_breakdown(
        self,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
    ) -> List[CommentDailyBreakdownSchema]:
        """
        Get daily breakdown of comments.

        :param date_from: date_from filter
        :param date_to: date_to filter
        :return: a list of daily breakdown of comments in the given date range
        """
        try:
            analytics_service = AnalyticsService()
            date_from_parsed, date_to_parsed = analytics_service.parse_dates(
                date_from=date_from,
                date_to=date_to,
            )
            comments = await analytics_service.fetch_comments(date_from=date_from_parsed, date_to=date_to_parsed)
            return await analytics_service.format_comments(comments=comments)
        except Exception as err:
            raise APIException(detail=str(err))
