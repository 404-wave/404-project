from rest_framework.response import Response
from rest_framework import pagination

class PostPagination(pagination.PageNumberPagination):

    page_size = 50
    max_page_size = 50
    page_size_query_param = 'size'

    def get_paginated_response(self, context):

        return Response({
            'query': 'posts',
            'count': self.page.paginator.count,
            'size': self.page.paginator.per_page,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'posts': context
        })


class CommentPagination(pagination.PageNumberPagination):

    page_size = 50
    max_page_size = 50
    page_size_query_param = 'size'

    def get_paginated_response(self, context):

        return Response({
            'query': 'comments',
            'count': self.page.paginator.count,
            'size': self.page.paginator.per_page,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'comments': context
        })
