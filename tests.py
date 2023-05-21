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
        # Test password hashing
        u = User(username='bobby')
        u.set_password('1234')
        self.assertFalse(u.check_password('123'))
        self.assertTrue(u.check_password('1234'))


    def test_chat(self):
       # Test chat text representation
       c = Chat(text='Hello, world!')
       self.assertNotEqual(str(c.text), 'Chat <Hello, world!>')

    def test_ranks(self):
        # Test rank name representation
        r = Rank(rank_name='Gold')
        self.assertNotEqual(str(r.rank_name), 'Rank <Silver I>')
        self.assertEqual(str(r.rank_name), 'Gold')


    def test_fav_map_representation(self):
        # Test representation of FavMap object
        fm = FavMap()
        self.assertEqual(str(fm), '<FavMap None>')
    
    def test_user_representation(self):
        # Test representation of User object
        u = User(username='test', email='test@example.com')
        db.session.add(u)
        db.session.commit()
        self.assertEqual(str(u), '<User test>')

    def test_chat_save(self):
        # Test saving and retrieving Chat object
        u = User(username='test', email='test@example.com')
        db.session.add(u)
        db.session.commit()
        c = Chat(text='Hello, world!', user_id=u.id)
        db.session.add(c)
        db.session.commit()
        retrieved_chat = Chat.query.filter_by(user_id=u.id).first()
        self.assertIsNotNone(retrieved_chat)
        self.assertEqual(retrieved_chat.text, 'Hello, world!')

    def test_weapon_representation(self):
        # Test representation of Weapon object
        w = Weapon(weapon_name='AK-47', category='Rifle', description='Powerful and reliable rifle.')
        self.assertEqual(str(w), '<Weapon AK-47>')

    def test_map_representation(self):
        # Test representation of Map object
        m = Map(map_name='Dust II')
        self.assertEqual(str(m), '<Map Dust II>')

    def test_command_representation(self):
        # Test representation of Commands object
        cmd = Commands(command_name='Help', query_command='/help')
        self.assertEqual(str(cmd), '<Commands Help>')
       
if __name__ == '__main__':
    unittest.main(verbosity=2)