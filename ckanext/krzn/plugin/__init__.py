import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import pkg_resources

def check_plugin_enabled(plugin_name):
    try:
        pkg_resources.get_distribution(f'ckanext-{plugin_name}')
        return True
    except pkg_resources.DistributionNotFound:
        return False

def no_registering(context, _):
    return {'success': False, 'msg': toolkit._('''You cannot register for this site. If you need an account, ask KRZN.''')}


def is_activity_plugin_loaded():
        return check_plugin_enabled('activity')


def get_current_context():
    """
    Get the current context (package and organization) safely.
    
    Returns:
        dict: A dictionary containing 'package' and 'organization' keys,
              with their respective values if available, or None.
    """
    context = {
        'package': None,
        'organization': None
    }

    try:
        if hasattr(toolkit.g, 'pkg_dict'):
            context['package'] = toolkit.g.pkg_dict
            if context['package'].get('organization'):
                context['organization'] = toolkit.h.get_organization(context['package']['organization']['id'])

        if not context['organization'] and hasattr(toolkit.g, 'group_dict'):
            context['organization'] = toolkit.g.group_dict

        if not context['organization']:
            org_id = toolkit.request.view_args.get('id')
            if org_id:
                try:
                    context['organization'] = toolkit.get_action('organization_show')(
                        data_dict={'id': org_id}
                    )
                except toolkit.ObjectNotFound:
                    pass

    except (RuntimeError, AttributeError):
        pass

    return context

class KrznCustomizations(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.ITemplateHelpers)

    def update_config(self, config):
        toolkit.add_public_directory(config, "../public")
        toolkit.add_template_directory(config, "../templates")
        toolkit.add_resource('../assets', 'ckanext-krzn')

    def get_auth_functions(self):
        """ Do not allow registering through the API """
        return {
            'user_create': no_registering
        }

    def get_helpers(self):
        return {
            'get_current_context': get_current_context,
            'is_activity_plugin_loaded': is_activity_plugin_loaded,
        }
