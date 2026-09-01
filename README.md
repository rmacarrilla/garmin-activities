# Garmin Activities

Programas en Python para consultar tus últimas actividades de Garmin Connect, usando la librería no oficial [`garminconnect`](https://github.com/cyberjunky/python-garminconnect). Incluye:

- Un script de terminal (`garmin_activities.py`).
- Un servidor MCP (`mcp_server.py`) que expone la misma consulta como herramienta para Claude — en local (`stdio`) o desplegado como servicio remoto con URL pública (HTTP).

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

Copia la plantilla de variables de entorno y rellénala:

```bash
cp .env.example .env
```

Edita `.env`:

```
GARMIN_EMAIL=tu_correo@ejemplo.com
GARMIN_PASSWORD=tu_contraseña

# Solo necesaria si vas a exponer el servidor MCP por HTTP
MCP_AUTH_TOKEN=genera_un_valor_aleatorio
```

`.env` está en `.gitignore` y nunca se sube al repositorio.

En el primer login exitoso, la librería guarda un token de sesión (por defecto en `~/.garminconnect`, configurable con `GARMIN_TOKENSTORE`), que se reutiliza en ejecuciones posteriores para evitar volver a autenticar con usuario/contraseña cada vez y reducir el riesgo de rate limiting (429) de Garmin.

## Uso

### Script de terminal

```bash
source venv/bin/activate
python garmin_activities.py
```

Imprime las 5 actividades más recientes (fecha y nombre).

### Servidor MCP en local

```bash
claude mcp add garmin-activities -- "$(pwd)/venv/bin/python" "$(pwd)/mcp_server.py"
```

Registra el servidor en Claude Code (modo `stdio`). Expone una herramienta, `list_activities`, que Claude puede invocar directamente en el chat.

### Servidor MCP remoto (HTTP)

```bash
MCP_TRANSPORT=http python mcp_server.py
```

Arranca el mismo servidor escuchando en `PORT` (por defecto 8000) en vez de por `stdio`. Pensado para desplegarse como servicio siempre activo (p. ej. en Railway) con una URL pública.

El acceso está protegido con una clave compartida (`MCP_AUTH_TOKEN`), que el cliente debe enviar de una de estas dos formas:

- Cabecera `Authorization: Bearer <token>` (clientes MCP estándar).
- Parámetro `?apiKey=<token>` en la URL (para enlaces de instalación de un clic, que no permiten configurar cabeceras).

## Despliegue en Railway

El proyecto se despliega como dos servicios independientes dentro del mismo proyecto de Railway:

- **Cron diario** (`garmin_activities.py`): tipo *Cron Job*, sin URL, corre según una programación (`cronSchedule`) y termina — no se reinicia en bucle (`restartPolicyType: NEVER`).
- **Servidor MCP remoto** (`mcp_server.py`): servicio web normal con dominio público, `MCP_TRANSPORT=http`.

Ambos servicios necesitan un volumen persistente montado (p. ej. en `/data`) con `GARMIN_TOKENSTORE` apuntando a él — el filesystem de Railway es efímero, así que sin volumen cada ejecución reautenticaría con usuario/contraseña, aumentando el riesgo de bloqueo por rate limiting.

## Estructura del proyecto

```
.
├── garmin_activities.py   # script de terminal / cron
├── garmin_client.py       # login a Garmin compartido por ambos programas
├── mcp_server.py          # servidor MCP (local stdio / remoto HTTP)
├── requirements.txt       # dependencias con versiones fijadas
├── .env.example            # plantilla de variables de entorno
├── .env                    # credenciales reales (no versionado)
└── venv/                   # entorno virtual (no versionado)
```

## Licencia

Ver [LICENSE](LICENSE).
