from typing import List, Optional, Sequence
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.models import Contact, User


class ContactService:
    @staticmethod
    async def get_all_for_user(
        db: AsyncSession, user: User, skip: int = 0, limit: int = 100
    ) -> Sequence[Contact]:
        result = await db.execute(
            select(Contact)
            .where(Contact.user_id == user.id)
            .offset(skip)
            .limit(limit)
            .order_by(Contact.created_at.desc())
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_id_for_user(
        db: AsyncSession, user: User, contact_id: str
    ) -> Optional[Contact]:
        result = await db.execute(
            select(Contact).where(Contact.id == contact_id, Contact.user_id == user.id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_for_user(db: AsyncSession, user: User, data: dict) -> Contact:
        contact = Contact(user_id=user.id, **data)
        db.add(contact)
        await db.commit()
        await db.refresh(contact)
        return contact

    @staticmethod
    async def update_for_user(
        db: AsyncSession, user: User, contact_id: str, data: dict
    ) -> Optional[Contact]:
        contact = await ContactService.get_by_id_for_user(db, user, contact_id)
        if not contact:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(contact, key, value)
        await db.commit()
        await db.refresh(contact)
        return contact

    @staticmethod
    async def delete_for_user(db: AsyncSession, user: User, contact_id: str) -> bool:
        result = await db.execute(
            delete(Contact).where(Contact.id == contact_id, Contact.user_id == user.id)
        )
        await db.commit()
        return result.rowcount > 0
