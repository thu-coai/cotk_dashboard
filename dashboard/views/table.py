from django.db.models import QuerySet, Q
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
                dataloader = dict(row.record_information['dataloader'])
                name = next(iter(dataloader))
                res = '{0} ({1})'.format(name, dataloader[name]['file_id'])
                if len(dataloader) > 1:
                    res += '...'
                return escape(res)
            except:
                return 'unknown'
        elif column == 'uploaded_at':
            return row.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return super(RecordsJson, self).render_column(row, column)

    def filter_queryset(self, qs: QuerySet):
        request = self.request
        search = request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(record_information__dataloader__has_key=search) |
                Q(user__username__iexact=search) |
                Q(git_user__iexact=search) |
                Q(git_repo__iexact=search)
            )

        return qs


def records(request):
    return render(request, 'dashboard/records.html', locals())
