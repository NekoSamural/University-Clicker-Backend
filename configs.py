from pathlib import Path

ROOT_PATH = Path(__file__).parent
CLICK_REQUEST_TIME = 0.2

class AUTH_JWT_CONFIG:
    private_key_path = (ROOT_PATH / "assets" / "certs" / "jwt-private.pem").read_text()
    public_key_path = (ROOT_PATH / "assets" / "certs" / "jwt-public.pem").read_text()
    algorithm = "RS256"

class DATA_BASE_CONFIG:
    path = ROOT_PATH / "assets" / "database.db"