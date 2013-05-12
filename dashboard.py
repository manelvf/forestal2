from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard

from forestal2.settings import ENV_BASE_URL

# to activate your index dashboard add the following to your settings.py:
#
# ADMIN_TOOLS_INDEX_DASHBOARD = 'forestal2.dashboard.CustomIndexDashboard'

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for forestal2.
    """
    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)

        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            title=_(u'Enlaces Rapidos'),
            layout='block',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                {
                    'title': _(u'Asociar Viaxes de Camion'),
                    'url': ENV_BASE_URL + '/homogeneidade/all',
                },
                {
                    'title': _(u'Asociar Servizos Forestais - Talas'),
                    'url': ENV_BASE_URL + '/servizogridview',
                },
                {
                    'title': _(u'Asociar Facturas'),
                    'url': ENV_BASE_URL + '/facturagridview',
                },
                {
                    'title': _(u'Pesadas'),
                    'url': ENV_BASE_URL + '/weightactions',
                },
                {
                    'title': _(u'Listado de Fincas/Escrituras'),
                    'url': ENV_BASE_URL + '/generateDeedCSV',
                },
                {
                    'title': _(u'Rexenerar nomes/superficie de fincas'),
                    'url': ENV_BASE_URL + '/rewriteLandSize',
                },
                {
                    'title': _(u'Backup'),
                    'url': ENV_BASE_URL + '/backup',
                },
                {
                    'title': _('Change password'),
                    'url': reverse('admin:password_change'),
                },
                {
                    'title': _('Log out'),
                    'url': reverse('admin:logout')
                },
            ]
        ))

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            title=_('Applications'),
            exclude_list=('django.contrib',),
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            title=_('Administration'),
            include_list=('django.contrib',),
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            title=_('Recent Actions'),
            limit=5
        ))

        # append a feed module
        """
        self.children.append(modules.Feed(
            title=_('Latest Django News'),
            feed_url='http://www.djangoproject.com/rss/weblog/',
            limit=5
        ))
        """

        # append another link list module for "support".
        """
        self.children.append(modules.LinkList(
            title=_('Support'),
            children=[
                {
                    'title': _('Django documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Django "django-users" mailing list'),
                    'url': 'http://groups.google.com/group/django-users',
                    'external': True,
                },
                {
                    'title': _('Django irc channel'),
                    'url': 'irc://irc.freenode.net/django',
                    'external': True,
                },
            ]
        ))
        """


    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        pass


# to activate your app index dashboard add the following to your settings.py:
#
# ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'forestal2.dashboard.CustomAppIndexDashboard'

class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for forestal2.
    """
    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # we disable title because its redundant with the model list module
        self.title = ''

        # append a model list module
        self.children.append(modules.ModelList(
            title=self.app_title,
            include_list=self.models,
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            title=_('Recent Actions'),
            include_list=self.get_app_content_types(),
        ))

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        pass
