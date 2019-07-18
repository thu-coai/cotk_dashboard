from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import render, reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape

import dashboard.views as views
from ..models import Record


class RecordsJson(BaseDatatableView):
    model = Record

    columns = ['id', 'user', 'github', 'dataset', 'uploaded_at']

    order_columns = ['id', '', '', '', 'uploaded_at']

    max_display_length = 50

    def render_column(self, row: Record, column):
        if column == 'id':
            return '<a href="{0}?id={1}">#{1}</a>'.format(reverse(views.show), row.id)
        elif column == 'user':
            return escape('{}'.format(row.user.username))
        elif column == 'github':
            return '<a href="{}">{}</a>'.format(row.github_url, row.github_str)
        elif column == 'dataset':
            try:
                return escape(next(iter(row.record_information['dataloader'])))
            except:
                return 'unknown'
        elif column == 'uploaded_at':
            return row.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return super(RecordsJson, self).render_column(row, column)

    def filter_queryset(self, qs: QuerySet):
        request = self.request
        return qs


def records(request):
    return render(request, 'dashboard/records.html', locals())
