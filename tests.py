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


    def test_chat(self):
       c = Chat(text='Hello, world!')
       self.assertNotEqual(str(c.text), 'Chat <Hello, world!>')

    def test_ranks(self):
        r = Rank(rank_name='Gold')
        self.assertNotEqual(str(r.rank_name), 'Rank <Silver I>')
        self.assertEqual(str(r.rank_name), 'Gold')


    def test_fav_map_representation(self):
        fm = FavMap()
        self.assertEqual(str(fm), '<FavMap None>')
       
if __name__ == '__main__':
    unittest.main(verbosity=2)