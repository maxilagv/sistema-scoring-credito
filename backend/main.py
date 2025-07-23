from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from schemas import CreditInput, CreditScoreResponse, ErrorResponse
from scoring import predict_credit_score
from database import Base, engine, get_db
from models import CreditApplication
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Scoring de Crédito",
    description="API para evaluación de riesgo crediticio personalizado",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "Sistema de Scoring de Crédito API",
        "version": "1.0.0",
        "endpoints": {
            "score": "/score - POST - Calcular score de crédito",
            "health": "/health - GET - Estado del sistema"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "credit-scoring-api"}

@app.post("/score", response_model=CreditScoreResponse)
def calculate_credit_score(
    credit_data: CreditInput,
    db: Session = Depends(get_db)
):
    """
    Calcular el score de crédito basado en los datos del solicitante
    """
    try:
        logger.info(f"Processing credit score request for: {credit_data.name}")
        
        # Validate business rules
        if credit_data.monthly_expense >= credit_data.monthly_income:
            raise HTTPException(
                status_code=400,
                detail="Los gastos mensuales no pueden ser mayores o iguales a los ingresos"
            )
        
        if credit_data.age < 18:
            raise HTTPException(
                status_code=400,
                detail="El solicitante debe ser mayor de edad"
            )
        
        # Convert to dict for processing
        data_dict = credit_data.model_dump()
        
        # Calculate credit score
        score, risk_level, factors = predict_credit_score(data_dict)
        
        # Create explanation
        explanation = generate_explanation(credit_data.name, score, risk_level, factors)
        
        # Save to database (optional)
        try:
            db_application = CreditApplication(
                **data_dict,
                score=score,
                risk_level=risk_level
            )
            db.add(db_application)
            db.commit()
            logger.info(f"Saved application to database with ID: {db_application.id}")
        except Exception as db_error:
            logger.warning(f"Failed to save to database: {db_error}")
            # Continue without failing the request
        
        response = CreditScoreResponse(
            name=credit_data.name,
            risk_level=risk_level,
            score=score,
            explanation=explanation,
            factors=factors
        )
        
        logger.info(f"Credit score calculated: {score} ({risk_level}) for {credit_data.name}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing credit score: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al procesar la solicitud"
        )

def generate_explanation(name: str, score: int, risk_level: str, factors: dict) -> str:
    """Generate human-readable explanation of the credit score"""
    
    explanation = f"{name}: {risk_level} (score {score}/100)\n\n"
    
    if factors['positive']:
        explanation += "✅ Factores positivos:\n"
        for factor in factors['positive']:
            explanation += f"• {factor}\n"
        explanation += "\n"
    
    if factors['negative']:
        explanation += "⚠️ Factores de riesgo:\n"
        for factor in factors['negative']:
            explanation += f"• {factor}\n"
        explanation += "\n"
    
    if factors['neutral']:
        explanation += "ℹ️ Consideraciones adicionales:\n"
        for factor in factors['neutral']:
            explanation += f"• {factor}\n"
        explanation += "\n"
    
    # Add recommendations based on score
    if score <= 40:
        explanation += "💡 Recomendaciones:\n"
        explanation += "• Reducir el nivel de endeudamiento\n"
        explanation += "• Mejorar el historial de pagos\n"
        explanation += "• Aumentar los ingresos o reducir gastos\n"
    elif score <= 70:
        explanation += "💡 Sugerencias para mejorar:\n"
        explanation += "• Mantener un buen historial de pagos\n"
        explanation += "• Considerar reducir deudas existentes\n"
    else:
        explanation += "🎉 Excelente perfil crediticio. Mantener las buenas prácticas financieras."
    
    return explanation

@app.get("/applications", response_model=list)
def get_recent_applications(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get recent credit applications (for admin/monitoring purposes)"""
    try:
        applications = db.query(CreditApplication)\
            .order_by(CreditApplication.created_at.desc())\
            .limit(limit)\
            .all()
        
        return [
            {
                "id": app.id,
                "name": app.name,
                "score": app.score,
                "risk_level": app.risk_level,
                "created_at": app.created_at
            }
            for app in applications
        ]
    except Exception as e:
        logger.error(f"Error fetching applications: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching applications")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
