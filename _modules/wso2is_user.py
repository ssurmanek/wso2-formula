from __future__ import absolute_import

from salt.ext.six import string_types
from salt.utils import dictupdate
from salt.utils.dictdiffer import deep_diff
from json import loads, dumps

import ast

def __virtual__():
    '''
    Only make these states available if Zabbix module is available.
    '''
    return 'wso2is.create_user' in __salt__

def pop_if_exists(attrs_dict, attr):
    if attr in attrs_dict:
        return attrs_dict.pop(attr)
    else:
        return {}

def present(familyName, givenName, password, emails, userName=None):
    '''
    Ensures that the user exists, eventually creates new user.

    profile - configuration profile used to connect WSO2 endpoint, default: wso2is
    userName - username of the user, imutable
    password - password of the user, imutable
    familyName - family name of the user
    givenName - given name of the user
    emails - list of email addresses with their properties:
        primary - valid values: true, false
        type - valid values: work, home, other (emails with the other types will be ignored)

    YAML example:
        wso2is_user.present:
            - familyName: George
            - givenName: App
            - password: secret
            - userName: georgeapp
            - emails:
                - george@example.com:
                    - primary: true
                    - type: work
                - george@mail.com:
                    - primary: false
                    - type: home
    CLI example:
        salt '*' state.apply wso2.user.delete
    '''
    if userName == None:
        return False, 'userName is missing in parameters'

    ret = {'name': userName, 'changes': {}, 'result': False, 'comment': ''}

    #format emails: 
    valid_types = ('home', 'work', 'other')    
    formated_emails = list()
    for email in emails:
        for mail_addr in email:
            emails_dict = dict()
            for mail_attr in email[mail_addr]:
                for key, value in mail_attr.items():
                    if key == 'type' and value in valid_types:
                        emails_dict[key] = value
                        emails_dict['value'] = mail_addr
        if emails_dict:
            formated_emails.append(emails_dict)
    
    existing_user = __salt__['wso2is.exists_user'](userName=userName)
    #create user:
    if not existing_user:
        user = __salt__['wso2is.create_user'](
            userName=userName,
            password=password,
            emails=formated_emails,
            familyName=familyName,
            givenName=givenName)
        if user or user is not None:
            ret['changes']['new'] = user
            ret['changes']['old'] = 'User {0} does not exists.'.format(userName)
            ret['result']=True
            ret['comment']='User {0} created.'.format(userName)
    
    #check if changes are needed:
    if existing_user:
        userId=existing_user.get("id")
        current_user=__salt__['wso2is.get_user'](userId=userId)
        current_user_copy = current_user.copy()
        pop_if_exists(current_user, 'meta')
        pop_if_exists(current_user, 'schemas')
        pop_if_exists(current_user, 'id')
        current_emails = pop_if_exists(current_user, 'emails')
        current_name = pop_if_exists(current_user, 'name')
        #compare emails:
        emails_diff = [x for x in current_emails if x not in formated_emails] + \
                      [y for y in formated_emails if y not in current_emails]  
        #compare names:
        required_name = {'familyName':familyName, 'givenName':givenName}
        name_diff = cmp(current_name, required_name)
        
        #no changes needed:
        if not emails_diff and name_diff==0:
            ret['result']=True
            ret['comment']='User {0} already up-to-date.'.format(userName)
        #update user:
        else:
            user = __salt__['wso2is.update_user'](
            userId=userId,
            userName=userName,
            emails=formated_emails,
            familyName=familyName,
            givenName=givenName)
            if user or user is not None:
                ret['changes']['new'] = user
                ret['changes']['old'] = current_user_copy
                ret['result']=True
                ret['comment']='User {0} updated.'.format(userName)
    return ret

def absent(profile='wso2is', userName=None):
    '''
    Ensures that the user does not exist, eventually deletes user.
    
    userName - username of the user
    
    YAML example:
        wso2is_user.absent:
            - userName: georgeapp
    CLI example:
        salt '*' state.apply wso2.user.create
    '''
    if userName == None:
        return False, 'userName is missing in parameters'

    ret = {'name': userName, 'changes': {}, 'result': False, 'comment': ''}
    
    existing_user = __salt__['wso2is.exists_user'](userName=userName)
    
    if not existing_user:
        ret['result'] = True
        ret['comment'] = 'User {0} does not exist.'.format(userName)
    else:
        userId=existing_user.get("id")
        deleted = __salt__['wso2is.delete_user'](profile=profile, userId=userId)
        if deleted:
            ret['result'] = True
            ret['comment'] = 'User {0} deleted.'.format(userName)
            ret['changes']['new'] = 'User {0} does not exists'.format(userName)
            ret['changes']['old'] = existing_user
        else:
            ret['result'] = False
            ret['comment'] = 'Unable to delete user {0}.'.format(userName)
    return ret
