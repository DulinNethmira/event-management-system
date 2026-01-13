from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.models.ticket import Ticket, TicketMessage
from app.api.schemas.ticket_schema import TicketCreate, TicketUpdate


def create_ticket(db: Session, user_id: int, ticket_data: TicketCreate) -> Ticket:
    new_ticket = Ticket(
        user_id=user_id,
        subject=ticket_data.subject,
        category=ticket_data.category,
        priority=ticket_data.priority,
        status="open"
    )
    
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    
    first_message = TicketMessage(
        ticket_id=new_ticket.id,
        user_id=user_id,
        message=ticket_data.message,
        is_staff_reply=0
    )
    
    db.add(first_message)
    db.commit()
    
    return new_ticket


def get_user_tickets(db: Session, user_id: int) -> List[Ticket]:
    return db.query(Ticket).filter(
        Ticket.user_id == user_id
    ).order_by(Ticket.created_at.desc()).all()


def get_all_tickets(db: Session, status: Optional[str] = None) -> List[Ticket]:
    query = db.query(Ticket)
    
    if status:
        query = query.filter(Ticket.status == status)
    
    return query.order_by(Ticket.created_at.desc()).all()


def get_ticket_by_id(db: Session, ticket_id: int, user_id: Optional[int] = None) -> Optional[Ticket]:
    query = db.query(Ticket).filter(Ticket.id == ticket_id)
    
    if user_id:
        query = query.filter(Ticket.user_id == user_id)
    
    return query.first()


def get_ticket_messages(db: Session, ticket_id: int) -> List[TicketMessage]:
    return db.query(TicketMessage).filter(
        TicketMessage.ticket_id == ticket_id
    ).order_by(TicketMessage.created_at.asc()).all()


def add_message_to_ticket(
    db: Session, 
    ticket_id: int, 
    user_id: int, 
    message: str, 
    is_staff: bool = False
) -> TicketMessage:
    new_message = TicketMessage(
        ticket_id=ticket_id,
        user_id=user_id,
        message=message,
        is_staff_reply=1 if is_staff else 0
    )
    
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    
    return new_message


def update_ticket(
    db: Session, 
    ticket_id: int, 
    ticket_update: TicketUpdate
) -> Optional[Ticket]:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    
    if not ticket:
        return None
    
    if ticket_update.status:
        ticket.status = ticket_update.status
    
    if ticket_update.priority:
        ticket.priority = ticket_update.priority
    
    db.commit()
    db.refresh(ticket)
    
    return ticket


def delete_ticket(db: Session, ticket_id: int) -> bool:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    
    if not ticket:
        return False
    
    db.query(TicketMessage).filter(TicketMessage.ticket_id == ticket_id).delete()
    db.delete(ticket)
    db.commit()
    
    return True