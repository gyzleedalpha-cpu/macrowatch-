# MacroWatch 🌍📊

Dashboard de noticias económicas globales — Fed, BOJ, SNB, Trump, Mercados.

## Deploy en Vercel (paso a paso)

### PASO 1 — Subir a GitHub

1. Andá a github.com → botón verde **"New"** → creá un repo llamado `macrowatch`
2. Marcá **"Public"**
3. Hacé click en **"uploading an existing file"**
4. Arrastrá estos 3 archivos/carpetas:
   - `index.html`
   - `vercel.json`
   - carpeta `api/` (con `chat.py` adentro)
5. Click **"Commit changes"**

### PASO 2 — Conectar con Vercel

1. Andá a **vercel.com** → "Sign up" con tu cuenta de GitHub
2. Click **"Add New Project"**
3. Seleccioná el repo `macrowatch`
4. Click **"Deploy"** (sin cambiar nada)

### PASO 3 — Agregar tu API Key (importante)

1. En Vercel, andá a tu proyecto → **Settings** → **Environment Variables**
2. Click **"Add New"**
3. Completá:
   - **Name:** `ANTHROPIC_API_KEY`
   - **Value:** tu clave (empieza con `sk-ant-...`)
4. Click **"Save"**
5. Andá a **Deployments** → click en los 3 puntos → **"Redeploy"**

### PASO 4 — Listo 🎉

Vercel te da una URL pública tipo:
`https://macrowatch-tuusuario.vercel.app`

Funciona desde cualquier dispositivo, celular incluido.

## Estructura del proyecto

```
macrowatch/
├── index.html        # Frontend del dashboard
├── vercel.json       # Configuración de Vercel
└── api/
    └── chat.py       # Servidor proxy (guarda tu API key segura)
```

## Costo

- Vercel: **gratis** (hobby plan)
- Anthropic API: ~$0.002 por actualización
