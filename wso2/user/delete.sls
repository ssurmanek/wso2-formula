{% for userName, user in salt['pillar.get']('users_relative', {}).items() %}
    {% if user.get('existence') == 'absent' and 'wso2is' in user.get('groups') %}
    delete_user_{{ userName }}:
        wso2is_user.absent:
            - userName: {{ userName }}
    {% endif %}
{% endfor %}
