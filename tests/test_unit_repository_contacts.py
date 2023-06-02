import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.database.models import Contact, User
from src.schemas import ContactModel
from src.repository.contacts import (
    get_contacts, get_contact_by_id, search_contacts_by_birthday, create, update, remove
)


class TestContacts(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.test_contact = Contact(
            id=1,
            first_name='Oleksandr',
            last_name='Gnatiuk',
            email='oleksandr@gmail.com',
            phone_number="+380678742845",
            birthday="1976-03-07"
        )

    async def test_get_contact_id(self):
        contacts = [self.test_contact, Contact(), Contact()]
        query_mock = self.session.query.return_value
        query_mock.filter.return_value = query_mock
        query_mock.first.return_value = contacts
        result = await get_contact_by_id(contact_id=self.test_contact.id, user=self.user, db=self.session)
        self.assertEqual(result[0], self.test_contact)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        query_mock = self.session.query.return_value
        query_mock.filter.return_value = query_mock
        query_mock.offset.return_value = query_mock
        query_mock.limit.return_value = query_mock
        query_mock.all.return_value = contacts
        result = await get_contacts(limit=10, offset=0, first_name="", last_name="", email="", user=self.user,
                                    db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_by_firstname(self):
        contacts = [self.test_contact, Contact(), Contact()]
        query_mock = self.session.query.return_value
        query_mock.filter.return_value = query_mock
        query_mock.offset.return_value = query_mock
        query_mock.limit.return_value = query_mock
        query_mock.all.return_value = contacts
        result = await get_contacts(limit=10, offset=0, first_name=self.test_contact.first_name, last_name="", email="", user=self.user,
                                    db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_by_lastname(self):
        contacts = [self.test_contact, Contact(), Contact()]
        query_mock = self.session.query.return_value
        query_mock.filter.return_value = query_mock
        query_mock.offset.return_value = query_mock
        query_mock.limit.return_value = query_mock
        query_mock.all.return_value = contacts
        result = await get_contacts(limit=10, offset=0, first_name="", last_name=self.test_contact.last_name, email="", user=self.user,
                                    db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_by_email(self):
        contacts = [self.test_contact, Contact(), Contact()]
        query_mock = self.session.query.return_value
        query_mock.filter.return_value = query_mock
        query_mock.offset.return_value = query_mock
        query_mock.limit.return_value = query_mock
        query_mock.all.return_value = contacts
        result = await get_contacts(limit=10, offset=0, first_name="", last_name="", email=self.test_contact.email, user=self.user,
                                    db=self.session)
        self.assertEqual(result, contacts)

    async def test_create_contact(self):
        body = ContactModel(first_name=self.test_contact.first_name,
                            last_name=self.test_contact.last_name,
                            email=self.test_contact.email,
                            phone_number=self.test_contact.phone_number,
                            birthday=self.test_contact.birthday,
                            additional_data="")
        result = await create(body=body, user=self.user, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertTrue(hasattr(result, "id"))



    # async def test_remove_note_found(self):
    #     note = Note()
    #     self.session.query().filter().first.return_value = note
    #     result = await remove_note(note_id=1, user=self.user, db=self.session)
    #     self.assertEqual(result, note)
    #
    # async def test_remove_note_not_found(self):
    #     self.session.query().filter().first.return_value = None
    #     result = await remove_note(note_id=1, user=self.user, db=self.session)
    #     self.assertIsNone(result)
    #
    # async def test_update_note_found(self):
    #     body = NoteUpdate(title="test", description="test note", tags=[1, 2], done=True)
    #     tags = [Tag(id=1, user_id=1), Tag(id=2, user_id=1)]
    #     note = Note(tags=tags)
    #     self.session.query().filter().first.return_value = note
    #     self.session.query().filter().all.return_value = tags
    #     self.session.commit.return_value = None
    #     result = await update_note(note_id=1, body=body, user=self.user, db=self.session)
    #     self.assertEqual(result, note)
    #
    # async def test_update_note_not_found(self):
    #     body = NoteUpdate(title="test", description="test note", tags=[1, 2], done=True)
    #     self.session.query().filter().first.return_value = None
    #     self.session.commit.return_value = None
    #     result = await update_note(note_id=1, body=body, user=self.user, db=self.session)
    #     self.assertIsNone(result)
    #
    # async def test_update_status_note_found(self):
    #     body = NoteStatusUpdate(done=True)
    #     note = Note()
    #     self.session.query().filter().first.return_value = note
    #     self.session.commit.return_value = None
    #     result = await update_status_note(note_id=1, body=body, user=self.user, db=self.session)
    #     self.assertEqual(result, note)
    #
    # async def test_update_status_note_not_found(self):
    #     body = NoteStatusUpdate(done=True)
    #     self.session.query().filter().first.return_value = None
    #     self.session.commit.return_value = None
    #     result = await update_status_note(note_id=1, body=body, user=self.user, db=self.session)
    #     self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
