import logging

from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponsePermanentRedirect
from django.conf import settings
from django.core.urlresolvers import reverse
from rest_framework.renderers import JSONRenderer

from readthedocs.builds.models import Build, Version
from readthedocs.builds.filters import BuildFilter
from readthedocs.projects.models import Project
from readthedocs.restapi.serializers import BuildSerializerFull

from redis import Redis, ConnectionError


log = logging.getLogger(__name__)


class BuildList(ListView):
    model = Build

    def get_queryset(self):
        self.project_slug = self.kwargs.get('project_slug', None)

        self.project = get_object_or_404(
            Project.objects.protected(self.request.user),
            slug=self.project_slug
        )
        queryset = Build.objects.filter(project=self.project)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(BuildList, self).get_context_data(**kwargs)

        filter = BuildFilter(self.request.GET, queryset=self.get_queryset())
        active_builds = self.get_queryset().exclude(state="finished").values('id')

        context['project'] = self.project
        context['filter'] = filter
        context['active_builds'] = active_builds
        context['versions'] = Version.objects.public(user=self.request.user, project=self.project)

        try:
            redis = Redis(**settings.REDIS)
            context['queue_length'] = redis.llen('celery')
        except ConnectionError:
            context['queue_length'] = None

        return context


class BuildDetail(DetailView):
    model = Build

    def get_queryset(self):
        self.project_slug = self.kwargs.get('project_slug', None)

        self.project = get_object_or_404(
            Project.objects.protected(self.request.user),
            slug=self.project_slug
        )
        queryset = Build.objects.filter(project=self.project)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(BuildDetail, self).get_context_data(**kwargs)
        context['project'] = self.project
        build_serializer = BuildSerializerFull(self.get_object())
        build_data = build_serializer.data
        context['build_json'] = (JSONRenderer()
                                 .render(build_data))
        return context


def builds_redirect_list(request, project_slug):
    return HttpResponsePermanentRedirect(reverse('builds_project_list', args=[project_slug]))


def builds_redirect_detail(request, project_slug, pk):
    return HttpResponsePermanentRedirect(reverse('builds_detail', args=[project_slug, pk]))
