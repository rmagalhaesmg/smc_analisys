from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import os, uuid
import asyncio
from ..auth.dependencies import get_current_user
from .replay_runner import ReplayRunner

router = APIRouter()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_csv(
    file: UploadFile = File(...),
    user=Depends(get_current_user)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(400, "Arquivo inválido")

    file_id = f"{uuid.uuid4()}.csv"
    path = os.path.join(UPLOAD_DIR, file_id)

    with open(path, "wb") as f:
        f.write(await file.read())

    # TODO: Integração com o replay runner
    # Por enquanto, apenas retorna o resultado do upload
    # run_replay(path, user.id)

    return {"status": "uploaded", "file_id": file_id, "path": path}


@router.post("/backtest")
async def run_backtest(
    file_id: str,
    user=Depends(get_current_user)
):
    """Roda backtest com arquivo já carregado"""
    path = os.path.join(UPLOAD_DIR, file_id)
    
    if not os.path.exists(path):
        raise HTTPException(404, "Arquivo não encontrado")
    
    # TODO: Integrar com ReplayRunner
    return {"status": "processing", "file_id": file_id}
