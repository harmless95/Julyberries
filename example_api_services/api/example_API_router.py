from fastapi import APIRouter

from utils.create_API_data import create_data

router = APIRouter(prefix="/valute")


@router.get("/")
async def get_all_valute():
    result = await create_data()
    return result


@router.get("/{char_code}/")
async def get_char_code(char_code: str):
    data = await create_data()
    for valute in data["ValCurs"]["Valute"]:
        if valute.get("CharCode") == char_code:
            return valute
    return {"error": "CharCode not found"}
