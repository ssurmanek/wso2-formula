create_user:
    wso2is_user.present:
        - familyName: George
        - givenName: Application
        - password: secret
        - userName: georgeapp
        - emails:
            - george@example.com:
                - primary: true
                - type: work
            - george@mail.com:
                - primary: false
                - type: home
            - not-valid@mail.com:
                - primary: false
                - type: mytype    
