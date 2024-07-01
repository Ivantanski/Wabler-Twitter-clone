import unittest
from models import db, User, Message, Likes
from app import app, CURR_USER_KEY

class UserViewsTestCase(unittest.TestCase):
    """Test views for Users."""

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

    def test_homepage_logged_out(self):
        """Test homepage when logged out."""

        with self.client as c:
            resp = c.get("/")
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Sign up", resp.data)

    def test_homepage_logged_in(self):
        """Test homepage when logged in."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = c.get("/")
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"@testuser", resp.data)

    def test_add_like(self):
        """Test adding a like."""

        m = Message(text="Test message", user_id=self.testuser_id)
        db.session.add(m)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = c.post(f"/users/add_like/{m.id}", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            likes = Likes.query.filter(Likes.user_id == self.testuser_id).all()
            self.assertEqual(len(likes), 1)

if __name__ == '__main__':
    unittest.main()
