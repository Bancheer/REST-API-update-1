from typing import List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from src.database.connect import get_db
from src.database.models import User, Roles
from src.schemas import ResponseContact, ContactModel
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service
from src.services.roles import RoleChecker

router = APIRouter(prefix='/contacts', tags=['contacts'])

allowed_get_contacts = RoleChecker([Roles.admin, Roles.moderator, Roles.user])
allowed_create_contacts = RoleChecker([Roles.admin, Roles.moderator, Roles.user])
allowed_update_contacts = RoleChecker([Roles.admin, Roles.moderator])
allowed_remove_contacts = RoleChecker([Roles.admin])


@router.get("/", response_model=List[ResponseContact], dependencies=[Depends(allowed_get_contacts)])
async def get_contacts(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(db)
    return contacts


@router.get("/{contact_id}", response_model=ResponseContact, dependencies=[Depends(allowed_get_contacts)])
async def get_contact(contact_id: int = Path(gt=0, ge=1), db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not found")
    return contact


@router.get("/by_first_name/{first_name}", response_model=List[ResponseContact],
            dependencies=[Depends(allowed_get_contacts)])
async def get_contact_by_first_name(first_name: str, db: Session = Depends(get_db),
                                    current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_first_name(first_name, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="First_name Not found")
    return contact


@router.get("/by_last_name/{last_name}", response_model=List[ResponseContact],
            dependencies=[Depends(allowed_get_contacts)])
async def get_contact_by_last_name(last_name: str, db: Session = Depends(get_db),
                                   current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_last_name(last_name, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Last_name Not found")
    return contact


@router.get("/by_email/{email}", response_model=ResponseContact, dependencies=[Depends(allowed_get_contacts)])
async def get_contact_by_email(email: str, db: Session = Depends(get_db),
                               current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_email(email, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Email Not found")
    return contact


@router.get("/upcoming_birthdays/", response_model=List[ResponseContact], dependencies=[Depends(allowed_get_contacts)])
async def get_upcoming_birthdays(db: Session = Depends(get_db),
                                 current_user: User = Depends(auth_service.get_current_user)):
    seven_days_from_now = datetime.now() + timedelta(days=7)
    upcoming_birthdays = await repository_contacts.get_upcoming_birthdays(db, seven_days_from_now)
    if not upcoming_birthdays:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No upcoming birthdays found")

    return upcoming_birthdays


@router.post("/", response_model=ResponseContact, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(allowed_create_contacts)])
async def get_create_contact(body: ContactModel, db: Session = Depends(get_db),
                             current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.create_contact(body, db)
    return contact


@router.put("/{contact_id}", response_model=ResponseContact, dependencies=[Depends(allowed_update_contacts)])
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(body, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not Found")

    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(allowed_remove_contacts)])
async def remove_contact(contact_id: int = Path(gt=0, ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not found")
    return contact
