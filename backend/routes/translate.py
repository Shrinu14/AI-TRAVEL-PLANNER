from fastapi import APIRouter, Body
from backend.modules.translate import translate_text

router = APIRouter()

@router.post("/translate")
def translate(text: str = Body(...), target_lang: str = Body(...)):
    return {"translated": translate_text(text, target_lang)}
