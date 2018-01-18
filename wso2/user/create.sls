{% for id, user in salt['pillar.get']('users', {}).items() %}
    {% set emails = user.get('emails') %}
    create_user_{{ id }}:
        wso2is_user.present:
            - familyName: {{ user.get('familyName') }}
            - givenName: {{ user.get('givenName') }}
            - password: {{ user.get('password') }}
            - userName: {{ user.get('userName') }}
            - emails:
                #{% for id, email in salt['pillar.get']('users.emails', {}).items() %}
                {% for id, email in emails.items() %}
                - {{ id }}:
                    - primary: {{ emails.get('primary') }}
                    - type: {{ emails.get('type') }}
                {% endfor %}    
{% endfor %}
