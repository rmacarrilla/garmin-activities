# Garmin Activities

Script Python que consulta las últimas actividades de una cuenta de Garmin Connect vía la librería no oficial `garminconnect`, para uso personal desde terminal.

## Comandos

```bash
source venv/bin/activate      # activar entorno virtual
python garmin_activities.py   # ejecutar el script
pip install -r requirements.txt  # instalar/actualizar dependencias
```

## Convenciones del proyecto

- Las credenciales viven en `.env` (nunca en el código ni en commits). `.env.example` documenta las claves esperadas.
- `requirements.txt` fija versiones exactas (`==`), no rangos, para reproducibilidad.
- El login usa caché de tokens en `~/.garminconnect` para evitar reautenticar con usuario/contraseña en cada ejecución y reducir rate limiting (errores 429) de Garmin.
- Errores de login/conexión se capturan explícitamente (`GarminConnectAuthenticationError`, `GarminConnectConnectionError`) y terminan el script con `sys.exit(mensaje)` en vez de un traceback crudo.
