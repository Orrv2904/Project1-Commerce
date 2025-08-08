# Commerce - Django Auctions Project

Un proyecto de subastas desarrollado con Django que permite a los usuarios crear listados, hacer ofertas y gestionar sus subastas.

## 🚀 Características

- ✅ Sistema de autenticación de usuarios
- ✅ Creación y gestión de listados de subastas
- ✅ Sistema de ofertas en tiempo real
- ✅ Watchlist personalizada
- ✅ Categorización de productos
- ✅ Sistema de comentarios
- ✅ Subida de imágenes a Cloudinary
- ✅ Interfaz moderna y responsive

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 5.2.5
- **Base de Datos**: PostgreSQL (producción) / SQLite (desarrollo)
- **Almacenamiento de Imágenes**: Cloudinary
- **Servidor Web**: Gunicorn
- **Servidor de Archivos Estáticos**: WhiteNoise

## 📋 Instalación Local

### Prerrequisitos

- Python 3.11+
- pip
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <tu-repositorio>
   cd Project1-Commerce
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv env
   env\Scripts\activate  # Windows
   source env/bin/activate  # Linux/Mac
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   Crea un archivo `.env` en la raíz del proyecto:
   ```
   SECRET_KEY=tu-secret-key-aqui
   CLOUDINARY_CLOUD_NAME=den3ccjvd
   CLOUDINARY_API_KEY=554688635689583
   CLOUDINARY_API_SECRET=adBQr8y2OHk3L6rqWKmFuQDkFy4
   ```

5. **Ejecutar migraciones**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Crear superusuario (opcional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Ejecutar el servidor**
   ```bash
   python manage.py runserver
   ```

8. **Abrir en el navegador**
   ```
   http://localhost:8000
   ```

## 🌐 Deployment en Render

### Configuración Automática

El proyecto está configurado para deployment automático en Render usando el archivo `render.yaml`.

### Variables de Entorno en Render

Configura las siguientes variables de entorno en tu dashboard de Render:

- `SECRET_KEY`: Clave secreta de Django (se genera automáticamente)
- `CLOUDINARY_CLOUD_NAME`: den3ccjvd
- `CLOUDINARY_API_KEY`: 554688635689583
- `CLOUDINARY_API_SECRET`: adBQr8y2OHk3L6rqWKmFuQDkFy4
- `DATABASE_URL`: URL de la base de datos PostgreSQL (se configura automáticamente)

### Pasos para Deployment

1. **Conectar con GitHub**
   - Ve a tu dashboard de Render
   - Conecta tu repositorio de GitHub

2. **Crear Web Service**
   - Selecciona tu repositorio
   - Render detectará automáticamente la configuración

3. **Configurar Build**
   - Build Command: `./build.sh`
   - Start Command: `gunicorn commerce.wsgi:application`

4. **Variables de Entorno**
   - Agrega las variables de entorno mencionadas arriba

5. **Deploy**
   - Render hará el deployment automáticamente

## 📁 Estructura del Proyecto

```
Project1-Commerce/
├── auctions/                 # App principal
│   ├── models.py            # Modelos de datos
│   ├── views.py             # Vistas de la aplicación
│   ├── urls.py              # URLs de la app
│   ├── form.py              # Formularios
│   └── templates/           # Templates HTML
├── commerce/                # Configuración del proyecto
│   ├── settings.py          # Configuración de desarrollo
│   ├── settings_production.py # Configuración de producción
│   └── urls.py              # URLs principales
├── static/                  # Archivos estáticos
├── media/                   # Archivos de media (local)
├── requirements.txt         # Dependencias
├── build.sh                # Script de build para Render
├── render.yaml             # Configuración de Render
└── manage.py               # Script de gestión de Django
```

## 🔧 Configuración de Cloudinary

El proyecto utiliza Cloudinary para el almacenamiento de imágenes. Las imágenes se suben automáticamente a la carpeta `media/images/project1/` en tu cuenta de Cloudinary.

### Configuración de Cloudinary

- **Cloud Name**: den3ccjvd
- **API Key**: 554688635689583
- **API Secret**: adBQr8y2OHk3L6rqWKmFuQDkFy4

## 🎯 Funcionalidades Principales

### Para Usuarios Registrados
- ✅ Crear nuevos listados de subastas
- ✅ Hacer ofertas en subastas activas
- ✅ Agregar/remover listados del watchlist
- ✅ Comentar en listados
- ✅ Ver mis listados ganados
- ✅ Cerrar subastas propias

### Para Visitantes
- ✅ Ver listados activos
- ✅ Filtrar por categorías
- ✅ Ver detalles de listados
- ✅ Registrarse/Iniciar sesión

## 🚨 Notas Importantes

- **Base de Datos**: En desarrollo usa SQLite, en producción PostgreSQL
- **Archivos Estáticos**: En producción se sirven con WhiteNoise
- **Imágenes**: Se almacenan en Cloudinary automáticamente
- **Seguridad**: Configuraciones de seguridad habilitadas en producción

## 📞 Soporte

Si tienes problemas con el deployment o necesitas ayuda, revisa:

1. Los logs de Render en tu dashboard
2. La configuración de variables de entorno
3. La conectividad con Cloudinary
4. Las migraciones de la base de datos

## 📄 Licencia

Este proyecto es de uso educativo y personal.
