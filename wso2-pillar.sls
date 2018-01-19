users:
    johndoe:
        existence: present
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
        givenName: Jane
        familyName: Doe
        password: secret
        emails:
            jane.doe@mail.com:
                primary: true
                type: work
