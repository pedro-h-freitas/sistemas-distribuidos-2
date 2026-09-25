
from typing import Annotated

from fastapi import Depends

from app.database import get_db


DatabaseDep = Annotated[dict, Depends(get_db)]
