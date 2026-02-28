from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import os, uuid
from app.auth.dependencies import get_current_user
from app.ingestion.replay_runner import run_replay

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

    run_replay(path, user.id)

    return {"status": "uploaded", "file_id": file_id}
