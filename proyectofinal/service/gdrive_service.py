import os
from typing import Optional
import time
from datetime import datetime

from google.oauth2.service_account import Credentials  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.http import MediaFileUpload  # type: ignore

# Cargar variables desde .env si está presente
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass


def _get_drive_service():
    service_account_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    # Fallback: credentials.json en el root del proyecto
    if not service_account_file:
        candidate = os.path.join(project_root, "credentials.json")
        if os.path.exists(candidate):
            service_account_file = candidate

    # Si la var existe pero es relativa y no existe, intentar resolver respecto al root del proyecto
    if service_account_file and not os.path.isabs(service_account_file) and not os.path.exists(service_account_file):
        candidate = os.path.join(project_root, service_account_file)
        if os.path.exists(candidate):
            print(f"[GDRIVE] Resuelto GOOGLE_SERVICE_ACCOUNT_FILE relativo a: {candidate}")
            service_account_file = candidate

    if not service_account_file or not os.path.exists(service_account_file):
        raise FileNotFoundError(
            "No se encontró el archivo de credenciales. Define GOOGLE_SERVICE_ACCOUNT_FILE o coloca credentials.json en el root del proyecto."
        )

    print(f"[GDRIVE] Usando credenciales: {service_account_file}")

    scopes = [
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_file(service_account_file, scopes=scopes)
    service = build("drive", "v3", credentials=creds)
    try:
        about = service.about().get(fields="user(emailAddress,displayName)").execute()
        user = about.get("user", {})
        print(f"[GDRIVE] Conectado como: {user.get('displayName')} <{user.get('emailAddress')}>")
    except Exception as e:
        print(f"[GDRIVE] Error consultando 'about': {e}")
    return service


def _resolve_folder_id(service, folder_hint: Optional[str]) -> Optional[str]:
    if not folder_hint:
        return None
    # Si parece un ID (contiene guiones y longitud típica), úsalo tal cual
    if len(folder_hint) >= 10 and "/" not in folder_hint and " " not in folder_hint:
        return folder_hint
    # De lo contrario, intentar resolver por nombre
    try:
        print(f"[GDRIVE] Resolviendo carpeta por nombre: {folder_hint}")
        q = (
            "mimeType='application/vnd.google-apps.folder' and trashed=false and name='"
            + folder_hint.replace("'", "\'")
            + "'"
        )
        res = (
            service.files()
            .list(q=q, fields="files(id,name)", pageSize=1, spaces="drive")
            .execute()
        )
        files = res.get("files", [])
        if files:
            folder_id = files[0]["id"]
            print(f"[GDRIVE] Carpeta encontrada. id={folder_id} name={files[0]['name']}")
            return folder_id
        print("[GDRIVE] Carpeta no encontrada por nombre. Se subirá al root.")
    except Exception as e:
        print(f"[GDRIVE] Error resolviendo carpeta por nombre: {e}. Se subirá al root.")
    return None


def upload_image_to_drive(
    file_path: str,
    folder_id: Optional[str] = None,
    make_public: bool = True,
    producto_nombre: Optional[str] = None,
) -> str:
    print(f"[GDRIVE] Subiendo archivo: {file_path} | folder_id={folder_id}")
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

    service = _get_drive_service()

    # Resolver carpeta si se pasó un nombre en vez de ID
    resolved_folder_id = _resolve_folder_id(service, folder_id)
    print(f"[GDRIVE] Carpeta destino resuelta: {resolved_folder_id or 'root'}")

    # Generar nombre personalizado con patrón: NOMBREPRODUCTO_TIMESTAMP.EXTENSION
    mime_type = _guess_mime_type(file_path)
    extension = _get_extension_from_mime(mime_type)
    
    if producto_nombre:
        # Limpiar nombre del producto (remover caracteres especiales)
        clean_nombre = "".join(c for c in producto_nombre if c.isalnum() or c in (' ', '-', '_')).strip()
        clean_nombre = clean_nombre.replace(' ', '_').upper()
        timestamp = int(time.time())
        custom_filename = f"{clean_nombre}_{timestamp}{extension}"
    else:
        # Fallback al nombre original si no se proporciona nombre del producto
        custom_filename = os.path.basename(file_path)
    
    print(f"[GDRIVE] Nombre personalizado: {custom_filename}")

    file_metadata: dict[str, object] = {"name": custom_filename}
    if resolved_folder_id:
        file_metadata["parents"] = [resolved_folder_id]

    media = MediaFileUpload(file_path, mimetype=mime_type)
    # Si es un Shared Drive, usar supportsAllDrives
    supports_all_drives = len(resolved_folder_id) >= 10 if resolved_folder_id else False
    
    created = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id", supportsAllDrives=supports_all_drives)
        .execute()
    )
    file_id: str = created["id"]
    print(f"[GDRIVE] Archivo creado. file_id={file_id}")

    if make_public:
        try:
            # Intentar establecer permisos públicos con soporte para Shared Drives
            service.permissions().create(
                fileId=file_id,
                body={"role": "reader", "type": "anyone"},
                supportsAllDrives=supports_all_drives
            ).execute()
            print(f"[GDRIVE] Permisos públicos establecidos para file_id={file_id}")
        except Exception as e:
            print(f"[GDRIVE] Error estableciendo permisos públicos: {e}")
            print(f"[GDRIVE] El archivo se creó pero puede no ser público. file_id={file_id}")
            # Continuar sin fallar - el archivo existe pero puede no ser público

    # URL pública estable para visualizar/descargar
    public_url = f"https://drive.google.com/uc?id={file_id}"
    print(f"[GDRIVE] URL pública: {public_url}")
    return public_url


def _guess_mime_type(file_path: str) -> str:
    lower = file_path.lower()
    if lower.endswith(".png"):
        return "image/png"
    if lower.endswith(".jpg") or lower.endswith(".jpeg"):
        return "image/jpeg"
    if lower.endswith(".gif"):
        return "image/gif"
    if lower.endswith(".webp"):
        return "image/webp"
    if lower.endswith(".bmp"):
        return "image/bmp"
    return "image/jpeg"  # Default para imágenes


def _get_extension_from_mime(mime_type: str) -> str:
    """Convierte MIME type a extensión de archivo"""
    mime_to_ext = {
        "image/png": ".png",
        "image/jpeg": ".jpg",
        "image/gif": ".gif",
        "image/webp": ".webp",
        "image/bmp": ".bmp",
    }
    return mime_to_ext.get(mime_type, ".jpg")  # Default .jpg


