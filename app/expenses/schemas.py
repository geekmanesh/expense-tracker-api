from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator


class BaseExpenseSchema(BaseModel):
    description: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Description of expense",
        examples=["Buy Coffee"],
    )
    amount: float = Field(..., gt=0, description="Expense amount", examples=[98.99])

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Description cannot be empty")
        return value

    @field_serializer("description")
    def serialize_description(self, value: str) -> str:
        return value.capitalize()


class ExpenseCreateSchema(BaseExpenseSchema):
    pass


class ExpenseUpdateSchema(BaseExpenseSchema):
    pass


class ExpenseResponseSchema(BaseExpenseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
