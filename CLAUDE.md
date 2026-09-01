# Garmin Activities

Programas en Python que consultan las últimas actividades de una cuenta de Garmin Connect vía la librería no oficial `garminconnect`, para uso personal: un script de terminal y un servidor MCP (local o remoto) que expone la misma consulta a Claude.

## Comandos

```bash
source venv/bin/activate         # activar entorno virtual
python garmin_activities.py      # ejecutar el script de terminal
python mcp_server.py             # servidor MCP en local (stdio)
MCP_TRANSPORT=http python mcp_server.py  # servidor MCP remoto (HTTP)
pip install -r requirements.txt  # instalar/actualizar dependencias
```

## Convenciones del proyecto

- Las credenciales viven en `.env` (nunca en el código ni en commits). `.env.example` documenta las claves esperadas.
- `requirements.txt` fija versiones exactas (`==`), no rangos, para reproducibilidad.
- El login a Garmin está centralizado en `garmin_client.py` (`get_client()`); tanto `garmin_activities.py` como `mcp_server.py` lo reutilizan en vez de duplicarlo.
- El login usa caché de tokens (por defecto en `~/.garminconnect`, configurable con `GARMIN_TOKENSTORE`) para evitar reautenticar con usuario/contraseña en cada ejecución y reducir rate limiting (errores 429) de Garmin. En Railway esto requiere un volumen persistente, ya que el filesystem es efímero.
- Errores de login/conexión se capturan explícitamente (`GarminConnectAuthenticationError`, `GarminConnectConnectionError`) y terminan el programa con `sys.exit(mensaje)` en vez de un traceback crudo.
- `mcp_server.py` arranca en modo `stdio` por defecto y en modo HTTP si `MCP_TRANSPORT=http`. En modo HTTP, el acceso está protegido con una clave compartida (`MCP_AUTH_TOKEN`), aceptada por cabecera `Authorization: Bearer` o por `?apiKey=` en la URL (para enlaces de instalación de un clic). No hay gestión de usuarios: es un servidor de un único usuario, pensado para uso personal.
- Despliegue en Railway: dos servicios independientes en el mismo proyecto — un *Cron Job* para `garmin_activities.py` (sin URL, `restartPolicyType: NEVER`) y un servicio web para `mcp_server.py` (con dominio público). Cada uno con su propio volumen montado para la caché de tokens.
