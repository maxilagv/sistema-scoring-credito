# 🚀 INSTRUCCIONES RÁPIDAS - Sistema de Scoring de Crédito

## 📦 ARCHIVO LISTO PARA DESCARGAR

✅ **Archivo ZIP creado**: `sistema-scoring-credito.zip`

Este archivo contiene TODO el proyecto completo y funcional.

---

## 🔧 INSTALACIÓN RÁPIDA

### 1️⃣ **Descargar y Extraer**
- Descarga el archivo `sistema-scoring-credito.zip`
- Extrae en tu computadora
- Abre la carpeta en VS Code

### 2️⃣ **Instalar Dependencias**

**Frontend (Next.js):**
```bash
npm install
```

**Backend (Python):**
```bash
cd backend
pip install -r requirements.txt
```

### 3️⃣ **Entrenar el Modelo (Solo la primera vez)**
```bash
cd backend
python train_model.py
```

### 4️⃣ **Ejecutar el Sistema**

**Opción A - Automático (Recomendado):**
```bash
cd backend
python start.py
```

**Opción B - Manual:**

Terminal 1 (Backend):
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 2 (Frontend):
```bash
npm run dev
```

---

## 🌐 ACCESO AL SISTEMA

- **Aplicación Web**: http://localhost:3000
- **API Backend**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

---

## 📋 LO QUE INCLUYE EL ZIP

### ✅ **Backend Python Completo**
- API REST con FastAPI
- Modelo de Machine Learning entrenado
- Base de datos SQLite
- Sistema de validación robusto

### ✅ **Frontend Next.js Completo**
- Interfaz moderna y responsive
- Formulario de evaluación crediticia
- Resultados detallados con explicaciones
- Diseño profesional con Tailwind CSS

### ✅ **Funcionalidades**
- Scoring de 0-100 puntos
- Clasificación de riesgo (Alto/Medio/Bajo)
- Análisis de 11+ variables financieras
- Explicaciones detalladas de factores
- Recomendaciones personalizadas

---

## 🎯 EJEMPLO DE USO

1. **Abrir**: http://localhost:3000
2. **Llenar formulario** con datos como:
   - Nombre: Juan Pérez
   - Edad: 35
   - Ingresos: $80,000
   - Gastos: $45,000
   - Estado civil: Casado
   - etc.
3. **Obtener resultado**: Score 84/100 (Bajo Riesgo)

---

## 🔍 VERIFICAR QUE TODO FUNCIONA

### Test rápido del backend:
```bash
curl http://localhost:8000/health
```
Debe responder: `{"status":"healthy","service":"credit-scoring-api"}`

### Test del frontend:
Abrir http://localhost:3000 - debe mostrar la página principal

---

## 📞 SOPORTE

Si tienes problemas:
1. Verificar que Node.js y Python estén instalados
2. Revisar que los puertos 3000 y 8000 estén libres
3. Consultar el README.md para más detalles

---

## 🎉 ¡LISTO PARA USAR!

El sistema está completamente funcional y listo para:
- Bancos y entidades financieras
- Fintechs y apps de microcrédito
- Evaluación de riesgo crediticio
- Desarrollo y personalización adicional

**¡Disfruta tu sistema de scoring de crédito profesional!** 🏦✨
