from rest_framework import pagination
from rest_framework.response import Response


class PostPagination(pagination.PageNumberPagination):

    page_size_query_param = 'size'
    max_page_size = 50

    def get_paginated_response(self, context):

        request = context['request']
        host = request.scheme + "://" + request.META['HTTP_HOST'] + "/"

        return Response({
            'query': 'posts',
            'count': self.page.paginator.count,
            'size': self.page.paginator.per_page,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'posts': context['data']
        })


class UserPagination(pagination.PageNumberPagination):

    page_size_query_param = 'size'
    max_page_size = 50

    def get_paginated_response(self, context):

        request = context['request']
        host = request.scheme + "://" + request.META['HTTP_HOST'] + "/"

        return Response({
            'query': 'authors',
            'host': host,
            'count': self.page.paginator.count,
            'size': self.page.paginator.per_page,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'authors': context['data']
        })


class CommentPagination(pagination.PageNumberPagination):

    page_size_query_param = 'size'
    max_page_size = 50

    def get_paginated_response(self, context):

        request = context['request']
        host = request.scheme + "://" + request.META['HTTP_HOST'] + "/"

        return Response({
            'query': 'comments',
            'count': self.page.paginator.count,
            'size': self.page.paginator.per_page,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'comment': context['data']
        })
