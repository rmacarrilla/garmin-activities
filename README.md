# Garmin Activities

Script en Python para consultar tus últimas actividades de Garmin Connect desde la terminal, usando la librería no oficial [`garminconnect`](https://github.com/cyberjunky/python-garminconnect).

## Requisitos

- Python 3.10+
- Una cuenta de Garmin Connect

## Instalación

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuración

Copia la plantilla de variables de entorno y rellénala con tus credenciales:

```bash
cp .env.example .env
```

Edita `.env`:

```
GARMIN_EMAIL=tu_correo@ejemplo.com
GARMIN_PASSWORD=tu_contraseña
```

`.env` está en `.gitignore` y nunca se sube al repositorio.

## Uso

```bash
source venv/bin/activate
python garmin_activities.py
```

Imprime las 5 actividades más recientes (nombre y fecha de inicio) y el detalle completo en JSON de la más reciente.

En el primer login exitoso, la librería guarda un token de sesión en `~/.garminconnect`, que se reutiliza en ejecuciones posteriores para evitar volver a autenticar con usuario/contraseña cada vez.

## Estructura del proyecto

```
.
├── garmin_activities.py   # script principal
├── requirements.txt       # dependencias con versiones fijadas
├── .env.example            # plantilla de variables de entorno
├── .env                    # credenciales reales (no versionado)
└── venv/                   # entorno virtual (no versionado)
```

## Licencia

Ver [LICENSE](LICENSE).
