import unittest
from models import db, User, Message
from app import app, CURR_USER_KEY

class MessageViewsTestCase(unittest.TestCase):
    """Test views for Messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testpassword",
                                    image_url=None)
        self.testuser_id = 1000
        self.testuser.id = self.testuser_id

        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_add_message(self):
        """Test adding a message."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = c.post("/messages/new", data={"text": "Hello"}, follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Hello", resp.data)

    def test_delete_message(self):
        """Test deleting a message."""

        m = Message(text="Test message", user_id=self.testuser_id)
        db.session.add(m)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = c.post(f"/messages/{m.id}/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            msg = Message.query.get(m.id)
            self.assertIsNone(msg)

if __name__ == '__main__':
    unittest.main()
