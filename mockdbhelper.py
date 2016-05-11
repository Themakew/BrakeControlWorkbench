MOCK_USERS = {'admin':'admin'}


class MockDBHelper:

    def get_user(self, email):
        if email in MOCK_USERS:
            return MOCK_USERS[email]
        return None
