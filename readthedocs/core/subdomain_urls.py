from django.conf.urls import url, patterns

from readthedocs.projects.constants import LANGUAGES_REGEX
from readthedocs.urls import urlpatterns as main_patterns

handler500 = 'readthedocs.core.views.server_error'
handler404 = 'readthedocs.core.views.server_error_404'

urlpatterns = patterns(
    '',  # base view, flake8 complains if it is on the previous line.
    url((r'^projects/(?P<project_slug>[\w.-]+)/(?P<lang_slug>%s)/'
         r'(?P<version_slug>[\w.-]+)/(?P<filename>.*)$' % LANGUAGES_REGEX),
        'readthedocs.core.views.subproject_serve_docs',
        name='subproject_docs_detail'),

    url(r'^projects/(?P<project_slug>[\w.-]+)',
        'readthedocs.core.views.subproject_serve_docs',
        name='subproject_docs_detail'),

    url(r'^projects/$',
        'readthedocs.core.views.subproject_list',
        name='subproject_docs_list'),

    url(r'^(?P<lang_slug>%s)/(?P<version_slug>[\w.-]+)/(?P<filename>.*)$' % LANGUAGES_REGEX,
        'readthedocs.core.views.serve_docs',
        name='docs_detail'),

    url(r'^(?P<lang_slug>%s)/(?P<version_slug>.*)/$' % LANGUAGES_REGEX,
        'readthedocs.core.views.serve_docs',
        {'filename': 'index.html'},
        name='docs_detail'),

    url(r'^page/(?P<filename>.*)$',
        'readthedocs.core.views.redirect_page_with_filename',
        name='docs_detail'),

    url(r'^(?P<lang_slug>%s)/$' % LANGUAGES_REGEX,
        'readthedocs.core.views.redirect_lang_slug',
        name='lang_subdomain_handler'),

    url(r'^(?P<version_slug>.*)/$',
        'readthedocs.core.views.redirect_version_slug',
        name='version_subdomain_handler'),

    url(r'^$', 'readthedocs.core.views.redirect_project_slug', name='homepage'),
)

urlpatterns += main_patterns
