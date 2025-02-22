import uuid
import json
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

api = FastAPI()

# Archivo donde se guardarán los datos
DATA_FILE = "users.json"

# Cargar datos al iniciar la API
try:
    with open(DATA_FILE, "r") as f:
        users = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    users = {}

@api.post(path="/user", tags=["User"])
async def user_register(data: dict):
    user_id = str(uuid.uuid4())  # Genera un ID único
    user = {
        "id": user_id,
        "name": data["name"],
        "email": data["email"],
        "username": data["username"]
    }

    users[user_id] = user

    # Guardar en JSON
    with open(DATA_FILE, "w") as f:
        json.dump(users, f)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            **user,
            "response": f"Se ha creado exitosamente el usuario {data['username']} con el email {data['email']}"
        }
    )

@api.get(path="/user/{user_id}", tags=["User"])
async def get_user(user_id: str):
    try:
        # Recargar datos desde el archivo
        with open(DATA_FILE, "r") as f:
            users = json.load(f)

        user = users[user_id]  # Buscar usuario por ID
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=user
        )
    except (KeyError, FileNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Usuario no encontrado"}
        )
