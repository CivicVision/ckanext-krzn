import os

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


def no_registering(context, data_dict):
    return {'success': False, 'msg': toolkit._('''You cannot register for this
        site. If you need an account, ask KRZN.''')}

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
    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.IAuthFunctions, inherit=True)

    def update_config(self, config):
        here = os.path.dirname(__file__)
        rootdir = os.path.dirname(os.path.dirname(here))

        our_public_dir = os.path.join(rootdir, 'ckanext', 'krzn', 'theme',
                'public')
        template_dir = os.path.join(rootdir, 'ckanext', 'krzn', 'theme',
                'templates')
        config['extra_public_paths'] = ','.join([our_public_dir,
                config.get('extra_public_paths', '')])
        config['extra_template_paths'] = ','.join([template_dir,
                config.get('extra_template_paths', '')])

        # set ckan.auth.create_dataset_if_not_in_organization = False

        toolkit.add_resource('theme/fanstatic_library', 'ckanext-krzn')

    def get_auth_functions(self):
        """ Do not allow registering through the API """
        return {
            'user_create': no_registering
        }

    def get_helpers(self):
        return {
            'get_current_context': get_current_context,
        }
