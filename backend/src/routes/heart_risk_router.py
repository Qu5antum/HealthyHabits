from fastapi import APIRouter, status
from backend.src.security.security import *
from backend.src.services.risk_form_service import *
from backend.src.models.schemas import *
from backend.src.database.db import get_session
from backend.src.dependencies.dependencies import get_current_user
from backend.src.model_and_data_analys.predict_risk import filter_by_user_age_and_sex

router = APIRouter(
    prefix="/heart_risk_form",
    tags=["heart_risk_form"]
)

@router.post("", status_code=status.HTTP_200_OK)
async def heart_risk_form_for_user(
    heart_risk_form: HeartRiskInput,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await add_risk_form_by_user(
        session=session,
        user_id=user.id,
        form=heart_risk_form
    )

@router.get("", status_code=status.HTTP_200_OK)
async def get_form_and_result(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await filter_by_user_age_and_sex(session=session, user_id=user.id)
    


@router.put("/update", status_code=status.HTTP_200_OK)
async def update_form(
    risk_form: HeartRiskInput,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await update_form_by_user(session=session, user_id=user.id, risk_form=risk_form)

   




    