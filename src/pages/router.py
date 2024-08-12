import logging

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from src.operations.router import get_specific_operations

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


pages_router = APIRouter(
    prefix="/pages",
    tags=["Pages"]
)


templates = Jinja2Templates(directory='src/templates')


@pages_router.get("/base")
def get_base_page(request: Request):
    logger.info(request)
    return templates.TemplateResponse("base.html", {"request": request})


@pages_router.get("/search/{operation_type}")
def get_search_page(request: Request, operation=Depends(get_specific_operations)):
    logger.info(request)
    return templates.TemplateResponse("search.html", {"request": request, "operations": operation['data']})
