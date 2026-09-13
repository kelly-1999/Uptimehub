from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.monitor import Monitor
from app.schemas.monitor import (
    MonitorCreate,
    MonitorResponse,
    MonitorUpdate,
)
from app.services.monitor_checker import check_monitor


router = APIRouter(
    prefix="/api/v1/monitors",
    tags=["Monitors"],
)


@router.post(
    "",
    response_model=MonitorResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_monitor(
    monitor_data: MonitorCreate,
    db: Session = Depends(get_db),
):
    monitor = Monitor(
        name=monitor_data.name,
        url=monitor_data.url,
        interval_seconds=monitor_data.interval_seconds,
        is_active=monitor_data.is_active,
    )

    db.add(monitor)
    db.commit()
    db.refresh(monitor)

    return monitor


@router.get(
    "",
    response_model=list[MonitorResponse],
)
def list_monitors(
    db: Session = Depends(get_db),
):
    statement = select(Monitor).order_by(Monitor.id)

    monitors = db.scalars(statement).all()

    return monitors


@router.get(
    "/{monitor_id}",
    response_model=MonitorResponse,
)
def get_monitor(
    monitor_id: int,
    db: Session = Depends(get_db),
):
    monitor = db.get(Monitor, monitor_id)

    if monitor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitor not found",
        )

    return monitor


@router.put(
    "/{monitor_id}",
    response_model=MonitorResponse,
)
def update_monitor(
    monitor_id: int,
    monitor_data: MonitorUpdate,
    db: Session = Depends(get_db),
):
    monitor = db.get(Monitor, monitor_id)

    if monitor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitor not found",
        )

    update_data = monitor_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(monitor, field, value)

    db.commit()
    db.refresh(monitor)

    return monitor


@router.delete(
    "/{monitor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_monitor(
    monitor_id: int,
    db: Session = Depends(get_db),
):
    monitor = db.get(Monitor, monitor_id)

    if monitor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitor not found",
        )

    db.delete(monitor)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{monitor_id}/check",
    response_model=MonitorResponse,
)
def check_monitor_now(
    monitor_id: int,
    db: Session = Depends(get_db),
):
    monitor = db.get(Monitor, monitor_id)

    if monitor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitor not found",
        )

    monitor = check_monitor(monitor)

    db.commit()
    db.refresh(monitor)

    return monitor
