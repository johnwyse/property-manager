from django.db.models import Max
from django.test import Client, TestCase
from .models import User, Issue, Message, Unit

# Create your tests here.
class PropertyTestCase(TestCase):

    def setUp(self):

        # Create users
        u1 = User.objects.create(manager=True, tenant=False, username="user1")
        u2 = User.objects.create(manager=False, tenant=True, username="user2")
        u3 = User.objects.create(manager=True, tenant=True, username="user3")
        u4 = User.objects.create(manager=False, tenant=False, username="user4")
        
            # Same as user1, user2
        u5 = User.objects.create(manager=True, tenant=False, username="user5")
        u6 = User.objects.create(manager=False, tenant=True, username="user6")

        # Create messages
        Message.objects.create(sender=u1, recipient=u2, text="hello")
        Message.objects.create(sender=u1, recipient=u2, text="")
        Message.objects.create(sender=u1, recipient=u1, text="hello self")
        Message.objects.create(sender=u1, recipient=u5, text="hello fellow manager")
        Message.objects.create(sender=u2, recipient=u6, text="hello fellow tenant")
        Message.objects.create(sender=u1, recipient=u4, text="hello invalid double user")
        Message.objects.create(sender=u1, recipient=u4, text="hello invalid none user")

        # Create units
        Unit.objects.create(manager=u1, address="123 Hello World St")
        Unit.objects.create(manager=u1, address="")
        Unit.objects.create(manager=u2, address="123 Tenant Manager Road")
        Unit.objects.create(manager=u3, address="123 Invalid Double Road")
        Unit.objects.create(manager=u4, address="123 Invalid None Road")    

    # User tests
    def test_valid_manager_user(self):
        u1 = User.objects.get(username="user1")
        self.assertTrue(u1.is_valid_user())
    
    def test_valid_tenant_user(self):
        u2 = User.objects.get(username="user2")
        self.assertTrue(u2.is_valid_user())
    
    def test_invalid_double_user(self):
        u3 = User.objects.get(username="user3")
        self.assertFalse(u3.is_valid_user())
    
    def test_invalid_none_user(self):
        u4 = User.objects.get(username="user4")
        self.assertFalse(u4.is_valid_user())
    

    # Message tests

    def test_valid_message(self):
        m1 = Message.objects.get(text="hello")
        self.assertTrue(m1.is_valid_message())
    
    def test_invalid_blank_message(self):
        m2 = Message.objects.get(text="")
        self.assertFalse(m2.is_valid_message())
    
    def test_invalid_message_to_self(self):
        m3 = Message.objects.get(text="hello self")
        self.assertFalse(m3.is_valid_message())

    def test_invalid_message_to_same_user_type(self):
        m4 = Message.objects.get(text="hello fellow manager")
        self.assertFalse(m4.is_valid_message())
    
    def test_invalid_message_to_same_user_type(self):
        m5 = Message.objects.get(text="hello fellow tenant")
        self.assertFalse(m5.is_valid_message())

    def test_message_to_invalid_double_user(self):
        m6 = Message.objects.get(text="hello invalid double user")
        self.assertFalse(m6.is_valid_message())
    
    def test_message_to_invalid_none_user(self):
        m7 = Message.objects.get(text="hello invalid none user")
        self.assertFalse(m7.is_valid_message())
    

    # Unit Tests

    def test_valid_unit(self):
        unit1 = Unit.objects.get(address="123 Hello World St")
        self.assertTrue(unit1.is_valid_unit())
    
    def test_invalid_blank_unit(self):
        unit2 = Unit.objects.get(address="")
        self.assertFalse(unit2.is_valid_unit())
    
    def test_invalid_tenant_manager_unit(self):
        unit3 = Unit.objects.get(address="123 Tenant Manager Road")
        self.assertFalse(unit3.is_valid_unit())
    
    def test_invalid_double_user_unit(self):
        unit4 = Unit.objects.get(address="123 Invalid Double Road")
        self.assertFalse(unit4.is_valid_unit())
    
    def test_invalid_none_user_unit(self):
        unit5 = Unit.objects.get(address="123 Invalid None Road")
        self.assertFalse(unit5.is_valid_unit())



    
