


Zabbix-example:
    zabbix_user.present:
        - alias: George
        - passwd: donottellanyonE@456x
        - password_reset: True
        - usrgrps:
            - 13
            - 7
        - medias:
            - me@example.com:
                - mediatype: mail
                - period: '1-7,00:00-24:00'
                - severity: NIWAHD
            - make_jabber:
                - active: true
                - mediatype: jabber
                - period: '1-5,08:00-19:00'
                - sendto: jabbera@example.com
            - text_me_morning_disabled:
                - active: false
                - mediatype: sms
                - period: '1-5,09:30-10:00'
                - severity: D
                - sendto: '+42032132588568'
