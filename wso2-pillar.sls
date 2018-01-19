users:
    johndoe:
        existence: present
        id: da22c6a0-fd00-11e7-9db1-fa163ec08874
        givenName: John
        familyName: Doe
        password: secret
        emails:
            john.doe@mail.com:
                primary: true
                type: work
            john@doe.com:
                primary: false
                type: home
    johnsmith:
        existence: present
        id: e7ebde98-fd00-11e7-9db1-fa163ec08874
        givenName: John
        familyName: Smith
        password: secret
        emails:
            john.smith@mail.com:
                primary: true
                type: work
            john@smith.com:
                primary: false
                type: other
    janedoe:
        existence: absent
        id: fbdcd5ba-fd00-11e7-9db1-fa163ec08874
        givenName: Jane
        familyName: Doe
        password: secret
        emails:
            jane.doe@mail.com:
                primary: true
                type: work
