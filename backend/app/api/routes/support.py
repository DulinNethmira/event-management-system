from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.core.database import get_db
from app.api.crud.ticket_crud import (
    create_ticket,
    get_user_tickets,
    get_all_tickets,
    get_ticket_by_id,
    get_ticket_messages,
    add_message_to_ticket,
    update_ticket,
    delete_ticket
)
from app.api.schemas.ticket_schema import (
    TicketCreate,
    TicketUpdate,
    TicketResponse,
    TicketWithMessages,
    TicketMessageCreate,
    TicketMessageResponse
)

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TicketResponse)
def create_support_ticket(
    ticket_data: TicketCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        ticket = create_ticket(db, user_id, ticket_data)
        return ticket
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create ticket: {str(e)}"
        )


@router.get("/my-tickets", response_model=List[TicketResponse])
def get_my_tickets(
    user_id: int,
    db: Session = Depends(get_db)
):
    tickets = get_user_tickets(db, user_id)
    return tickets


@router.get("/all", response_model=List[TicketResponse])
def get_all_support_tickets(
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    tickets = get_all_tickets(db, status_filter)
    return tickets


@router.get("/{ticket_id}", response_model=TicketWithMessages)
def get_ticket_details(
    ticket_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    ticket = get_ticket_by_id(db, ticket_id, user_id)
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    messages = get_ticket_messages(db, ticket_id)
    
    response_data = TicketResponse.model_validate(ticket)
    return TicketWithMessages(
        **response_data.model_dump(),
        messages=[TicketMessageResponse.model_validate(msg) for msg in messages]
    )


@router.post("/{ticket_id}/messages", response_model=TicketMessageResponse)
def add_ticket_message(
    ticket_id: int,
    message_data: TicketMessageCreate,
    user_id: int,
    is_staff: bool = False,
    db: Session = Depends(get_db)
):
    ticket = get_ticket_by_id(db, ticket_id)
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    if ticket.status == "closed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot add messages to closed ticket"
        )
    
    message = add_message_to_ticket(
        db, 
        ticket_id, 
        user_id, 
        message_data.message, 
        is_staff
    )
    
    return message


@router.patch("/{ticket_id}", response_model=TicketResponse)
def update_support_ticket(
    ticket_id: int,
    ticket_update: TicketUpdate,
    user_id: int,
    db: Session = Depends(get_db)
):
    ticket = get_ticket_by_id(db, ticket_id, user_id)
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    updated_ticket = update_ticket(db, ticket_id, ticket_update)
    
    return updated_ticket


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_support_ticket(
    ticket_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    ticket = get_ticket_by_id(db, ticket_id, user_id)
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    delete_ticket(db, ticket_id)
    
    return None