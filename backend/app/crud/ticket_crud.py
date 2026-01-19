from sqlalchemy.orm import Session
from ..models.ticket import Ticket




def create_ticket(db: Session, ticket_data: dict) -> Ticket:
    new_ticket = Ticket(
        event_id=ticket_data['event_id'],
        ticket_type=ticket_data['ticket_type'],
        price=ticket_data['price'],
        quantity_available=ticket_data['quantity_available']
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

    
def get_tickets_by_event(db: Session, event_id: int) -> list["Ticket"]:
    return db.query(Ticket).filter(Ticket.event_id == event_id).all()