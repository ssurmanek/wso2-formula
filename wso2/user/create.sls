update_pillar:
    salt.runner:
        - name: git_pillar.update
        - branch: master
        - repo: https://github.com/ssurmanek/users-data.git

{% for userName, user in salt['pillar.get']('users', {}).items() %}
    {% if user.get('existence') == 'present' %}
    create_user_{{ userName }}:
        wso2is_user.present:
            - familyName: {{ user.get('familyName') }}
            - givenName: {{ user.get('givenName') }}
            - password: {{ user.get('password') }}
            - userName: {{ userName }}
            - emails:
            {% set emails = user.get('emails') %}
            {% for emailValue, email in emails.items() %}
                - {{ emailValue }}:
                    - primary: {{ email.get('primary') }}
                    - type: {{ email.get('type') }}
            {% endfor %}
    {% endif %}
{% endfor %}
