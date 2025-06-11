from fastapi import APIRouter
from pydantic import BaseModel, Field
from backend.utils.logger import logger

router = APIRouter()

class BudgetInput(BaseModel):
    budget: float = Field(..., gt=0, description="Total budget available")
    days: int = Field(..., gt=0, description="Number of travel days")

class BudgetOutput(BaseModel):
    estimated_cost: float
    remaining_budget: float
    status: str

@router.post("/estimate-budget", response_model=BudgetOutput)
def estimate_budget(data: BudgetInput):
    logger.info(f"📊 Estimating budget: budget={data.budget}, days={data.days}")
    
    avg_daily_cost = 2500  # Could later depend on destination, season, etc.
    total = data.days * avg_daily_cost
    remaining = data.budget - total
    status = "Within Budget" if remaining >= 0 else "Over Budget"

    logger.info(f"Estimated cost: {total}, Remaining: {remaining}, Status: {status}")
    
    return BudgetOutput(
        estimated_cost=total,
        remaining_budget=remaining,
        status=status
    )
