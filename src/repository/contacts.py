from datetime import datetime, timedelta
from pydantic import EmailStr
from sqlalchemy.orm import Session
from src.database.models import Contact
from src.schemas import ContactModel, ResponseContact


async def get_contacts(db: Session):
    contacts = db.query(Contact).all()
    return contacts


async def get_contact(contact_id: int, db):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def get_contact_by_first_name(first_name: str, db):
    contacts = db.query(Contact).filter_by(first_name=first_name).all()
    response_contacts = [ResponseContact(
        id=contact.id,
        first_name=contact.first_name,
        last_name=contact.last_name,
        phone_number=contact.phone_number,
        birthday=contact.birthday,
        email=contact.email,
        additional_data=contact.additional_data
    ) for contact in contacts]

    return response_contacts


async def get_contact_by_last_name(last_name: str, db):
    contacts = db.query(Contact).filter_by(last_name=last_name).all()
    response_contacts = [ResponseContact(
        id=contact.id,
        first_name=contact.first_name,
        last_name=contact.last_name,
        phone_number=contact.phone_number,
        birthday=contact.birthday,
        email=contact.email,
        additional_data=contact.additional_data
    ) for contact in contacts]

    return response_contacts


async def get_upcoming_birthdays(db: Session, seven_days_from_now: datetime):
    upcoming_birthdays = db.query(Contact).filter(Contact.birthday >= datetime.now(),
                                                  Contact.birthday <= seven_days_from_now).all()
    return upcoming_birthdays


async def get_contact_by_email(email: EmailStr, db):
    contact = db.query(Contact).filter_by(email=email).first()

    return contact


async def create_contact(body: ContactModel, db: Session):
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(body: ContactModel, contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birthday = body.birthday
        contact.additional_data = body.additional_data
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
