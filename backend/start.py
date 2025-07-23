#!/usr/bin/env python3
"""
Startup script for the Credit Scoring API
This script will install dependencies, train the model, and start the server
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}:")
        print(f"   Comando: {command}")
        print(f"   Error: {e.stderr}")
        sys.exit(1)

def main():
    print("🚀 Iniciando Sistema de Scoring de Crédito")
    print("=" * 50)
    
    # Check if we're in the backend directory
    if not os.path.exists("requirements.txt"):
        print("❌ Error: Ejecutar desde el directorio backend/")
        print("   cd backend && python start.py")
        sys.exit(1)
    
    # Install dependencies
    run_command("pip install -r requirements.txt", "Instalando dependencias")
    
    # Train model if it doesn't exist
    if not os.path.exists("credit_model.pkl"):
        print("🤖 Modelo no encontrado, entrenando...")
        run_command("python train_model.py", "Entrenando modelo de ML")
    else:
        print("✅ Modelo existente encontrado")
    
    # Start the server
    print("\n🌐 Iniciando servidor FastAPI...")
    print("📍 API disponible en: http://localhost:8000")
    print("📖 Documentación en: http://localhost:8000/docs")
    print("\n⏹️  Presiona Ctrl+C para detener el servidor")
    print("=" * 50)
    
    try:
        subprocess.run("uvicorn main:app --reload --host 0.0.0.0 --port 8000", shell=True)
    except KeyboardInterrupt:
        print("\n👋 Servidor detenido")

if __name__ == "__main__":
    main()
