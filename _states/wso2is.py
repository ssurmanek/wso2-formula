
'''
Module for working with the WSO2 Identity Server SCIM API

.. versionadded:: 2017.7.0

:depends: requests

:configuration: This module requires a configuration profile to be configured
    in the minion config, minion pillar, or master config.
    The module will use the 'grafana' key by default, if defined.

    For example:

    .. code-block:: yaml

        wso2is:
            wso2is_url: https://localhost:9443
            wso2is_admin: admin
            wso2is_password: admin
'''
from __future__ import absolute_import

try:
    import requests
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False

from salt.ext.six import string_types

__virtualname__ = 'wso2is'


def __virtual__():
    '''
    Only load if requests is installed
    '''
    if HAS_LIBS:
        return __virtualname__
    else:
        return False, 'The "{0}" module could not be loaded: ' \
                      '"requests" is not installed.'.format(__virtualname__)
def _get_auth(profile):
    return requests.auth.HTTPBasicAuth(
        profile['wso2is_admin'],
        profile['wso2is_password']
    )

def fulfill_user_schema(params, **optionalParams):
    #fulfill user attributes schema with optional attributes
    if 'emails' in optionalParams:
        params['emails'] = optionalParams['emails']
    name ={}
    if 'familyName' in optionalParams:
        name['familyName'] = optionalParams['familyName']
    if 'givenName' in optionalParams:
        name['givenName'] = optionalParams['givenName']
    if bool(name):
        params['name'] = name
    return params

def create_user(profile='wso2is', userName=None, password=None, **kwargs):
    '''
    Create a new user.

    profile - configuration profile used to connect WSO2 endpoint, default: wso2is
    userName - username of the user, required, imutable
    password - password of the user, required
    familyName - family name of the user, optional
    givenName - given name of the user, optional
    emails - array of email addresses with their properties, optional

    CLI example:

        salt '*' wso2is.create_user userName='<username>' password='<password>' familyName='<FamilyName>' givenName='<GivenName>' emails='[{"primary":<true/fasle>,"value":"<email address>","type":"<home/work>"}]'
    '''

    if userName is None or password is None:
        return False, 'userName and/or password is missing in parameters'    
    if isinstance(profile, string_types):
        profile = __salt__['config.option'](profile)
    params = {"userName": userName, "password": password, }
    params = fulfill_user_schema(params, **kwargs)
    response = requests.post(
        '{0}/wso2/scim/Users'.format(profile['wso2is_url']),
        json=params,
        auth=_get_auth(profile),
        headers={'Content-type': 'application/json'},
        verify=False,
    )
    if response.status_code >= 400:
        response.raise_for_status()
    return response.json()

def get_users(profile='wso2is'):
    '''
    List all users.

    profile - configuration profile used to connect WSO2 endpoint, default: wso2is

    CLI example:
    
        salt '*' wso2is.get_users
    '''
    if isinstance(profile, string_types):
        profile = __salt__['config.option'](profile)
    response = requests.get(
        '{0}/wso2/scim/Users'.format(profile['wso2is_url']),
        auth=_get_auth(profile),
        headers={'Content-type': 'application/json'},
        verify=False,
    )
    if response.status_code >= 400:
        response.raise_for_status()
    data = response.json()
    users = data['Resources']

    return users

def get_user(profile='wso2is', userId=None):
    '''
    Show a single user.

    profile - configuration profile used to connect WSO2 endpoint, default: wso2is
    userId - ID of the user, required, imutable

    CLI example:

        salt '*' wso2is.get_user iserId='<userId>'
    '''
    if userId is None:
        return False, 'userId is missing in parameters'
    
    if isinstance(profile, string_types):
        profile = __salt__['config.option'](profile)
    response = requests.get(
        '{0}/wso2/scim/Users/{1}'.format(profile['wso2is_url'], userId),
        auth=_get_auth(profile),
        headers={'Content-type': 'application/json'},
        verify=False,
    )
    if response.status_code >= 400:
        response.raise_for_status()
    return response.json()

#plus sign in query parameter is problem!!
def exists_user(profile='wso2is', userName=None):
    '''
    Confirm existence of a user. If exists return user data else None.

    profile - configuration profile used to connect WSO2 endpoint, default: wso2is
    userName - username of the user, required, imutable

    CLI example:

        salt '*' wso2is.exists_user userName='<userName>'
    '''
    if userName is None:
        return False, 'userName is missing in parameters'
    if isinstance(profile, string_types):
        profile = __salt__['config.option'](profile)

    users = get_users(profile)
    #return data
    #users = json.dupms(data)
    for user in users:
        if user['userName'] == userName:
            return user
    return False


def update_user(profile='wso2is', userId=None, userName=None, **kwargs):
    '''
    Update a user.
    
    profile - configuration profile used to connect WSO2 endpoint, default: wso2is
    userId - ID of the user, required, imutable
    userName - username of the user, required, imutable
    familyName - family name of the user, optional
    givenName - given name of the user, optional
    emails - array of email addresses with their properties, optional

    CLI example:

        salt '*' wso2is.update_user userId='<userId>' userName='<username>' familyName='<FamilyName>' givenName='<GivenName>' emails='[{"primary":<true/fasle>,"value":"<email_address>","type":"<home/work>"}]'
    '''
    if userId is None:
        return False, 'userId is missing in parameters'
    if userName is None:
        return False, 'userName is missing in parameters'
    if isinstance(profile, string_types):
        profile = __salt__['config.option'](profile)
    params = {"userName": userName, }
    params = fulfill_user_schema(params, **kwargs)
    response = requests.put(
        '{0}/wso2/scim/Users/{1}'.format(profile['wso2is_url'], userId),
        json=params,
        auth=_get_auth(profile),
        headers={'Content-type': 'application/json'},
        verify=False,
    )
    if response.status_code >= 400:
        response.raise_for_status()
    return response.json()

def delete_user(profile='wso2is', userId=None):
    '''
    Delete a user.
    
    userId - ID of the user, required

    CLI example:
   
        salt '*' wso2is.delete_user userId='<userId>'
    '''
    if userId is None:
        return False, 'userId is missing in parameters'
    if isinstance(profile, string_types):
        profile = __salt__['config.option'](profile)
    response = requests.delete(
        '{0}/wso2/scim/Users/{1}'.format(profile['wso2is_url'], userId),
        auth=_get_auth(profile),
        headers={'Content-type': 'application/json'},
        verify=False,
    )
    if response.status_code >= 400:
        response.raise_for_status()
    if response.status_code == 200:
        return True
