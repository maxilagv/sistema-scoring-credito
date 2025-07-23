#!/usr/bin/env python3
"""
Script to train the credit scoring model
Run this script to generate the initial model files
"""

from scoring import train_model
import sys

def main():
    print("🚀 Iniciando entrenamiento del modelo de scoring de crédito...")
    print("=" * 60)
    
    try:
        model, scaler = train_model()
        print("✅ Modelo entrenado exitosamente!")
        print("📁 Archivos generados:")
        print("   - credit_model.pkl (modelo de machine learning)")
        print("   - scaler.pkl (normalizador de características)")
        print("\n🎯 El modelo está listo para hacer predicciones de scoring de crédito.")
        
    except Exception as e:
        print(f"❌ Error durante el entrenamiento: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
