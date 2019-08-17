import json

from django.db.models import QuerySet, Q, CharField
from django.db.models.functions import Cast
from django.http import HttpRequest
from django.shortcuts import render, reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django_mysql.models.functions import JSONExtract

from .. import views
from ..models import Record


class RecordsJson(BaseDatatableView):
    model = Record

    # columns = ['id', 'user', 'github', 'dataset', 'uploaded_at']

    # order_columns = ['id', '', '', '', 'uploaded_at']

    max_display_length = 50

    def render_column(self, row: Record, column):
        if column == 'id':
            return '<a href="{0}?id={1}">#{1}</a>'.format(reverse(views.show), row.id)
        elif column == 'user':
            return '<a href="{0}?uid={1}">{2}</a>'.format(reverse(views.records), row.user.id, row.user.username)
        elif column == 'github':
            return '<a href="{}">{}</a>'.format(row.github_url, row.github_str)
        elif column == 'dataset':
            try:
                dataloader = dict(row.record_information['dataloader'])
                name = next(iter(dataloader))
                res = '<a href="{0}?dataset={1}">{1}</a> ({2})'.format(reverse(views.records), name,
                                                                       dataloader[name]['file_id'])
                if len(dataloader) > 1:
                    res += '...'
                return res
            except:
                return 'unknown'
        elif column == 'uploaded_at':
            return row.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
        elif column in row.result:
            data = row.result[column]
            if isinstance(data, float):
                return '{0:.3f}'.format(data)
            elif isinstance(data, str) and 'hash' in column:
                return '{}...'.format(data[:6])
            return escape(json.dumps(data))
        else:
            return super(RecordsJson, self).render_column(row, column)

    def get_initial_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            return Record.objects.filter(
                Q(hidden=False) |
                Q(user=user)
            )
        else:
            return Record.objects.filter(
                hidden=False
            )

    def filter_queryset(self, qs: QuerySet):
        query_dict = self._querydict

        dataset = query_dict.get('dataset', None)
        if dataset:
            qs = qs.filter(
                record_information__dataloader__has_key=dataset
            )

        username = query_dict.get('user', None)
        if username:
            qs = qs.filter(
                user__username__exact=username
            )

        github = query_dict.get('github', None)
        if github:
            qs = qs.filter(
                Q(git_user__istartswith=github) |
                Q(git_repo__istartswith=github) |
                Q(git_commit__istartswith=github)
            )

        file_id = query_dict.get('file_id', None)
        if file_id:
            qs = qs.filter(
                file_id__iendswith=file_id
            )

        return qs

    def ordering(self, qs):
        query_dict = self._querydict

        if 'order[0][column]' not in query_dict:
            return qs

        sort_col = int(query_dict.get('order[0][column]'))
        sort_dir = query_dict.get('order[0][dir]')
        order_columns = self.get_order_columns()
        sortcol = order_columns[sort_col]
        sdir = '-' if sort_dir == 'desc' else ''

        if sortcol == 'id' or sortcol == 'uploaded_at':
            return qs.order_by('{0}{1}'.format(sdir, sortcol))
        else:
            json_extract = JSONExtract('result', '$."{0}"'.format(sortcol))
            if sort_dir == 'desc':
                json_extract = json_extract.desc()
            return qs.order_by(json_extract)


def records(request):
    username = request.GET.get('user', '')
    file_id = request.GET.get('file_id', '')

    extra_columns = request.GET.get('extra_columns', None)
    if extra_columns:
        extra_columns = [s.strip() for s in extra_columns.split(',')]
    else:
        extra_columns = []

    dataset = request.GET.get('dataset', '')

    all_datasets = json.load(open('config/dataset_columns.json'))
    return render(request, 'dashboard/records.html', locals())
