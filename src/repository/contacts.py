from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.database.models import Contact, User
from src.schemas import ContactModel
from datetime import datetime, timedelta


async def get_contacts(limit: int, offset: int, first_name: str, last_name: str, email: str, user: User, db: Session):
    first_name_query = db.query(Contact).filter(and_(Contact.first_name == first_name, Contact.user_id == user.id))
    last_name_query = db.query(Contact).filter(and_(Contact.last_name == last_name, Contact.user_id == user.id))
    email_query = db.query(Contact).filter(and_(Contact.email == email, Contact.user_id == user.id))
    if first_name and last_name and email:
        return first_name_query.union(last_name_query).union(email_query).all()
    if first_name and last_name:
        return first_name_query.union(last_name_query).all()
    if first_name and email:
        return first_name_query.union(email_query).all()
    if last_name and email:
        return last_name_query.union(email_query).all()
    if first_name:
        return first_name_query.all()
    if last_name:
        return last_name_query.all()
    if email:
        return email_query.all()
    return db.query(Contact).limit(limit).offset(offset).all()


async def get_contact_by_id(contact_id: int, user: User, db: Session):
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    return contact


async def search_contacts_by_birthday(limit: int, offset: int, user: User, db: Session):
    today = datetime.today()
    current_year = today.year
    birthdays_in_period = []

    for contact in db.query(Contact).filter(Contact.user_id == user.id).limit(limit).offset(offset).all():
        y, m, d, *_ = contact.birthday.split('-')
        contact_birthday = datetime(year=current_year, month=int(m), day=int(d))

        if today <= contact_birthday <= today + timedelta(days=7):
            birthdays_in_period.append(contact)
    return birthdays_in_period


async def create(body: ContactModel, user: User, db: Session):
    contact = Contact(**body.dict(), user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(contact_id: int, body: ContactModel, user: User, db: Session):
    contact = await get_contact_by_id(contact_id, user, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.additional_data = body.additional_data
        db.commit()
    return contact


async def remove(contact_id: int, user: User, db: Session):
    contact = await get_contact_by_id(contact_id, user, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact
