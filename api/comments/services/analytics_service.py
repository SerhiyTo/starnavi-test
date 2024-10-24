from datetime import datetime
from typing import Optional

from asgiref.sync import sync_to_async
from django.db.models import Q, Count, QuerySet
from django.db.models.functions import TruncDate

from api.comments.models import Comment
from api.comments.schemas import CommentDailyBreakdownSchema


class AnalyticsService:
    """
    Service class for analytics functionality.

    Attributes:
        - parse_dates (method): Parse the date strings into datetime objects.
        - search_comments (method): Search for comments based on the date range.
        - format_comments (method): Format the comments queryset into a list of dictionaries.
    """

    @staticmethod
    def parse_dates(
        date_from: str, date_to: str
    ) -> (Optional[datetime], Optional[datetime]):
        """
        Parse the date strings into datetime objects.

        Args:
            - date_from(str): The start date string.
            - date_to(str): The end date string.

        Returns:
            - A tuple containing the parsed start and end dates.
        """
        date_from_parsed = (
            datetime.strptime(date_from, "%Y-%m-%d") if date_from else None
        )
        date_to_parsed = datetime.strptime(date_to, "%Y-%m-%d") if date_to else None

        return date_from_parsed, date_to_parsed

    @staticmethod
    async def fetch_comments(
        date_from: Optional[datetime], date_to: Optional[datetime]
    ) -> QuerySet:
        """
        Search for comments based on the date range.

        :param date_from: date_from filter
        :param date_to: date_to filter
        :return: comments queryset
        """
        query = Q()
        if date_from:
            query &= Q(created_at__gte=date_from)
        if date_to:
            query &= Q(created_at__lte=date_to)

        return await sync_to_async(
            lambda: (
                Comment.objects.filter(query)
                .annotate(date=TruncDate("created_at"))
                .values("date")
                .annotate(
                    total_comments=Count("id"),
                    blocked_comments=Count("id", filter=Q(is_blocked=True)),
                )
                .order_by("date")
            )
        )()

    @staticmethod
    async def format_comments(comments: QuerySet):
        """
        Format the comments queryset into a list of dictionaries.

        :param comments: comments queryset
        :return: list of dictionaries
        """
        return await sync_to_async(
            lambda: [
                CommentDailyBreakdownSchema(
                    date=entry["date"].strftime("%Y-%m-%d"),
                    total_comments=entry["total_comments"],
                    blocked_comments=entry["blocked_comments"],
                )
                for entry in comments
            ]
        )()
