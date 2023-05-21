import os
os.environ['DATABASE_URL'] = 'sqlite://'

from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Chat, FavWeapon, Weapon, FavMap, Map, Rank, Commands

class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='bobby')
        u.set_password('1234')
        self.assertFalse(u.check_password('123'))
        self.assertTrue(u.check_password('1234'))

    def test_avatar(self):
        u = User(username='shaun', email='shaun@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?d=identicon&s=128'))

    def test_chat(self):
       c = Chat(text='Hello, world!')
       self.assertEqual(str(c), '<Chat Hello, world!>')

    def test_ranks(self):
        r = Rank(rank_name='Gold')
        self.assertNotEqual(str(r), '<Silver I>')

    def test_fav_map_representation(self):
        fm = FavMap()
        self.assertEqual(str(fm), '<Anubis>')
       
if __name__ == '__main__':
    unittest.main(verbosity=2)