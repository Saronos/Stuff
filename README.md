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

## ⚠️ Nota Importante: NO necesitas Docker

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Este proyecto está diseñado para funcionar SIN Docker     │
│   en tu máquina local.                                      │
│                                                             │
│   • LOCAL: Python + SQLite (simple, sin instalaciones extra)│
│   • GITHUB ACTIONS: Construye la imagen Docker por ti       │
│   • OPENSHIFT: Ejecuta la imagen con PostgreSQL             │
│                                                             │
│   Tú solo escribes el Dockerfile. GitHub Actions se         │
│   encarga de construirlo y subirlo a ghcr.io.               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Resumen de cambios aplicados

> **Nota:** Si vienes de una versión anterior del README, estos son los cambios relevantes:
>
> 1. **Dockerfile** — Corregido el mismatch de rutas de dependencias. Ahora usa `pip install --user` y copia correctamente de `/root/.local` a `/home/appuser/.local`.
> 2. **`app/app.py`** — Añadida validación de expiración (devuelve 410 Gone) y manejo de race conditions con retry + IntegrityError.
> 3. **`ci.yml`** — Eliminado `no-cache: true` que contradecía la configuración de caché GHA.
> 4. **`cd.yml`** — `IMAGE_NAME` ahora usa `${{ github.repository }}` dinámicamente en vez de estar hardcodeado.
> 5. **Helm `deployment.yaml`** — Los `initialDelaySeconds` ahora usan valores del `values.yaml` en vez de estar hardcodeados.
> 6. **`values-pro.yaml`** — Movido a `helm/url-shortener/values-pro.yaml` (ubicación correcta para Helm).

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

## 📁 Estructura Final del Proyecto

```
url-shortener/
├── .github/
│   └── workflows/
│       ├── ci.yml              # Tests en cada PR
│       └── cd.yml              # Deploy a OpenShift
├── app/
│   ├── __init__.py
│   ├── app.py                  # API Flask
│   ├── models.py               # Modelos de BD
│   ├── config.py               # Configuración
│   └── utils.py                # Generador de códigos cortos
├── tests/
│   ├── __init__.py
│   ├── test_app.py             # Tests unitarios
│   └── test_integration.py     # Tests de integración
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── route.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   └── cronjob.yaml            # Limpieza de URLs expiradas
├── helm/
│   └── url-shortener/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── values-dev.yaml
│       ├── values-pro.yaml     # ⚠️ DENTRO de url-shortener/, no en helm/
│       └── templates/
│           ├── deployment.yaml
│           ├── service.yaml
│           ├── route.yaml
│           ├── configmap.yaml
│           ├── secret.yaml
│           └── cronjob.yaml
├── Dockerfile
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🗺️ Mapa de Fases

```
FASE 0 → FASE 1 → FASE 2 → FASE 3 → FASE 4 → FASE 5 → FASE 6 → FASE 7
Setup    API      Tests    Docker   K8s      CI/CD    Helm     Deploy
```

---

# 🚀 FASES DEL PROYECTO

---

## Fase 0: Setup del Entorno

### 🎯 Objetivo
Configurar todo lo necesario: Python, OpenShift CLI, y secrets en GitHub.

```
┌─────────────────────────────────────────────────────────────┐
│   💡 NO necesitas Docker en tu máquina.                     │
│   GitHub Actions construye las imágenes por ti.             │
│   Local: Python + SQLite | OpenShift: PostgreSQL            │
└─────────────────────────────────────────────────────────────┘
```

### 📝 Tareas

#### 0.1 Instalar Python

**Windows:**
1. Descarga Python **3.11** o **3.12** de python.org (NO 3.14)
2. ☑️ **"Add python.exe to PATH"** ← MUY IMPORTANTE
3. Verifica: `python --version`

**Mac:** `brew install python@3.11`

**Linux:** `sudo apt install python3.11 python3.11-venv python3-pip`

#### 0.2 Crear cuenta en OpenShift Developer Sandbox

1. Ve a https://developers.redhat.com/developer-sandbox
2. "Start your sandbox for free"
3. Crea cuenta Red Hat, verifica teléfono
4. Tu sandbox incluye: namespace propio, CPU/memoria limitados, 30 días renovable

#### 0.3 Instalar OpenShift CLI (oc)

En la consola web de OpenShift: **Help (?)** → **Command Line Tools** → descarga para tu OS.

#### 0.4 Login en OpenShift

1. Consola web → tu nombre → **"Copy login command"** → **"Display Token"**
2. `oc login --token=sha256~XXX --server=https://api.sandbox-xxx.openshiftapps.com:6443`
3. Verifica: `oc whoami` y `oc project`

> ⚠️ El token expira cada 24 horas. Repite este paso si ves errores de autenticación.

#### 0.5 Configurar Secrets en GitHub Actions

Repo → Settings → Secrets and variables → Actions:

| Secret Name | Valor |
|-------------|-------|
| `OPENSHIFT_SERVER` | URL del servidor OpenShift |
| `OPENSHIFT_TOKEN` | Token sha256~ del login |

> `GITHUB_TOKEN` ya existe automáticamente, no necesitas crearlo.

#### 0.6 Instalar Helm

**Windows:** https://github.com/helm/helm/releases
**Mac:** `brew install helm`
**Linux:** `curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash`

---

## Fase 1: Setup del Proyecto y API Local

### 🎯 Objetivo
Crear la API de Flask funcionando en local.

### 📝 Tareas

#### 1.1 Crea el repositorio
Repo `url-shortener` en GitHub, clónalo y crea la estructura de carpetas.

#### 1.2 `requirements.txt`

```txt
flask==3.0.0
flask-sqlalchemy==3.1.1
psycopg2-binary==2.9.9
python-dotenv==1.0.0
gunicorn==21.2.0
pytest==7.4.3
pytest-flask==1.3.0
```

#### 1.2b `.gitignore`

```
__pycache__/
*.py[cod]
*.db
urlshortener.db
env/
venv/
.venv/
.pytest_cache/
.coverage
.idea/
.vscode/
.DS_Store
```

#### 1.3 `app/config.py`

```python
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///urlshortener.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')
```

#### 1.4 `app/models.py`

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

#### 1.5 `app/utils.py`

```python
import string
import random

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
```

#### 1.6 `app/app.py`

```python
from flask import Flask, request, jsonify, redirect
from app.models import db, URL
from app.utils import generate_short_code
from app.config import Config
from datetime import datetime
from sqlalchemy.exc import IntegrityError


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
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
    
    @app.route('/shorten', methods=['POST'])
    def shorten_url():
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({'error': 'URL is required'}), 400
        
        original_url = data['url']
        
        if not original_url.startswith(('http://', 'https://')):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        # Generar código único con retry para manejar race conditions
        max_retries = 5
        for attempt in range(max_retries):
            short_code = generate_short_code()
            try:
                url_entry = URL(original_url=original_url, short_code=short_code)
                db.session.add(url_entry)
                db.session.commit()
                return jsonify(url_entry.to_dict()), 201
            except IntegrityError:
                db.session.rollback()
                if attempt == max_retries - 1:
                    return jsonify({'error': 'Could not generate unique code, try again'}), 503
    
    @app.route('/<short_code>', methods=['GET'])
    def redirect_to_url(short_code):
        url_entry = URL.query.filter_by(short_code=short_code).first()
        
        if not url_entry:
            return jsonify({'error': 'URL not found'}), 404
        
        # Comprobar si la URL ha expirado
        if url_entry.expires_at and url_entry.expires_at < datetime.utcnow():
            return jsonify({'error': 'URL has expired'}), 410
        
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

> 📝 **Nota:** Este código ya incluye:
> - **Validación de expiración:** Devuelve 410 (Gone) si la URL ha expirado, en vez de redirigir.
> - **Manejo de race conditions:** Usa retry con `IntegrityError` para evitar colisiones de short_code.

#### 1.7 `app/__init__.py`

```python
from app.app import create_app, app
from app.models import db, URL

__all__ = ['create_app', 'app', 'db', 'URL']
```

### ✅ Checkpoint

1. `python -m pip install -r requirements.txt`
2. `python -m app.app` → debe arrancar en http://127.0.0.1:5000
3. Prueba: `curl -X POST http://localhost:5000/shorten -H "Content-Type: application/json" -d '{"url": "https://www.google.com"}'`
4. Abre `http://localhost:5000/<short_code>` → debe redirigir

### 🧩 Retos de la Fase 1

**Reto 1.1:** Validación de URL duplicada — si la URL ya existe, devolver el short_code existente.

**Reto 1.2:** Endpoint DELETE `/urls/<short_code>` que devuelva 204 o 404.

**Reto 1.3:** Personalizar short_code — campo opcional `custom_code`, validar caracteres y longitud máxima 20.

---

## Fase 2: Tests

### 🎯 Objetivo
Crear tests para asegurar que tu API funciona correctamente.

### 📝 Tareas

#### 2.1 `tests/__init__.py`
```python
# Empty file
```

#### 2.2 `tests/conftest.py`

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

#### 2.3 `tests/test_app.py`

```python
import json

def test_health_live(client):
    response = client.get('/health/live')
    assert response.status_code == 200
    assert response.json['status'] == 'alive'

def test_health_ready(client):
    response = client.get('/health/ready')
    assert response.status_code == 200
    assert response.json['status'] == 'ready'

def test_shorten_url_success(client):
    response = client.post('/shorten',
        data=json.dumps({'url': 'https://www.example.com'}),
        content_type='application/json')
    assert response.status_code == 201
    data = response.json
    assert 'short_code' in data
    assert data['original_url'] == 'https://www.example.com'
    assert len(data['short_code']) == 6

def test_shorten_url_missing_url(client):
    response = client.post('/shorten',
        data=json.dumps({}),
        content_type='application/json')
    assert response.status_code == 400

def test_shorten_url_invalid_format(client):
    response = client.post('/shorten',
        data=json.dumps({'url': 'not-a-valid-url'}),
        content_type='application/json')
    assert response.status_code == 400

def test_redirect_success(client):
    create_response = client.post('/shorten',
        data=json.dumps({'url': 'https://www.example.com'}),
        content_type='application/json')
    short_code = create_response.json['short_code']
    redirect_response = client.get(f'/{short_code}')
    assert redirect_response.status_code == 302

def test_redirect_not_found(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404

def test_stats_endpoint(client):
    create_response = client.post('/shorten',
        data=json.dumps({'url': 'https://www.example.com'}),
        content_type='application/json')
    short_code = create_response.json['short_code']
    client.get(f'/{short_code}')
    stats_response = client.get(f'/stats/{short_code}')
    assert stats_response.status_code == 200
    assert stats_response.json['clicks'] == 1

def test_list_urls(client):
    client.post('/shorten', data=json.dumps({'url': 'https://www.example1.com'}), content_type='application/json')
    client.post('/shorten', data=json.dumps({'url': 'https://www.example2.com'}), content_type='application/json')
    response = client.get('/urls')
    assert response.status_code == 200
    assert len(response.json) == 2
```

### ✅ Checkpoint
```bash
pytest tests/ -v
# Todos los tests en verde
```

### 🧩 Retos de la Fase 2

**Reto 2.1:** Tests para funcionalidades nuevas (duplicada, DELETE, custom_code). Mínimo 5 tests.

**Reto 2.2:** Test de expiración — La validación de expiración ya está implementada en `app.py` (devuelve 410 Gone). Tu tarea es solo escribir el test que lo verifique:

```python
from datetime import datetime, timedelta
from app.models import db, URL

url_entry = URL(
    original_url='https://www.example.com',
    short_code='expired1',
    expires_at=datetime.utcnow() - timedelta(days=1)
)
db.session.add(url_entry)
db.session.commit()
# GET /expired1 debe devolver 410
```

**Reto 2.3:** Medir cobertura con `pytest-cov`. Objetivo: ≥80%.

---

## Fase 3: Dockerización

### 🎯 Objetivo
Crear un Dockerfile para que GitHub Actions construya la imagen.

```
┌─────────────────────────────────────────────────────────────┐
│   💡 NO necesitas Docker en tu máquina                      │
│   Solo creas el Dockerfile. GitHub Actions lo construye.    │
└─────────────────────────────────────────────────────────────┘
```

### 📝 Tareas

#### 3.1 `Dockerfile`

```dockerfile
# ============================================
# Stage 1: Builder
# ============================================
FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ============================================
# Stage 2: Runtime
# ============================================
FROM python:3.11-slim as runtime

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /bin/bash appuser

# Copiar dependencias del builder (--user instala en /root/.local)
COPY --from=builder /root/.local /home/appuser/.local

COPY --chown=appuser:appuser app/ ./app/

ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health/live')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app.app:app"]
```

> 💡 **Detalle importante:** `pip install --user` instala en `/root/.local` (builder). Luego copiamos a `/home/appuser/.local` (runtime). El `ENV PATH` incluye `/home/appuser/.local/bin` para que `appuser` encuentre `gunicorn` y demás binarios.

#### 3.2 `.dockerignore`

```
__pycache__
*.pyc
*.db
.git
.gitignore
Dockerfile
*.md
tests/
.pytest_cache/
k8s/
helm/
.github/
```

### ✅ Checkpoint
Sin Docker local, la validación real será en Fase 5 cuando GitHub Actions construya la imagen.

### 🧩 Retos de la Fase 3

**Reto 3.1:** Responde: ¿Por qué multi-stage? ¿Por qué `--user`? ¿Por qué usuario no-root?

**Reto 3.2:** Añade OCI labels (`org.opencontainers.image.title`, etc.)

**Reto 3.3:** Investiga Trivy y CVEs. Documenta en `SEGURIDAD.md`.

---

## Fase 4: Manifiestos de Kubernetes

### 🎯 Objetivo
Crear los manifiestos para desplegar en OpenShift.

### 📝 Tareas

#### 4.1 `k8s/namespace.yaml` (opcional)

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: url-shortener
```

#### 4.2 `k8s/configmap.yaml`

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

#### 4.3 `k8s/secret.yaml`

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

#### 4.4 `k8s/deployment.yaml`

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
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 5000
            initialDelaySeconds: 5
            periodSeconds: 5
```

#### 4.5 `k8s/service.yaml`

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

#### 4.6 `k8s/route.yaml`

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
```

#### 4.7 `k8s/postgresql.yaml`

```yaml
---
apiVersion: v1
kind: Secret
metadata:
  name: postgresql-secret
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
spec:
  accessModes: [ReadWriteOnce]
  resources:
    requests:
      storage: 1Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgresql
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
              command: ["pg_isready", "-U", "urlshortener"]
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            exec:
              command: ["pg_isready", "-U", "urlshortener"]
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
spec:
  type: ClusterIP
  ports:
    - port: 5432
      targetPort: 5432
  selector:
    app: postgresql
```

#### 4.8 `k8s/cronjob.yaml`

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: url-shortener-cleanup
spec:
  schedule: "0 2 * * *"
  concurrencyPolicy: Forbid
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

### ✅ Checkpoint
```bash
oc apply -f k8s/postgresql.yaml
oc get pods -w  # Esperar a Running
oc apply -f k8s/configmap.yaml -f k8s/secret.yaml -f k8s/deployment.yaml -f k8s/service.yaml -f k8s/route.yaml -f k8s/cronjob.yaml
```

### 🧩 Retos de la Fase 4

**Reto 4.1:** Encuentra 5 errores en un Deployment roto (tipos de datos, labels, recursos, probes).

**Reto 4.2:** Crea `k8s/hpa.yaml` — HPA entre 2-10 réplicas, CPU 70%, memoria 80%.

**Reto 4.3:** Crea `k8s/networkpolicy.yaml` — solo pods `app: url-shortener` pueden conectar a PostgreSQL.

**Reto 4.4:** Diagnostica por qué el CronJob no funciona (`oc get cronjobs`, `oc get jobs`, `oc logs`).

---

## Fase 5: GitHub Actions CI/CD

### 🎯 Objetivo
Automatizar build, test y deploy con GitHub Actions.

### 📝 Tareas

#### 5.1 `.github/workflows/ci.yml`

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
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --ignore=W292,W293,E302,E305

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

> 📝 **Nota sobre flake8:** Usamos `--select=E9,F63,F7,F82` para detectar solo errores de sintaxis graves e ignorar cuestiones estéticas.

> 📝 **Nota sobre caché:** `cache-from/cache-to: type=gha` reutiliza capas entre builds. NO usamos `no-cache: true` porque anula este caché.

#### 5.2 `.github/workflows/cd.yml`

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
          oc_version: 'latest'
      
      - name: Login to OpenShift
        run: |
          oc login --token=${{ secrets.OPENSHIFT_TOKEN }} --server=${{ secrets.OPENSHIFT_SERVER }}
      
      - name: Set image tag
        run: |
          echo "IMAGE_TAG=$(git rev-parse --short HEAD)" >> $GITHUB_ENV
      
      - name: Deploy to OpenShift
        run: |
          oc set image deployment/url-shortener \
            url-shortener=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ env.IMAGE_TAG }} \
            --record
          oc rollout status deployment/url-shortener --timeout=300s
          oc wait --for=condition=ready pod -l app=url-shortener --timeout=120s

      - name: Verify deployment
        run: |
          ROUTE_URL=$(oc get route url-shortener -o jsonpath='{.spec.host}')
          echo "Application URL: https://$ROUTE_URL"
          for i in 1 2 3; do
            if curl -sf https://$ROUTE_URL/health/live; then
              echo "✅ Deployment successful!"
              exit 0
            fi
            echo "Intento $i fallido, esperando..."
            sleep 10
          done
          echo "❌ Deployment failed after 3 attempts."
          exit 1
```

> 📝 **Nota:** `IMAGE_NAME` usa `${{ github.repository }}` que se resuelve dinámicamente (ej: `asstrid98/url-shortener`). No se hardcodea.

#### 5.3 Secrets en GitHub

| Secret Name | Valor |
|-------------|-------|
| `OPENSHIFT_TOKEN` | `oc whoami -t` |
| `OPENSHIFT_SERVER` | URL del servidor OpenShift |

### ✅ Checkpoint
1. Push a `main` → pestaña Actions → CI (tests + build) → CD (deploy)
2. `oc get pods` y `oc get routes` en OpenShift

### 🧩 Retos de la Fase 5

**Reto 5.1:** Añade Trivy al CI para detectar vulnerabilidades CRITICAL antes del deploy.

**Reto 5.2:** Notificaciones a Slack/Discord en cada deploy.

**Reto 5.3:** Rollback automático si el health check post-deploy falla.

**Reto 5.4 (avanzado):** Preview environments por PR con namespace dinámico `pr-<numero>`.

---

## Fase 6: Helm Chart

### 🎯 Objetivo
Convertir los manifiestos K8s en un Helm Chart parametrizable.

### 📝 Tareas

#### 6.1 Estructura
```bash
mkdir -p helm/url-shortener/templates
```

#### 6.2 `helm/url-shortener/Chart.yaml`

```yaml
apiVersion: v2
name: url-shortener
description: A URL shortener application
type: application
version: 1.0.0
appVersion: "1.0.0"
```

#### 6.3 `helm/url-shortener/values.yaml`

```yaml
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
  host: ""

resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "500m"

config:
  baseUrl: ""

database:
  enabled: true
  host: postgresql
  port: 5432
  name: urlshortener
  user: urlshortener
  password: password123

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

#### 6.4 `helm/url-shortener/values-dev.yaml`

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

#### 6.5 `helm/url-shortener/values-pro.yaml`

> ⚠️ **Importante:** Este archivo va **dentro** de `helm/url-shortener/`, NO en `helm/`. Si lo pones en el sitio equivocado, Helm no lo encontrará con `-f values-pro.yaml`.

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

#### 6.6 `helm/url-shortener/templates/_helpers.tpl`

```yaml
{{- define "url-shortener.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

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

{{- define "url-shortener.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
app.kubernetes.io/name: {{ include "url-shortener.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Values.image.tag | default .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "url-shortener.selectorLabels" -}}
app.kubernetes.io/name: {{ include "url-shortener.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "url-shortener.databaseUrl" -}}
postgresql://{{ .Values.database.user }}:{{ .Values.database.password }}@{{ .Values.database.host }}:{{ .Values.database.port }}/{{ .Values.database.name }}
{{- end }}
```

#### 6.7 `helm/url-shortener/templates/configmap.yaml`

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

#### 6.8 `helm/url-shortener/templates/secret.yaml`

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

#### 6.9 `helm/url-shortener/templates/deployment.yaml`

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

> 📝 **Nota:** `initialDelaySeconds` usa `{{ .Values.probes.X.initialDelaySeconds }}`, NO valores hardcodeados. Así puedes ajustar tiempos por entorno.

#### 6.10 `helm/url-shortener/templates/service.yaml`

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

#### 6.11 `helm/url-shortener/templates/route.yaml`

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

#### 6.12 `helm/url-shortener/templates/cronjob.yaml`

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

#### 6.13 `helm/url-shortener/templates/postgresql.yaml`

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
  accessModes: [ReadWriteOnce]
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
          livenessProbe:
            exec:
              command: ["pg_isready", "-U", "{{ .Values.database.user }}"]
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            exec:
              command: ["pg_isready", "-U", "{{ .Values.database.user }}"]
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
{{- end }}
```

### ✅ Checkpoint

```bash
# Validar el chart
helm template url-shortener helm/url-shortener/

# Instalar en dev
helm install url-shortener helm/url-shortener/ -f helm/url-shortener/values-dev.yaml

# Instalar en pro
helm install url-shortener helm/url-shortener/ -f helm/url-shortener/values-pro.yaml

# Verificar
helm list
oc get pods
```

### 🧩 Retos de la Fase 6

**Reto 6.1:** Añade un Ingress template condicional (alternativa a Route para clusters no-OpenShift).

**Reto 6.2:** Crea un `values-staging.yaml` con configuración intermedia.

**Reto 6.3:** Modifica el CD workflow para usar `helm upgrade --install` en vez de `oc set image`.

---

## Fase 7: Deploy Final y Verificación

### 🎯 Objetivo
Desplegar todo en OpenShift Sandbox y verificar que funciona end-to-end.

### 📝 Tareas

1. Push final a `main`
2. Verificar que CI pasa (tests + build)
3. Verificar que CD despliega correctamente
4. Probar la app desde la URL pública
5. Verificar el CronJob

```bash
# Probar la app
ROUTE=$(oc get route url-shortener -o jsonpath='{.spec.host}')

# Crear URL corta
curl -X POST https://$ROUTE/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'

# Verificar redirect
curl -I https://$ROUTE/<short_code>

# Ver stats
curl https://$ROUTE/stats/<short_code>

# Listar todas
curl https://$ROUTE/urls

# Health checks
curl https://$ROUTE/health/live
curl https://$ROUTE/health/ready
```

### 🎉 ¡Felicidades!

Si todo funciona, has completado un proyecto DevOps completo:
- ✅ API Flask con tests
- ✅ Dockerfile multi-stage optimizado
- ✅ Manifiestos Kubernetes
- ✅ CI/CD con GitHub Actions
- ✅ Helm Chart parametrizable
- ✅ Desplegado en OpenShift
