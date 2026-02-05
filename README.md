[url-shortener-guide-2 (1).md](https://github.com/user-attachments/files/25110473/url-shortener-guide-2.1.md)
# 🔗 Proyecto: URL Shortener

## Tu Misión DevOps

Vas a construir **desde cero** un acortador de URLs (tipo bit.ly) y desplegarlo en OpenShift con todo lo que has aprendido.

```
┌────────────────────────────────────────────────────────────────┐
│                                                                │
│    TU CONSTRUYES ESTO:                                         │
│                                                                │
│    Usuario                                                     │
│       │                                                        │
│       │  POST /shorten                                         │
│       │  {"url": "https://una-url-muy-larga.com/pagina"}       │
│       ▼                                                        │
│    ┌─────────────────┐      ┌─────────────────┐                │
│    │   URL Shortener │ ───▶ │   PostgreSQL    │                │
│    │   (Tu App)      │      │   (Base Datos)  │                │
│    └────────┬────────┘      └─────────────────┘                │
│             │                                                  │
│             │  Respuesta: https://tu-app.com/abc123            │
│             ▼                                                  │
│    Usuario visita /abc123 ──▶ Redirect a URL original          │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Lo que vas a practicar

| Componente | Skill |
|------------|-------|
| API Python (Flask) | Desarrollo |
| Dockerfile multi-stage | Containerización |
| Deployment, Service, Route | Kubernetes |
| ConfigMaps y Secrets | Configuración |
| PostgreSQL en OpenShift | Bases de datos |
| Helm Chart | Parametrización |
| GitHub Actions | CI/CD |
| CronJob | Tareas programadas |
| Tests | Calidad |
| Health checks | Observabilidad |

---

## 📋 Arquitectura Final

Cuando termines, tendrás esto funcionando:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            GITHUB                                       │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │                        Tu Repositorio                          │     │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │     │
│  │  │   app/   │ │   k8s/   │ │  helm/   │ │.github/  │          │     │
│  │  │          │ │          │ │          │ │workflows/│          │     │
│  │  │ app.py   │ │deploy.yml│ │Chart.yaml│ │  ci.yml  │          │     │
│  │  │Dockerfile│ │service.  │ │values-   │ │  cd.yml  │          │     │
│  │  │requirements│ │route... │ │ dev.yaml │ │          │          │     │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │     │
│  └────────────────────────────────────────────────────────────────┘     │
│                                    │                                    │
│                                    │ Push / PR                          │
│                                    ▼                                    │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │                     GitHub Actions                             │     │
│  │                                                                │     │
│  │   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐       │     │
│  │   │  Test   │──▶│  Build  │──▶│  Push   │──▶│ Deploy  │       │     │
│  │   │ pytest  │   │ Docker  │   │ ghcr.io │   │   oc    │       │     │
│  │   └─────────┘   └─────────┘   └─────────┘   └─────────┘       │     │
│  └────────────────────────────────────────────────────────────────┘     │
│                                    │                                    │
└────────────────────────────────────┼────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        OPENSHIFT SANDBOX                                │
│                                                                         │
│   Namespace: taylinn-dev                                                │
│   ┌─────────────────────────────────────────────────────────────┐       │
│   │                                                             │       │
│   │  ┌─────────────────┐         ┌─────────────────┐           │       │
│   │  │   Deployment    │         │   Deployment    │           │       │
│   │  │  url-shortener  │         │   postgresql    │           │       │
│   │  │                 │         │                 │           │       │
│   │  │  ┌───────────┐  │         │  ┌───────────┐  │           │       │
│   │  │  │    Pod    │  │────────▶│  │    Pod    │  │           │       │
│   │  │  │  app:5000 │  │         │  │  db:5432  │  │           │       │
│   │  │  └───────────┘  │         │  └───────────┘  │           │       │
│   │  └────────┬────────┘         └────────┬────────┘           │       │
│   │           │                           │                    │       │
│   │           ▼                           ▼                    │       │
│   │  ┌─────────────────┐         ┌─────────────────┐           │       │
│   │  │    Service      │         │    Service      │           │       │
│   │  │  ClusterIP:5000 │         │  ClusterIP:5432 │           │       │
│   │  └────────┬────────┘         └─────────────────┘           │       │
│   │           │                                                │       │
│   │           ▼                                                │       │
│   │  ┌─────────────────┐                                       │       │
│   │  │     Route       │                                       │       │
│   │  │ url-shortener-  │                                       │       │
│   │  │ taylinn-dev...  │                                       │       │
│   │  └────────┬────────┘                                       │       │
│   │           │                                                │       │
│   └───────────┼─────────────────────────────────────────────────┘       │
│               │                                                         │
└───────────────┼─────────────────────────────────────────────────────────┘
                │
                ▼
        🌐 https://url-shortener-taylinn-dev.apps.sandbox-xxx.openshiftapps.com
                │
                ▼
        👩‍💻 Taylinn prueba su app desde el navegador
```

---

## 📁 Estructura Final del Proyecto

```
url-shortener/
├── .github/
│   └── workflows/
│       ├── ci.yml              # Tests en cada PR
│       └── cd.yml              # Deploy a OpenShift
│
├── app/
│   ├── __init__.py
│   ├── app.py                  # API Flask
│   ├── models.py               # Modelos de BD
│   ├── config.py               # Configuración
│   └── utils.py                # Generador de códigos cortos
│
├── tests/
│   ├── __init__.py
│   ├── test_app.py             # Tests unitarios
│   └── test_integration.py     # Tests de integración
│
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── route.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   └── cronjob.yaml            # Limpieza de URLs expiradas
│
├── helm/
│   └── url-shortener/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── values-dev.yaml
│       ├── values-pro.yaml
│       └── templates/
│           ├── deployment.yaml
│           ├── service.yaml
│           ├── route.yaml
│           ├── configmap.yaml
│           ├── secret.yaml
│           └── cronjob.yaml
│
├── Dockerfile
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🗺️ Mapa de Fases

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   FASE 0          FASE 1         FASE 2         FASE 3         │
│   Setup           API            Tests          Docker          │
│   ┌─────┐        ┌─────┐        ┌─────┐        ┌─────┐         │
│   │ OCP │───────▶│Flask│───────▶│Pytest│──────▶│Image│         │
│   │ghcr │        │ App │        │     │        │     │         │
│   └─────┘        └─────┘        └─────┘        └─────┘         │
│                                                   │             │
│   ┌─────────────────────────────────────────────────┘             │
│   │                                                             │
│   ▼                                                             │
│   FASE 4         FASE 5         FASE 6         FASE 7          │
│   Kubernetes     CI/CD          Helm           Deploy          │
│   ┌─────┐        ┌─────┐        ┌─────┐        ┌─────┐         │
│   │ K8s │───────▶│ GH  │───────▶│Chart│───────▶│ 🚀  │         │
│   │YAML │        │Actions│       │     │        │LIVE!│         │
│   └─────┘        └─────┘        └─────┘        └─────┘         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

# 🚀 FASES DEL PROYECTO

---

## Fase 0: Setup del Entorno

### 🎯 Objetivo
Configurar todo lo necesario antes de empezar a desarrollar: Python, OpenShift CLI, y secrets en GitHub.

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   💡 NOTA IMPORTANTE                                        │
│                                                             │
│   NO necesitas Docker en tu máquina.                        │
│   GitHub Actions construye las imágenes por ti.             │
│                                                             │
│   Local: Python + SQLite (simple, sin instalaciones extra)  │
│   OpenShift: PostgreSQL (lo maneja el pipeline)             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 📝 Tareas

#### 0.1 Instalar Python

**Windows:**
1. Ve a [python.org/downloads](https://www.python.org/downloads/)
2. Descarga Python **3.11** o **3.12** (NO 3.14, es muy nueva)
3. Al instalar, **marca la casilla:**
   
   ☑️ **"Add python.exe to PATH"** ← MUY IMPORTANTE
   
4. Completa la instalación
5. Cierra y vuelve a abrir VS Code / Git Bash
6. Verifica:
   ```bash
   python --version
   # Python 3.11.x o 3.12.x
   ```

**Mac:**
```bash
brew install python@3.11
```

**Linux:**
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

#### 0.2 Crear cuenta en OpenShift Developer Sandbox

1. Ve a [https://developers.redhat.com/developer-sandbox](https://developers.redhat.com/developer-sandbox)

2. Haz clic en **"Start your sandbox for free"**

3. Crea una cuenta de Red Hat (o inicia sesión si ya tienes)

4. Verifica tu cuenta (te pedirán número de teléfono)

5. Una vez verificado, haz clic en **"Start using your sandbox"**

6. Se abrirá la consola de OpenShift. ¡Ya tienes tu cluster!

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   🎉 Tu sandbox incluye:                                    │
│                                                             │
│   • Namespace propio: <tu-usuario>-dev                      │
│   • CPU y memoria limitados (suficiente para este proyecto) │
│   • Duración: 30 días (renovable)                           │
│   • URL pública para tus aplicaciones                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 0.3 Instalar OpenShift CLI (oc)

**Windows:**
1. En la consola web de OpenShift, haz clic en **Help (?)** → **Command Line Tools**
2. Descarga el archivo para Windows
3. Extrae el zip
4. Mueve `oc.exe` a una carpeta en tu PATH (por ejemplo `C:\Windows\`)
5. O añade la carpeta donde lo extrajiste al PATH de Windows

**Mac:**
```bash
brew install openshift-cli
```

**Linux:**
```bash
wget https://mirror.openshift.com/pub/openshift-v4/clients/ocp/stable/openshift-client-linux.tar.gz
tar xvf openshift-client-linux.tar.gz
sudo mv oc /usr/local/bin/
```

**Verificar instalación:**
```bash
oc version
# Client Version: 4.x.x
```

#### 0.4 Obtener token y hacer login en OpenShift

1. En la consola web de OpenShift, haz clic en tu nombre (arriba a la derecha)

2. Selecciona **"Copy login command"**

3. Se abre una nueva pestaña → Haz clic en **"Display Token"**

4. Copia el comando completo que aparece:

```bash
oc login --token=sha256~XXXXXXXXXXXXXXXXXXXXXXXXX --server=https://api.sandbox-xxx.openshiftapps.com:6443
```

5. Pégalo en tu terminal y ejecútalo

6. Verifica que estás conectado:
```bash
oc whoami
# tu-usuario

oc project
# Using project "tu-usuario-dev"
```

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   ⚠️  IMPORTANTE: El token expira cada 24 horas             │
│                                                             │
│   Si ves errores de autenticación, repite el paso 0.4      │
│   para obtener un nuevo token.                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 0.5 Configurar Secrets en GitHub Actions

Para que el pipeline pueda hacer deploy a OpenShift, necesita secrets.

**Paso 1: Ir a los secrets del repositorio**

1. Ve a tu repositorio en GitHub
2. Settings → Secrets and variables → Actions
3. Haz clic en **"New repository secret"**

**Paso 2: Añadir los secrets necesarios**

| Secret Name | Valor | Cómo obtenerlo |
|-------------|-------|----------------|
| `OPENSHIFT_SERVER` | `https://api.sandbox-xxx.openshiftapps.com:6443` | Del comando de login (paso 0.4) |
| `OPENSHIFT_TOKEN` | `sha256~XXXXXXX...` | Del comando de login (paso 0.4) |

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   📝 NOTA: GITHUB_TOKEN ya existe automáticamente           │
│                                                             │
│   GitHub Actions tiene acceso a ghcr.io usando el token     │
│   automático ${{ secrets.GITHUB_TOKEN }}                    │
│                                                             │
│   No necesitas crear ningún token adicional para ghcr.io    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 0.6 Instalar Helm

**Windows:**
1. Descarga desde [github.com/helm/helm/releases](https://github.com/helm/helm/releases)
2. Extrae el zip
3. Mueve `helm.exe` al mismo lugar donde pusiste `oc.exe`

**Mac:**
```bash
brew install helm
```

**Linux:**
```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

**Verificar:**
```bash
helm version
```

### ✅ Checkpoint de Validación

<details>
<summary>🔍 ¿Cómo sé que lo hice bien?</summary>

Ejecuta estos comandos y verifica que todos funcionan:

```bash
# 1. Python instalado
python --version
# ✅ Debe mostrar Python 3.11.x o 3.12.x

# 2. Pip funciona
python -m pip --version
# ✅ Debe mostrar la versión de pip

# 3. OpenShift CLI instalado
oc version
# ✅ Debe mostrar la versión del cliente

# 4. Conectado a OpenShift
oc whoami
# ✅ Debe mostrar tu usuario

# 5. Tienes un proyecto/namespace
oc project
# ✅ Debe mostrar "tu-usuario-dev"

# 6. Helm instalado
helm version
# ✅ Debe mostrar la versión

# 7. Secrets configurados en GitHub
# Ve a tu repo → Settings → Secrets → Actions
# ✅ Debes ver OPENSHIFT_SERVER y OPENSHIFT_TOKEN
```

**Si todo funciona, ¡estás lista para empezar!** 🚀

</details>

<details>
<summary>💡 Hint: El comando python no funciona</summary>

En Windows, prueba con:
```bash
py --version
```

Si `py` funciona pero `python` no, puedes usar `py` en todos los comandos:
```bash
py -m pip install -r requirements.txt
py -m pytest tests/ -v
py -m app.app
```

</details>

<details>
<summary>💡 Hint: Error "token expired" en OpenShift</summary>

El token del Sandbox expira cada 24 horas. Para renovarlo:

1. Ve a la consola web de OpenShift
2. Haz clic en tu nombre → "Copy login command"
3. Display Token
4. Copia y ejecuta el nuevo comando `oc login`
5. **Actualiza el secret en GitHub** con el nuevo token

</details>

---

## Fase 1: Setup del Proyecto y API Local

### 🎯 Objetivo
Crear la API de Flask funcionando en tu máquina local.

### 📝 Tareas

#### 1.1 Crea el repositorio
- Crea un nuevo repo en GitHub llamado `url-shortener`
- Clónalo en tu máquina
- Crea la estructura de carpetas inicial

#### 1.2 Crea el archivo `requirements.txt`

```txt
flask==3.0.0
flask-sqlalchemy==3.1.1
psycopg2-binary==2.9.9
python-dotenv==1.0.0
gunicorn==21.2.0
pytest==7.4.3
pytest-flask==1.3.0
```

> 💡 **Nota:** `psycopg2-binary` es para PostgreSQL en OpenShift. Si te da error al instalarlo localmente, puedes ignorarlo (local usa SQLite).

#### 1.2b Crea el archivo `.gitignore`

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/

# SQLite (base de datos local)
*.db
urlshortener.db

# IDE
.idea/
.vscode/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# OS
.DS_Store
Thumbs.db
```

#### 1.3 Crea `app/config.py`

```python
import os

class Config:
    # Local: SQLite (sin instalaciones extra)
    # OpenShift: PostgreSQL (configurado por variable de entorno)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///urlshortener.db'  # Base de datos local en un archivo
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')
```

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   💡 ¿Por qué SQLite local y PostgreSQL en OpenShift?       │
│                                                             │
│   • SQLite: Un simple archivo, no necesita instalar nada    │
│   • PostgreSQL: Base de datos "de verdad" para producción   │
│                                                             │
│   El código es el mismo, solo cambia la URL de conexión.    │
│   En OpenShift, la variable DATABASE_URL apunta a Postgres. │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 1.4 Crea `app/models.py`

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()

class URL(db.Model):
    __tablename__ = 'urls'
    
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(days=30))
    clicks = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'original_url': self.original_url,
            'short_code': self.short_code,
            'short_url': f"{self.short_url}",
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat(),
            'clicks': self.clicks
        }
    
    @property
    def short_url(self):
        from flask import current_app
        base_url = current_app.config.get('BASE_URL', 'http://localhost:5000')
        return f"{base_url}/{self.short_code}"
```

#### 1.5 Crea `app/utils.py`

```python
import string
import random

def generate_short_code(length=6):
    """Genera un código corto aleatorio."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
```

#### 1.6 Crea `app/app.py`

```python
from flask import Flask, request, jsonify, redirect
from app.models import db, URL
from app.utils import generate_short_code
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    # Health check endpoints
    @app.route('/health/live', methods=['GET'])
    def liveness():
        return jsonify({'status': 'alive'}), 200
    
    @app.route('/health/ready', methods=['GET'])
    def readiness():
        try:
            db.session.execute(db.text('SELECT 1'))
            return jsonify({'status': 'ready'}), 200
        except Exception as e:
            return jsonify({'status': 'not ready', 'error': str(e)}), 503
    
    # API endpoints
    @app.route('/shorten', methods=['POST'])
    def shorten_url():
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        original_url = data['url']
        
        # Validación básica de URL
        if not original_url.startswith(('http://', 'https://')):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        # Generar código único
        short_code = generate_short_code()
        while URL.query.filter_by(short_code=short_code).first():
            short_code = generate_short_code()
        
        # Crear registro
        url_entry = URL(original_url=original_url, short_code=short_code)
        db.session.add(url_entry)
        db.session.commit()
        
        return jsonify(url_entry.to_dict()), 201
    
    @app.route('/<short_code>', methods=['GET'])
    def redirect_to_url(short_code):
        url_entry = URL.query.filter_by(short_code=short_code).first()
        
        if not url_entry:
            return jsonify({'error': 'URL not found'}), 404
        
        # Incrementar contador de clicks
        url_entry.clicks += 1
        db.session.commit()
        
        return redirect(url_entry.original_url, code=302)
    
    @app.route('/stats/<short_code>', methods=['GET'])
    def get_stats(short_code):
        url_entry = URL.query.filter_by(short_code=short_code).first()
        
        if not url_entry:
            return jsonify({'error': 'URL not found'}), 404
        
        return jsonify(url_entry.to_dict()), 200
    
    @app.route('/urls', methods=['GET'])
    def list_urls():
        urls = URL.query.order_by(URL.created_at.desc()).limit(100).all()
        return jsonify([url.to_dict() for url in urls]), 200
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

#### 1.7 Crea `app/__init__.py`

```python
from app.app import create_app, app
from app.models import db, URL

__all__ = ['create_app', 'app', 'db', 'URL']
```

### ✅ Checkpoint de Validación

<details>
<summary>🔍 ¿Cómo sé que lo hice bien?</summary>

1. **Instala dependencias:**
   ```bash
   python -m pip install -r requirements.txt
   ```

   > ⚠️ Si da error con `psycopg2-binary`, créate un `requirements-dev.txt` sin esa línea:
   > ```txt
   > flask==3.0.0
   > flask-sqlalchemy==3.1.1
   > python-dotenv==1.0.0
   > gunicorn==21.2.0
   > pytest==7.4.3
   > pytest-flask==1.3.0
   > ```
   > Y ejecuta: `python -m pip install -r requirements-dev.txt`

2. **Ejecuta la app:**
   ```bash
   python -m app.app
   ```
   
   Deberías ver:
   ```
   * Running on http://127.0.0.1:5000
   ```

3. **Prueba los endpoints** (en otra terminal):
   ```bash
   # Crear URL corta
   curl -X POST http://localhost:5000/shorten \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.google.com"}'
   
   # Respuesta esperada:
   # {"id": 1, "original_url": "https://www.google.com", "short_code": "abc123", ...}
   
   # Health check
   curl http://localhost:5000/health/live
   # {"status": "alive"}
   
   curl http://localhost:5000/health/ready
   # {"status": "ready"}
   ```

4. **Abre en el navegador:** `http://localhost:5000/abc123` → Debe redirigir a Google

5. **Verifica que se creó la base de datos:**
   ```bash
   ls -la
   # Deberías ver: urlshortener.db (archivo SQLite)
   ```

</details>

<details>
<summary>💡 Hint: curl no funciona en Windows</summary>

En Git Bash, `curl` debería funcionar. Si no:

**Opción 1:** Usa PowerShell:
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/health/live" -Method GET
```

**Opción 2:** Usa el navegador o Postman para probar los endpoints.

**Opción 3:** Instala curl con Git for Windows (ya viene incluido normalmente).

</details>

<details>
<summary>💡 Hint: Error "Address already in use"</summary>

El puerto 5000 está ocupado. Opciones:

1. Mata el proceso que lo usa:
   ```bash
   # Windows
   netstat -ano | findstr :5000
   taskkill /PID <numero> /F
   
   # Mac/Linux
   lsof -i :5000
   kill -9 <PID>
   ```

2. O cambia el puerto en `app.py`:
   ```python
   app.run(host='0.0.0.0', port=5001, debug=True)
   ```

</details>

### 🧩 Retos de la Fase 1

Antes de pasar a la siguiente fase, completa estos retos:

<details>
<summary>🎯 Reto 1.1: Añadir validación de URL duplicada</summary>

**Problema:** Ahora mismo, si alguien acorta la misma URL dos veces, se crean dos registros diferentes.

**Tu tarea:** Modifica el endpoint `/shorten` para que:
- Si la URL ya existe en la base de datos, devuelva el short_code existente
- Solo cree un nuevo registro si la URL es nueva

**Pista:** Usa `URL.query.filter_by(original_url=...).first()`

**¿Cómo sé que lo hice bien?**
```bash
# Primera llamada
curl -X POST http://localhost:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
# Devuelve: {"short_code": "abc123", ...}

# Segunda llamada (misma URL)
curl -X POST http://localhost:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
# Debe devolver EL MISMO short_code: {"short_code": "abc123", ...}
```
</details>

<details>
<summary>🎯 Reto 1.2: Crear endpoint DELETE</summary>

**Problema:** No hay forma de eliminar una URL acortada.

**Tu tarea:** Crea un nuevo endpoint `DELETE /urls/<short_code>` que:
- Elimine la URL de la base de datos
- Devuelva 204 (No Content) si se eliminó correctamente
- Devuelva 404 si el short_code no existe

**¿Cómo sé que lo hice bien?**
```bash
# Crear una URL
curl -X POST http://localhost:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com"}'

# Eliminarla
curl -X DELETE http://localhost:5000/urls/abc123
# Status: 204

# Intentar eliminar de nuevo
curl -X DELETE http://localhost:5000/urls/abc123
# Status: 404
```
</details>

<details>
<summary>🎯 Reto 1.3: Personalizar el short_code</summary>

**Problema:** Los usuarios quieren poder elegir su propio código corto (ej: `miempresa` en vez de `x7Kp2m`).

**Tu tarea:** Modifica el endpoint `/shorten` para que:
- Acepte un campo opcional `custom_code` en el JSON
- Si se proporciona, use ese código (validando que no exista ya)
- Si no se proporciona, genere uno aleatorio como antes
- Valida que el custom_code solo tenga letras, números y guiones
- Máximo 20 caracteres

**¿Cómo sé que lo hice bien?**
```bash
# Con código personalizado
curl -X POST http://localhost:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com", "custom_code": "mi-link"}'
# Devuelve: {"short_code": "mi-link", ...}

# Código ya existe
curl -X POST http://localhost:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com", "custom_code": "mi-link"}'
# Devuelve: 409 Conflict {"error": "Custom code already exists"}

# Código inválido
curl -X POST http://localhost:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com", "custom_code": "código con espacios!"}'
# Devuelve: 400 Bad Request
```
</details>

---

## Fase 2: Tests

### 🎯 Objetivo
Crear tests para asegurar que tu API funciona correctamente.

### 📝 Tareas

#### 2.1 Crea `tests/__init__.py`
```python
# Empty file
```

#### 2.2 Crea `tests/conftest.py`

```python
import pytest
from app.app import create_app
from app.models import db

class TestConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    BASE_URL = 'http://localhost:5000'

@pytest.fixture
def app():
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
```

#### 2.3 Crea `tests/test_app.py`

```python
import json

def test_health_live(client):
    """Test liveness endpoint."""
    response = client.get('/health/live')
    assert response.status_code == 200
    assert response.json['status'] == 'alive'

def test_health_ready(client):
    """Test readiness endpoint."""
    response = client.get('/health/ready')
    assert response.status_code == 200
    assert response.json['status'] == 'ready'

def test_shorten_url_success(client):
    """Test creating a short URL."""
    response = client.post('/shorten',
        data=json.dumps({'url': 'https://www.example.com'}),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = response.json
    assert 'short_code' in data
    assert data['original_url'] == 'https://www.example.com'
    assert len(data['short_code']) == 6

def test_shorten_url_missing_url(client):
    """Test error when URL is missing."""
    response = client.post('/shorten',
        data=json.dumps({}),
        content_type='application/json'
    )
    assert response.status_code == 400
    assert 'error' in response.json

def test_shorten_url_invalid_format(client):
    """Test error when URL format is invalid."""
    response = client.post('/shorten',
        data=json.dumps({'url': 'not-a-valid-url'}),
        content_type='application/json'
    )
    assert response.status_code == 400

def test_redirect_success(client):
    """Test redirect to original URL."""
    # First create a short URL
    create_response = client.post('/shorten',
        data=json.dumps({'url': 'https://www.example.com'}),
        content_type='application/json'
    )
    short_code = create_response.json['short_code']
    
    # Then try to access it
    redirect_response = client.get(f'/{short_code}')
    assert redirect_response.status_code == 302
    assert redirect_response.location == 'https://www.example.com'

def test_redirect_not_found(client):
    """Test 404 for non-existent short code."""
    response = client.get('/nonexistent')
    assert response.status_code == 404

def test_stats_endpoint(client):
    """Test getting stats for a URL."""
    # Create a short URL
    create_response = client.post('/shorten',
        data=json.dumps({'url': 'https://www.example.com'}),
        content_type='application/json'
    )
    short_code = create_response.json['short_code']
    
    # Access it once
    client.get(f'/{short_code}')
    
    # Check stats
    stats_response = client.get(f'/stats/{short_code}')
    assert stats_response.status_code == 200
    assert stats_response.json['clicks'] == 1

def test_list_urls(client):
    """Test listing all URLs."""
    # Create some URLs
    client.post('/shorten',
        data=json.dumps({'url': 'https://www.example1.com'}),
        content_type='application/json'
    )
    client.post('/shorten',
        data=json.dumps({'url': 'https://www.example2.com'}),
        content_type='application/json'
    )
    
    # List all
    response = client.get('/urls')
    assert response.status_code == 200
    assert len(response.json) == 2
```

### ✅ Checkpoint de Validación

<details>
<summary>🔍 ¿Cómo sé que lo hice bien?</summary>

```bash
# Ejecuta los tests
pytest tests/ -v

# Deberías ver algo así:
# tests/test_app.py::test_health_live PASSED
# tests/test_app.py::test_health_ready PASSED
# tests/test_app.py::test_shorten_url_success PASSED
# ... todos los tests en verde
```

</details>

### 🧩 Retos de la Fase 2

<details>
<summary>🎯 Reto 2.1: Tests para tus nuevas funcionalidades</summary>

**Problema:** Añadiste funcionalidades en la Fase 1 (retos 1.1, 1.2, 1.3) pero no tienen tests.

**Tu tarea:** Escribe tests para:
- El comportamiento de URL duplicada (Reto 1.1)
- El endpoint DELETE (Reto 1.2)
- El custom_code (Reto 1.3)

**Mínimo 5 tests nuevos.**

**Pista:** Piensa en casos edge:
- ¿Qué pasa si el custom_code tiene 21 caracteres?
- ¿Qué pasa si intento borrar algo que no existe?
</details>

<details>
<summary>🎯 Reto 2.2: Test de expiración</summary>

**Problema:** Las URLs expiran a los 30 días, pero no hay test que lo verifique.

**Tu tarea:** Escribe un test que:
1. Cree una URL con fecha de expiración en el pasado (manipulando el modelo)
2. Verifique que el redirect devuelve 404 o un mensaje de "URL expirada"

**Pista:** Tendrás que modificar también el código de la app para que verifique la expiración antes de redirigir.

**Doble reto:** Haz que devuelva un error específico 410 (Gone) para URLs expiradas, diferente del 404 (Not Found).
</details>

<details>
<summary>🎯 Reto 2.3: Medir cobertura de tests</summary>

**Problema:** No sabes qué porcentaje de tu código está cubierto por tests.

**Tu tarea:**
1. Instala `pytest-cov`: añádelo a requirements.txt
2. Ejecuta los tests con cobertura: `pytest --cov=app tests/`
3. Consigue al menos **80% de cobertura**

**¿Cómo sé que lo hice bien?**
```bash
pytest --cov=app --cov-report=term-missing tests/

# Deberías ver algo así:
# Name             Stmts   Miss  Cover   Missing
# ----------------------------------------------
# app/app.py          45      5    89%   23, 45-48
# app/models.py       20      2    90%   18-19
# ...
# TOTAL              100     10    90%
```
</details>

---

## Fase 3: Dockerización

### 🎯 Objetivo
Crear un Dockerfile para que GitHub Actions pueda construir la imagen y desplegarla en OpenShift.

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   💡 NO necesitas Docker en tu máquina                      │
│                                                             │
│   Solo creas el Dockerfile. GitHub Actions:                 │
│   1. Lee tu Dockerfile                                      │
│   2. Construye la imagen                                    │
│   3. La sube a ghcr.io                                      │
│   4. La despliega en OpenShift                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 📝 Tareas

#### 3.1 Crea el `Dockerfile`

```dockerfile
# ============================================
# Stage 1: Builder
# ============================================
FROM python:3.11-slim as builder

WORKDIR /app

# Instalar dependencias de compilación
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ============================================
# Stage 2: Runtime
# ============================================
FROM python:3.11-slim as runtime

WORKDIR /app

# Instalar solo runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /bin/bash appuser

# Copiar dependencias instaladas del builder
COPY --from=builder /root/.local /home/appuser/.local

# Copiar código de la aplicación
COPY --chown=appuser:appuser app/ ./app/

# Configurar entorno
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Cambiar a usuario no-root
USER appuser

# Puerto
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health/live')" || exit 1

# Comando de inicio
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app.app:app"]
```

> 📝 **Nota:** Este Dockerfile usa `python:3.11-slim` (no 3.14) para evitar problemas de compatibilidad.

#### 3.2 Crea el `.dockerignore`

```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
.git
.gitignore
.dockerignore
Dockerfile
*.md
tests/
.pytest_cache/
.coverage
htmlcov/
k8s/
helm/
.github/
*.db
urlshortener.db
```

### ✅ Checkpoint de Validación

<details>
<summary>🔍 ¿Cómo sé que lo hice bien?</summary>

Como no tienes Docker local, la validación es más simple:

1. **Verifica que los archivos existen:**
   ```bash
   ls -la Dockerfile .dockerignore
   # Deben aparecer ambos archivos
   ```

2. **Verifica la sintaxis del Dockerfile:**
   - Abre el Dockerfile en VS Code
   - Si tienes la extensión de Docker, te marcará errores de sintaxis
   - Si no hay errores, ¡está bien!

3. **La prueba real será en la Fase 5:**
   - Cuando configures GitHub Actions, el pipeline construirá la imagen
   - Si hay errores en el Dockerfile, el pipeline fallará y te dirá qué arreglar

</details>

### 🧩 Retos de la Fase 3

<details>
<summary>🎯 Reto 3.1: Entender el Dockerfile multi-stage</summary>

**Problema:** Tienes un Dockerfile pero no entiendes por qué está estructurado así.

**Tu tarea:** Responde estas preguntas (investiga si es necesario):

1. ¿Por qué hay dos `FROM` en el Dockerfile? ¿Qué ventaja tiene?
2. ¿Por qué instalamos `gcc` y `libpq-dev` en el builder pero no en runtime?
3. ¿Qué hace el comando `COPY --from=builder`?
4. ¿Por qué creamos un usuario `appuser` en vez de usar root?
5. ¿Para qué sirve el `HEALTHCHECK`?

**Bonus:** ¿Cuánto más pesaría la imagen si no usáramos multi-stage? (pista: el builder tiene compiladores)

**¿Cómo sé que lo hice bien?** Escribe tus respuestas en un archivo `DOCKERFILE-EXPLICADO.md` en tu repo.
</details>

<details>
<summary>🎯 Reto 3.2: Añadir labels al Dockerfile</summary>

**Problema:** Tu imagen no tiene metadatos que indiquen quién la creó, versión, etc.

**Tu tarea:** Añade estos labels al Dockerfile:
- `org.opencontainers.image.title`
- `org.opencontainers.image.description`
- `org.opencontainers.image.version`
- `org.opencontainers.image.authors`
- `org.opencontainers.image.source` (URL del repo)

**Pista:** Usa `LABEL` en el Dockerfile después del segundo `FROM`:
```dockerfile
FROM python:3.11-slim as runtime

LABEL org.opencontainers.image.title="URL Shortener"
LABEL org.opencontainers.image.description="A simple URL shortener API"
# ... añade los demás
```

**¿Cómo sé que lo hice bien?** Cuando el pipeline corra, podrás ver los labels en GitHub Packages.
</details>

<details>
<summary>🎯 Reto 3.3: Investigar sobre seguridad en contenedores</summary>

**Problema:** No sabes qué vulnerabilidades podría tener tu imagen.

**Tu tarea:**
1. Investiga qué es **Trivy** y para qué sirve
2. Investiga qué son las vulnerabilidades **CVE**
3. Mira el Dockerfile: ¿qué medidas de seguridad ya tiene?
   - Pista: busca `USER`, `--no-cache-dir`, imagen `slim`
4. Cuando llegues a la Fase 5, añadirás Trivy al pipeline

**Escribe tus hallazgos en un archivo `SEGURIDAD.md`**

Preguntas a responder:
- ¿Qué es un CVE?
- ¿Por qué es malo correr como root en un contenedor?
- ¿Qué hace `--no-cache-dir` en pip y por qué es buena práctica?
</details>

---

## Fase 4: Manifiestos de Kubernetes

### 🎯 Objetivo
Crear los manifiestos de Kubernetes para desplegar tu aplicación.

### 📝 Tareas

#### 4.1 Crea `k8s/namespace.yaml` (opcional, OpenShift ya te da uno)

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: url-shortener
```

#### 4.2 Crea `k8s/configmap.yaml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: url-shortener-config
  labels:
    app: url-shortener
data:
  BASE_URL: "https://url-shortener-<TU-NAMESPACE>.apps.sandbox-xxx.openshiftapps.com"
```

#### 4.3 Crea `k8s/secret.yaml`

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: url-shortener-secret
  labels:
    app: url-shortener
type: Opaque
stringData:
  DATABASE_URL: "postgresql://urlshortener:password123@postgresql:5432/urlshortener"
```

> ⚠️ **IMPORTANTE:** Este secret es para desarrollo. En producción usarás Sealed Secrets o External Secrets.

#### 4.4 Crea `k8s/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: url-shortener
  labels:
    app: url-shortener
spec:
  replicas: 2
  selector:
    matchLabels:
      app: url-shortener
  template:
    metadata:
      labels:
        app: url-shortener
    spec:
      containers:
        - name: url-shortener
          image: ghcr.io/<TU-USUARIO>/url-shortener:latest
          ports:
            - containerPort: 5000
              protocol: TCP
          envFrom:
            - configMapRef:
                name: url-shortener-config
            - secretRef:
                name: url-shortener-secret
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health/live
              port: 5000
            initialDelaySeconds: 10
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 5000
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 3
```

#### 4.5 Crea `k8s/service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: url-shortener
  labels:
    app: url-shortener
spec:
  type: ClusterIP
  ports:
    - port: 5000
      targetPort: 5000
      protocol: TCP
      name: http
  selector:
    app: url-shortener
```

#### 4.6 Crea `k8s/route.yaml` (OpenShift)

```yaml
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: url-shortener
  labels:
    app: url-shortener
spec:
  to:
    kind: Service
    name: url-shortener
    weight: 100
  port:
    targetPort: http
  tls:
    termination: edge
    insecureEdgeTerminationPolicy: Redirect
  wildcardPolicy: None
```

#### 4.7 Crea `k8s/postgresql.yaml`

```yaml
---
apiVersion: v1
kind: Secret
metadata:
  name: postgresql-secret
  labels:
    app: postgresql
type: Opaque
stringData:
  POSTGRES_USER: urlshortener
  POSTGRES_PASSWORD: password123
  POSTGRES_DB: urlshortener

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgresql-pvc
  labels:
    app: postgresql
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgresql
  labels:
    app: postgresql
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgresql
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: postgresql
    spec:
      containers:
        - name: postgresql
          image: postgres:15-alpine
          ports:
            - containerPort: 5432
          envFrom:
            - secretRef:
                name: postgresql-secret
          volumeMounts:
            - name: postgresql-data
              mountPath: /var/lib/postgresql/data
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "500m"
          livenessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - urlshortener
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            exec:
              command:
                - pg_isready
                - -U
                - urlshortener
            initialDelaySeconds: 5
            periodSeconds: 5
      volumes:
        - name: postgresql-data
          persistentVolumeClaim:
            claimName: postgresql-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: postgresql
  labels:
    app: postgresql
spec:
  type: ClusterIP
  ports:
    - port: 5432
      targetPort: 5432
  selector:
    app: postgresql
```

#### 4.8 Crea `k8s/cronjob.yaml`

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: url-shortener-cleanup
  labels:
    app: url-shortener
spec:
  schedule: "0 2 * * *"  # Todos los días a las 2:00 AM
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 3
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: cleanup
              image: postgres:15-alpine
              command:
                - /bin/sh
                - -c
                - |
                  psql $DATABASE_URL -c "DELETE FROM urls WHERE expires_at < NOW();"
                  echo "Cleanup completed at $(date)"
              envFrom:
                - secretRef:
                    name: url-shortener-secret
          restartPolicy: OnFailure
```

### ✅ Checkpoint de Validación

<details>
<summary>🔍 ¿Cómo sé que lo hice bien?</summary>

```bash
# Login a OpenShift
oc login --token=<tu-token> --server=<tu-server>

# Despliega PostgreSQL primero
oc apply -f k8s/postgresql.yaml

# Espera a que esté ready
oc get pods -w
# Espera hasta ver: postgresql-xxx   1/1   Running

# Despliega la app (primero necesitas la imagen, lo veremos en la siguiente fase)
oc apply -f k8s/configmap.yaml
oc apply -f k8s/secret.yaml
oc apply -f k8s/deployment.yaml
oc apply -f k8s/service.yaml
oc apply -f k8s/route.yaml
oc apply -f k8s/cronjob.yaml

# Verifica
oc get pods
oc get routes
oc get cronjobs
```

</details>

<details>
<summary>💡 Hint: Los pods no arrancan</summary>

Revisa los logs:
```bash
oc logs -f deployment/url-shortener
oc describe pod <nombre-del-pod>
```

Errores comunes:
- **ImagePullBackOff:** La imagen no existe o no tienes permisos
- **CrashLoopBackOff:** Error en la aplicación, revisa los logs
- **Pending:** No hay recursos, verifica con `oc describe pod`

</details>

### 🧩 Retos de la Fase 4

<details>
<summary>🎯 Reto 4.1: Debugging - Arregla este Deployment</summary>

**Problema:** El siguiente Deployment tiene **5 errores**. Encuéntralos y corrígelos.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: url-shortener
spec:
  replicas: "2"
  selector:
    matchLabels:
      app: shortener
  template:
    metadata:
      labels:
        app: url-shortener
    spec:
      containers:
        - name: url-shortener
          image: ghcr.io/usuario/url-shortener
          ports:
            - containerPort: "5000"
          resources:
            requests:
              memory: 128Mi
              cpu: 100m
            limits:
              memory: 64Mi
              cpu: 50m
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 10
```

**Pistas:**
- Revisa los tipos de datos (¿strings donde deberían ser integers?)
- Revisa que los labels coincidan
- Revisa los recursos (¿tiene sentido lo que pone?)
- Revisa los probes (¿coinciden con tu app?)

**¿Cómo sé que lo hice bien?** El deployment debe crearse sin errores y los pods deben arrancar.
</details>

<details>
<summary>🎯 Reto 4.2: Añadir Horizontal Pod Autoscaler</summary>

**Problema:** Si hay mucho tráfico, 2 réplicas no son suficientes.

**Tu tarea:** Crea un archivo `k8s/hpa.yaml` que:
- Escale automáticamente entre 2 y 10 réplicas
- Escale cuando el CPU supere el 70%
- Escale cuando la memoria supere el 80%

**Pista:** Busca "HorizontalPodAutoscaler v2" en la documentación de Kubernetes.

**¿Cómo sé que lo hice bien?**
```bash
oc apply -f k8s/hpa.yaml
oc get hpa

# NAME            REFERENCE                  TARGETS   MINPODS   MAXPODS   REPLICAS
# url-shortener   Deployment/url-shortener   10%/70%   2         10        2
```
</details>

<details>
<summary>🎯 Reto 4.3: Configurar NetworkPolicy</summary>

**Problema:** Cualquier pod del cluster puede conectarse a tu base de datos.

**Tu tarea:** Crea un archivo `k8s/networkpolicy.yaml` que:
- Solo permita conexiones a PostgreSQL desde pods con label `app: url-shortener`
- Bloquee cualquier otra conexión entrante a PostgreSQL

**Pista:** 
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: postgresql-policy
spec:
  podSelector:
    matchLabels:
      app: postgresql
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              # ¿Qué label va aquí?
      ports:
        - port: 5432
```

**¿Cómo sé que lo hice bien?**
```bash
# Desde un pod url-shortener, debe funcionar:
oc exec -it deployment/url-shortener -- nc -zv postgresql 5432
# Connection succeeded

# Desde otro pod cualquiera, debe fallar (timeout):
oc run test-pod --image=busybox --rm -it -- nc -zv postgresql 5432
# Connection timed out
```
</details>

<details>
<summary>🎯 Reto 4.4: El CronJob no funciona - ¿Por qué?</summary>

**Problema:** Desplegaste el CronJob pero nunca limpia las URLs expiradas.

**Diagnóstico:** Ejecuta estos comandos y analiza:
```bash
# Ver estado del cronjob
oc get cronjobs

# Ver jobs ejecutados
oc get jobs

# Ver logs del último job
oc logs job/<nombre-del-job>
```

**Tu tarea:** 
1. Encuentra por qué falla (puede haber varias razones)
2. Corrígelo
3. Ejecuta el job manualmente para probar: `oc create job --from=cronjob/url-shortener-cleanup test-cleanup`

**Posibles problemas a investigar:**
- ¿El secret tiene el nombre correcto?
- ¿La tabla `urls` existe?
- ¿El campo se llama `expires_at` o `expiration_date`?
</details>

---

## Fase 5: GitHub Actions CI/CD

### 🎯 Objetivo
Automatizar el build, test y deploy con GitHub Actions.

### 📝 Tareas

#### 5.1 Crea `.github/workflows/ci.yml`

```yaml
name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: urlshortener_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/urlshortener_test
        run: pytest tests/ -v --tb=short
      
      - name: Run linter
        run: |
          pip install flake8
          flake8 app/ --max-line-length=120 --ignore=E501

  build:
    runs-on: ubuntu-latest
    needs: test
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    permissions:
      contents: read
      packages: write
    
    outputs:
      image_tag: ${{ steps.meta.outputs.tags }}
      image_digest: ${{ steps.build.outputs.digest }}
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=
            type=raw,value=latest
      
      - name: Build and push
        id: build
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

#### 5.2 Crea `.github/workflows/cd.yml`

```yaml
name: CD

on:
  workflow_run:
    workflows: [CI]
    types: [completed]
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  deploy:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Install OpenShift CLI
        uses: redhat-actions/oc-installer@v1
        with:
          oc_version: '4.12'
      
      - name: Login to OpenShift
        run: |
          oc login --token=${{ secrets.OPENSHIFT_TOKEN }} --server=${{ secrets.OPENSHIFT_SERVER }}
      
      - name: Set image tag
        run: |
          echo "IMAGE_TAG=$(git rev-parse --short HEAD)" >> $GITHUB_ENV
      
      - name: Deploy to OpenShift
        run: |
          # Actualizar imagen en deployment
          oc set image deployment/url-shortener \
            url-shortener=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ env.IMAGE_TAG }} \
            --record
          
          # Esperar a que el rollout termine
          oc rollout status deployment/url-shortener --timeout=300s
      
      - name: Verify deployment
        run: |
          # Obtener la URL de la route
          ROUTE_URL=$(oc get route url-shortener -o jsonpath='{.spec.host}')
          echo "Application URL: https://$ROUTE_URL"
          
          # Verificar health check
          curl -f https://$ROUTE_URL/health/live || exit 1
          echo "✅ Deployment successful!"
```

#### 5.3 Configura los Secrets en GitHub

Ve a tu repositorio → Settings → Secrets and variables → Actions → New repository secret:

| Secret Name | Valor |
|-------------|-------|
| `OPENSHIFT_TOKEN` | Tu token de OpenShift (oc whoami -t) |
| `OPENSHIFT_SERVER` | URL del servidor OpenShift |

### ✅ Checkpoint de Validación

<details>
<summary>🔍 ¿Cómo sé que lo hice bien?</summary>

1. Haz un commit y push a `main`
2. Ve a la pestaña "Actions" en GitHub
3. Deberías ver:
   - ✅ CI workflow ejecutándose (tests + build)
   - ✅ CD workflow ejecutándose después (deploy)

4. Verifica en OpenShift:
   ```bash
   oc get pods
   oc get routes
   ```

5. Accede a la URL de la route y prueba:
   ```bash
   curl -X POST https://<tu-route>/shorten \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.google.com"}'
   ```

</details>

<details>
<summary>💡 Hint: El workflow de CD no se ejecuta</summary>

Verifica que:
1. El workflow de CI terminó con éxito
2. El push fue a la rama `main`
3. Los secrets están bien configurados

Para depurar:
```yaml
# Añade esto al job de deploy para ver qué pasa
- name: Debug
  run: |
    echo "Event: ${{ github.event.workflow_run.conclusion }}"
    echo "Branch: ${{ github.event.workflow_run.head_branch }}"
```

</details>

### 🧩 Retos de la Fase 5

<details>
<summary>🎯 Reto 5.1: Añadir paso de seguridad al CI</summary>

**Problema:** El pipeline no verifica si hay vulnerabilidades antes de desplegar.

**Tu tarea:** Añade un job `security` al workflow de CI que:
1. Ejecute Trivy contra la imagen construida
2. Falle el pipeline si hay vulnerabilidades CRITICAL
3. Se ejecute DESPUÉS del build pero ANTES del deploy

**Pista:**
```yaml
security:
  runs-on: ubuntu-latest
  needs: build  # Espera a que build termine
  steps:
    - name: Run Trivy
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: '${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ needs.build.outputs.image_tag }}'
        severity: 'CRITICAL'
        exit-code: '1'
```

**¿Cómo sé que lo hice bien?** Si la imagen tiene vulnerabilidades críticas, el pipeline debe fallar y NO desplegar.
</details>

<details>
<summary>🎯 Reto 5.2: Notificaciones a Slack/Discord</summary>

**Problema:** No te enteras si el deploy falla (o tiene éxito) a menos que mires GitHub.

**Tu tarea:** Añade un paso al final del workflow de CD que:
- Envíe un mensaje a Slack o Discord cuando el deploy termine
- Incluya: estado (éxito/fallo), URL de la app, commit hash
- Use color verde para éxito, rojo para fallo

**Pista para Discord:**
```yaml
- name: Discord notification
  if: always()  # Se ejecuta aunque falle el deploy
  uses: sarisia/actions-status-discord@v1
  with:
    webhook: ${{ secrets.DISCORD_WEBHOOK }}
    status: ${{ job.status }}
    title: "Deploy to OpenShift"
    description: "Commit: ${{ github.sha }}"
```

**¿Cómo sé que lo hice bien?** Debes recibir un mensaje en tu canal cada vez que se hace deploy.
</details>

<details>
<summary>🎯 Reto 5.3: Implementar Rollback Automático</summary>

**Problema:** Si el deploy falla, la app queda en mal estado.

**Tu tarea:** Modifica el workflow de CD para que:
1. Guarde el estado actual antes de desplegar (imagen anterior)
2. Si el health check falla después del deploy, haga rollback automático
3. Notifique que hubo rollback

**Pista:**
```yaml
- name: Save current state
  run: |
    CURRENT_IMAGE=$(oc get deployment url-shortener -o jsonpath='{.spec.template.spec.containers[0].image}')
    echo "ROLLBACK_IMAGE=$CURRENT_IMAGE" >> $GITHUB_ENV

- name: Deploy
  run: |
    # ... deploy normal ...

- name: Health check
  id: healthcheck
  continue-on-error: true
  run: |
    sleep 30
    curl -f https://$ROUTE_URL/health/ready || exit 1

- name: Rollback if failed
  if: steps.healthcheck.outcome == 'failure'
  run: |
    echo "❌ Health check failed, rolling back..."
    oc set image deployment/url-shortener url-shortener=${{ env.ROLLBACK_IMAGE }}
    oc rollout status deployment/url-shortener
```
</details>

<details>
<summary>🎯 Reto 5.4: Pipeline para PRs con preview environments</summary>

**Problema:** Los PRs solo ejecutan tests, no puedes ver la app funcionando hasta que mergeas.

**Tu tarea (avanzado):** Crea un workflow que:
1. Cuando se abre un PR, despliegue una versión preview de la app
2. El namespace sea dinámico: `pr-<numero>` (ej: `pr-42`)
3. Comente en el PR con la URL del preview
4. Cuando el PR se cierre, elimine el preview environment

**Esto es complejo. Divide el problema:**
- Primero: crear namespace dinámico
- Segundo: desplegar ahí
- Tercero: comentar en el PR (usa `actions/github-script`)
- Cuarto: cleanup al cerrar PR

**Recursos:**
- `github.event.pull_request.number` → número del PR
- `github.event.action` → `opened`, `closed`, `synchronize`
</details>

---

## Fase 6: Helm Chart

### 🎯 Objetivo
Convertir los manifiestos de Kubernetes en un Helm Chart parametrizable.

### 📝 Tareas

#### 6.1 Crea la estructura del Helm Chart

```bash
mkdir -p helm/url-shortener/templates
```

#### 6.2 Crea `helm/url-shortener/Chart.yaml`

```yaml
apiVersion: v2
name: url-shortener
description: A URL shortener application
type: application
version: 1.0.0
appVersion: "1.0.0"
```

#### 6.3 Crea `helm/url-shortener/values.yaml`

```yaml
# Default values for url-shortener

replicaCount: 2

image:
  repository: ghcr.io/TU-USUARIO/url-shortener
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 5000

route:
  enabled: true
  host: ""  # Dejar vacío para autogenerar

resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "500m"

config:
  baseUrl: ""  # Se autoconfigura con la route

database:
  enabled: true
  host: postgresql
  port: 5432
  name: urlshortener
  user: urlshortener
  password: password123  # Override en producción

postgresql:
  enabled: true
  storage: 1Gi

cronjob:
  enabled: true
  schedule: "0 2 * * *"

probes:
  liveness:
    initialDelaySeconds: 10
    periodSeconds: 10
  readiness:
    initialDelaySeconds: 5
    periodSeconds: 5
```

#### 6.4 Crea `helm/url-shortener/values-dev.yaml`

```yaml
replicaCount: 1

resources:
  requests:
    memory: "64Mi"
    cpu: "50m"
  limits:
    memory: "128Mi"
    cpu: "250m"

postgresql:
  storage: 512Mi
```

#### 6.5 Crea `helm/url-shortener/values-pro.yaml`

```yaml
replicaCount: 3

resources:
  requests:
    memory: "256Mi"
    cpu: "200m"
  limits:
    memory: "512Mi"
    cpu: "1000m"

postgresql:
  storage: 5Gi

cronjob:
  schedule: "0 3 * * *"
```

#### 6.6 Crea `helm/url-shortener/templates/_helpers.tpl`

```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "url-shortener.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "url-shortener.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "url-shortener.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
app.kubernetes.io/name: {{ include "url-shortener.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Values.image.tag | default .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "url-shortener.selectorLabels" -}}
app.kubernetes.io/name: {{ include "url-shortener.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Database URL
*/}}
{{- define "url-shortener.databaseUrl" -}}
postgresql://{{ .Values.database.user }}:{{ .Values.database.password }}@{{ .Values.database.host }}:{{ .Values.database.port }}/{{ .Values.database.name }}
{{- end }}
```

#### 6.7 Crea `helm/url-shortener/templates/configmap.yaml`

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "url-shortener.fullname" . }}-config
  labels:
    {{- include "url-shortener.labels" . | nindent 4 }}
data:
  {{- if .Values.config.baseUrl }}
  BASE_URL: {{ .Values.config.baseUrl | quote }}
  {{- else if .Values.route.enabled }}
  BASE_URL: "https://{{ include "url-shortener.fullname" . }}-{{ .Release.Namespace }}.apps.sandbox.openshiftapps.com"
  {{- else }}
  BASE_URL: "http://localhost:5000"
  {{- end }}
```

#### 6.8 Crea `helm/url-shortener/templates/secret.yaml`

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "url-shortener.fullname" . }}-secret
  labels:
    {{- include "url-shortener.labels" . | nindent 4 }}
type: Opaque
stringData:
  DATABASE_URL: {{ include "url-shortener.databaseUrl" . | quote }}
```

#### 6.9 Crea `helm/url-shortener/templates/deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "url-shortener.fullname" . }}
  labels:
    {{- include "url-shortener.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "url-shortener.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "url-shortener.selectorLabels" . | nindent 8 }}
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - containerPort: 5000
              protocol: TCP
          envFrom:
            - configMapRef:
                name: {{ include "url-shortener.fullname" . }}-config
            - secretRef:
                name: {{ include "url-shortener.fullname" . }}-secret
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
          livenessProbe:
            httpGet:
              path: /health/live
              port: 5000
            initialDelaySeconds: {{ .Values.probes.liveness.initialDelaySeconds }}
            periodSeconds: {{ .Values.probes.liveness.periodSeconds }}
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 5000
            initialDelaySeconds: {{ .Values.probes.readiness.initialDelaySeconds }}
            periodSeconds: {{ .Values.probes.readiness.periodSeconds }}
```

#### 6.10 Crea `helm/url-shortener/templates/service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: {{ include "url-shortener.fullname" . }}
  labels:
    {{- include "url-shortener.labels" . | nindent 4 }}
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
      targetPort: 5000
      protocol: TCP
      name: http
  selector:
    {{- include "url-shortener.selectorLabels" . | nindent 4 }}
```

#### 6.11 Crea `helm/url-shortener/templates/route.yaml`

```yaml
{{- if .Values.route.enabled }}
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: {{ include "url-shortener.fullname" . }}
  labels:
    {{- include "url-shortener.labels" . | nindent 4 }}
spec:
  {{- if .Values.route.host }}
  host: {{ .Values.route.host }}
  {{- end }}
  to:
    kind: Service
    name: {{ include "url-shortener.fullname" . }}
    weight: 100
  port:
    targetPort: http
  tls:
    termination: edge
    insecureEdgeTerminationPolicy: Redirect
{{- end }}
```

#### 6.12 Crea `helm/url-shortener/templates/cronjob.yaml`

```yaml
{{- if .Values.cronjob.enabled }}
apiVersion: batch/v1
kind: CronJob
metadata:
  name: {{ include "url-shortener.fullname" . }}-cleanup
  labels:
    {{- include "url-shortener.labels" . | nindent 4 }}
spec:
  schedule: {{ .Values.cronjob.schedule | quote }}
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 3
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: cleanup
              image: postgres:15-alpine
              command:
                - /bin/sh
                - -c
                - |
                  psql $DATABASE_URL -c "DELETE FROM urls WHERE expires_at < NOW();"
                  echo "Cleanup completed at $(date)"
              envFrom:
                - secretRef:
                    name: {{ include "url-shortener.fullname" . }}-secret
          restartPolicy: OnFailure
{{- end }}
```

#### 6.13 Crea `helm/url-shortener/templates/postgresql.yaml`

```yaml
{{- if .Values.postgresql.enabled }}
---
apiVersion: v1
kind: Secret
metadata:
  name: postgresql-secret
  labels:
    {{- include "url-shortener.labels" . | nindent 4 }}
type: Opaque
stringData:
  POSTGRES_USER: {{ .Values.database.user }}
  POSTGRES_PASSWORD: {{ .Values.database.password }}
  POSTGRES_DB: {{ .Values.database.name }}

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgresql-pvc
  labels:
    {{- include "url-shortener.labels" . | nindent 4 }}
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: {{ .Values.postgresql.storage }}

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgresql
  labels:
    {{- include "url-shortener.labels" . | nindent 4 }}
    app: postgresql
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgresql
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        app: postgresql
    spec:
      containers:
        - name: postgresql
          image: postgres:15-alpine
          ports:
            - containerPort: 5432
          envFrom:
            - secretRef:
                name: postgresql-secret
          volumeMounts:
            - name: postgresql-data
              mountPath: /var/lib/postgresql/data
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "500m"
      volumes:
        - name: postgresql-data
          persistentVolumeClaim:
            claimName: postgresql-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: postgresql
  labels:
    {{- include "url-shortener.labels" . | nindent 4 }}
    app: postgresql
spec:
  type: ClusterIP
  ports:
    - port: 5432
      targetPort: 5432
  selector:
    app: postgresql
{{- end }}
```

### ✅ Checkpoint de Validación

<details>
<summary>🔍 ¿Cómo sé que lo hice bien?</summary>

```bash
# Validar el chart
helm lint helm/url-shortener/

# Ver qué se generaría (dry-run)
helm template my-release helm/url-shortener/ -f helm/url-shortener/values-dev.yaml

# Instalar en OpenShift
helm install url-shortener helm/url-shortener/ \
  -f helm/url-shortener/values-dev.yaml \
  --namespace tu-namespace

# Verificar
helm list
oc get pods
oc get routes
```

</details>

### 🧩 Retos de la Fase 6

<details>
<summary>🎯 Reto 6.1: Hacer el PostgreSQL opcional</summary>

**Problema:** El chart siempre despliega PostgreSQL, pero en producción podrías usar una base de datos managed (RDS, Cloud SQL).

**Tu tarea:** Modifica el chart para que:
- Si `postgresql.enabled: true` → despliegue PostgreSQL (como ahora)
- Si `postgresql.enabled: false` → NO despliegue PostgreSQL
- Añade un nuevo valor `database.externalHost` para conectarse a una BD externa

**Ejemplo de values-pro.yaml:**
```yaml
postgresql:
  enabled: false

database:
  host: "mi-rds.xxxxx.eu-west-1.rds.amazonaws.com"
  port: 5432
  name: urlshortener
  user: admin
  password: ""  # Se configuraría con un secret externo
```

**¿Cómo sé que lo hice bien?**
```bash
# Con PostgreSQL
helm template test ./helm/url-shortener -f values-dev.yaml | grep -c "kind: Deployment"
# Debe mostrar: 2 (app + postgresql)

# Sin PostgreSQL
helm template test ./helm/url-shortener -f values-pro.yaml | grep -c "kind: Deployment"
# Debe mostrar: 1 (solo app)
```
</details>

<details>
<summary>🎯 Reto 6.2: Añadir Ingress como alternativa a Route</summary>

**Problema:** Route es específico de OpenShift. Si quieres desplegar en otro Kubernetes, necesitas Ingress.

**Tu tarea:** 
1. Crea `templates/ingress.yaml`
2. Añade valores en `values.yaml`:
```yaml
ingress:
  enabled: false
  className: "nginx"
  host: "url-shortener.example.com"
  tls: true
```
3. Haz que Route e Ingress sean mutuamente excluyentes

**Pista en el template:**
```yaml
{{- if and .Values.ingress.enabled (not .Values.route.enabled) }}
apiVersion: networking.k8s.io/v1
kind: Ingress
# ...
{{- end }}
```
</details>

<details>
<summary>🎯 Reto 6.3: Helm hooks para migraciones de BD</summary>

**Problema:** Cuando despliegas una nueva versión, puede que necesites ejecutar migraciones de base de datos ANTES de que arranque la nueva versión de la app.

**Tu tarea:** Crea un Helm hook que:
1. Se ejecute ANTES del upgrade (`pre-upgrade`)
2. Corra un Job que ejecute las migraciones
3. Solo continúe con el deploy si las migraciones fueron exitosas

**Pista:**
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "url-shortener.fullname" . }}-migrate
  annotations:
    "helm.sh/hook": pre-upgrade
    "helm.sh/hook-weight": "-5"
    "helm.sh/hook-delete-policy": hook-succeeded
spec:
  template:
    spec:
      containers:
        - name: migrate
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          command: ["python", "-c", "from app.models import db; db.create_all()"]
          # ...
```

**Para probar:** Añade un campo nuevo al modelo, haz upgrade, y verifica que la columna existe.
</details>

<details>
<summary>🎯 Reto 6.4: Crear un umbrella chart</summary>

**Problema:** Quieres que con un solo `helm install` se despliegue toda la stack: app + monitoring + base de datos.

**Tu tarea:** Crea un "umbrella chart" que:
1. Tenga como dependencias:
   - Tu chart url-shortener
   - Bitnami PostgreSQL (en vez del tuyo manual)
2. Configure todo desde un solo values.yaml

**Estructura:**
```
helm/
├── url-shortener/          # Tu chart actual
└── url-shortener-stack/    # Nuevo umbrella chart
    ├── Chart.yaml
    ├── values.yaml
    └── charts/             # Dependencias se descargan aquí
```

**Chart.yaml del umbrella:**
```yaml
apiVersion: v2
name: url-shortener-stack
version: 1.0.0
dependencies:
  - name: url-shortener
    version: "1.0.0"
    repository: "file://../url-shortener"
  - name: postgresql
    version: "12.x.x"
    repository: "https://charts.bitnami.com/bitnami"
```

**Comandos:**
```bash
cd helm/url-shortener-stack
helm dependency update
helm install full-stack .
```
</details>

---

## Fase 7: Actualizar CI/CD para Helm

### 🎯 Objetivo
Modificar el pipeline para desplegar usando Helm.

### 📝 Tareas

#### 7.1 Actualiza `.github/workflows/cd.yml`

```yaml
name: CD

on:
  workflow_run:
    workflows: [CI]
    types: [completed]
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  deploy-dev:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    environment: development
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Install OpenShift CLI
        uses: redhat-actions/oc-installer@v1
        with:
          oc_version: '4.12'
      
      - name: Install Helm
        uses: azure/setup-helm@v3
        with:
          version: '3.13.0'
      
      - name: Login to OpenShift
        run: |
          oc login --token=${{ secrets.OPENSHIFT_TOKEN }} --server=${{ secrets.OPENSHIFT_SERVER }}
      
      - name: Set image tag
        run: |
          echo "IMAGE_TAG=$(git rev-parse --short HEAD)" >> $GITHUB_ENV
      
      - name: Deploy with Helm
        run: |
          helm upgrade --install url-shortener ./helm/url-shortener \
            -f ./helm/url-shortener/values-dev.yaml \
            --set image.repository=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }} \
            --set image.tag=${{ env.IMAGE_TAG }} \
            --wait \
            --timeout 300s
      
      - name: Verify deployment
        run: |
          ROUTE_URL=$(oc get route url-shortener -o jsonpath='{.spec.host}')
          echo "🚀 Application URL: https://$ROUTE_URL"
          
          # Wait for app to be ready
          sleep 10
          
          # Health check
          curl -f https://$ROUTE_URL/health/live || exit 1
          echo "✅ Deployment successful!"
```

---

## 🧩 Retos Finales (Bonus)

Estos retos combinan todo lo aprendido. ¡Solo para valientes!

<details>
<summary>🏆 Reto Final 1: Añadir métricas con Prometheus</summary>

**Problema:** No tienes visibilidad de cómo se comporta tu app (requests por segundo, latencia, errores).

**Tu tarea completa:**

1. **En la app Python:** Añade la librería `prometheus-flask-exporter`
   ```python
   from prometheus_flask_exporter import PrometheusMetrics
   metrics = PrometheusMetrics(app)
   ```

2. **En Kubernetes:** Crea un ServiceMonitor para que Prometheus descubra tu app
   ```yaml
   apiVersion: monitoring.coreos.com/v1
   kind: ServiceMonitor
   metadata:
     name: url-shortener-monitor
   spec:
     selector:
       matchLabels:
         app: url-shortener
     endpoints:
       - port: http
         path: /metrics
   ```

3. **Verifica:** Accede a `/metrics` en tu app y ve las métricas

4. **Bonus:** Crea un dashboard en Grafana con:
   - Requests por segundo
   - Latencia p50, p95, p99
   - Tasa de errores
</details>

<details>
<summary>🏆 Reto Final 2: Implementar Blue-Green Deployment</summary>

**Problema:** Los rolling updates pueden causar problemas si la nueva versión es incompatible.

**Tu tarea:**
1. Modifica el Helm chart para soportar blue-green deployments
2. Crea dos deployments: `url-shortener-blue` y `url-shortener-green`
3. El Service apunta a uno de ellos (configurable)
4. El switch entre versiones es instantáneo cambiando el selector del Service

**Flujo:**
```
1. Blue está activo (recibe tráfico)
2. Despliegas nueva versión en Green
3. Pruebas Green internamente
4. Cambias el Service para apuntar a Green
5. Blue queda como backup para rollback instantáneo
```

**¿Cómo sé que lo hice bien?**
```bash
# Cambiar de blue a green
helm upgrade url-shortener ./helm/url-shortener --set activeColor=green

# El cambio debe ser instantáneo (< 1 segundo de downtime)
```
</details>

<details>
<summary>🏆 Reto Final 3: Disaster Recovery</summary>

**Problema:** Si se borra el namespace por accidente, pierdes todo.

**Tu tarea:**
1. **Backup de la BD:** Crea un CronJob que haga `pg_dump` cada hora y suba el backup a un bucket S3 o PVC separado

2. **Backup de los manifiestos:** Investiga e implementa Velero para backup de recursos de Kubernetes

3. **Documenta el proceso de recovery:** Escribe un runbook (documento paso a paso) de cómo restaurar todo desde cero

4. **Prueba el disaster recovery:** Borra todo y recupéralo siguiendo tu runbook

**El runbook debe incluir:**
- Tiempo estimado de recuperación (RTO)
- Punto de recuperación (RPO) - ¿cuántos datos puedes perder?
- Comandos exactos a ejecutar
- Verificaciones post-recovery
</details>

<details>
<summary>🏆 Reto Final 4: Multi-tenancy</summary>

**Problema:** Quieres ofrecer el URL Shortener como SaaS, donde cada cliente tiene sus propios datos aislados.

**Tu tarea:**
1. Modifica la app para soportar múltiples "tenants"
2. Cada tenant tiene su propio subdominio: `cliente1.tu-app.com`, `cliente2.tu-app.com`
3. Los datos están aislados (un tenant no puede ver URLs de otro)
4. Implementa rate limiting por tenant

**Opciones de arquitectura (elige una):**
- **Base de datos compartida:** Una tabla `urls` con columna `tenant_id`
- **Schema por tenant:** Cada tenant tiene su propio schema en PostgreSQL
- **Base de datos por tenant:** Más aislamiento, más complejidad

**¿Cómo sé que lo hice bien?**
```bash
# Crear URL como tenant1
curl -X POST https://tenant1.tu-app.com/shorten -d '{"url": "..."}'

# No debe aparecer en tenant2
curl https://tenant2.tu-app.com/urls
# Lista vacía
```
</details>

---

## 🏆 Rúbrica de Autoevaluación

Cuando termines, evalúa tu trabajo:

### Parte 1: Implementación Base (100 puntos)

| Criterio | Puntos | ✅/❌ |
|----------|--------|-------|
| **Entorno configurado (Fase 0)** | 10 | |
| OpenShift Sandbox funcionando | 3 | |
| ghcr.io configurado | 3 | |
| Secrets en GitHub Actions | 4 | |
| **API funciona localmente** | 10 | |
| Endpoint POST /shorten crea URLs | 5 | |
| Endpoint GET /:code redirige | 5 | |
| **Tests pasan** | 10 | |
| Todos los tests en verde | 10 | |
| **Docker** | 10 | |
| Dockerfile creado correctamente | 5 | |
| .dockerignore configurado | 5 | |
| **Kubernetes** | 20 | |
| Deployment funciona | 5 | |
| Service expone correctamente | 5 | |
| Route accesible desde internet | 5 | |
| Probes configurados | 5 | |
| **Base de datos** | 10 | |
| PostgreSQL desplegado | 5 | |
| PersistentVolume configurado | 5 | |
| **CI/CD** | 20 | |
| CI ejecuta tests automáticamente | 10 | |
| CD despliega automáticamente | 10 | |
| **Helm** | 10 | |
| Chart válido (helm lint pasa) | 5 | |
| Values por entorno funcionan | 5 | |
| **CronJob** | 5 | |
| CronJob configurado | 5 | |
| **TOTAL BASE** | **105** | |

---

### Parte 2: Retos Completados (Puntos Extra)

| Reto | Puntos | ✅/❌ |
|------|--------|-------|
| **Fase 1** | | |
| 1.1 URL duplicada | 5 | |
| 1.2 Endpoint DELETE | 5 | |
| 1.3 Custom short_code | 10 | |
| **Fase 2** | | |
| 2.1 Tests para nuevas features | 10 | |
| 2.2 Test de expiración | 10 | |
| 2.3 Cobertura 80%+ | 5 | |
| **Fase 3** | | |
| 3.1 Entender Dockerfile multi-stage | 5 | |
| 3.2 Labels OCI | 5 | |
| 3.3 Investigar seguridad contenedores | 5 | |
| **Fase 4** | | |
| 4.1 Debugging del Deployment | 5 | |
| 4.2 HorizontalPodAutoscaler | 10 | |
| 4.3 NetworkPolicy | 10 | |
| 4.4 Arreglar CronJob | 5 | |
| **Fase 5** | | |
| 5.1 Security scan en CI | 10 | |
| 5.2 Notificaciones Slack/Discord | 10 | |
| 5.3 Rollback automático | 15 | |
| 5.4 Preview environments | 20 | |
| **Fase 6** | | |
| 6.1 PostgreSQL opcional | 10 | |
| 6.2 Ingress alternativo | 10 | |
| 6.3 Helm hooks migraciones | 15 | |
| 6.4 Umbrella chart | 15 | |
| **TOTAL RETOS** | **190** | |

---

### Parte 3: Retos Finales Bonus

| Reto | Puntos | ✅/❌ |
|------|--------|-------|
| Métricas Prometheus + Grafana | 25 | |
| Blue-Green Deployment | 30 | |
| Disaster Recovery | 25 | |
| Multi-tenancy | 40 | |
| **TOTAL BONUS** | **120** | |

---

### Puntuación Final

| Sección | Máximo | Tu puntuación |
|---------|--------|---------------|
| Base | 105 | |
| Retos | 190 | |
| Bonus | 120 | |
| **TOTAL** | **415** | |

**Niveles:**
- 🥉 **105-160 puntos:** Junior DevOps - ¡Buen comienzo!
- 🥈 **161-250 puntos:** Mid DevOps - Tienes una base sólida
- 🥇 **251-350 puntos:** Senior DevOps - ¡Impresionante!
- 🏆 **351+ puntos:** DevOps Master - Estás lista para cualquier reto

---

## 🎉 ¿Terminaste?

¡Felicidades! Has construido una aplicación completa con:

- ✅ API REST funcional
- ✅ Base de datos persistente
- ✅ Containerización optimizada
- ✅ Despliegue en Kubernetes/OpenShift
- ✅ CI/CD automatizado
- ✅ Parametrización con Helm
- ✅ Tareas programadas

**Siguiente paso:** Cuando domines esto, podemos avanzar a:
- 🔧 Terraform + AWS
- 🔄 GitOps con ArgoCD
- 🔒 DevSecOps (Trivy, SAST/DAST)

---

## 📚 Recursos Útiles

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [OpenShift Documentation](https://docs.openshift.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
