from fastapi import FastAPI
from pydantic import BaseModel
from src.agents.triage_agent import TriageAgent
from src.tools.search_engine import DoctorSearchEngine
from src.agents.booking_agent import BookingAgent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

triage = TriageAgent()
search_engine = DoctorSearchEngine()
booking_agent = BookingAgent()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------
# Request Models
# --------------------

class SymptomRequest(BaseModel):
    symptoms: str
    city: str


class BookingRequest(BaseModel):
    patient_name: str
    doctor: dict


# --------------------
# Routes
# --------------------

@app.post("/triage")
def triage_route(request: SymptomRequest):

    triage_result = triage.analyze(request.symptoms, request.city)

    doctors = search_engine.search(
        triage_result["specialty"],
        request.city,
        triage_result["urgency"]
    )

    return {
        "triage": triage_result,
        "doctors": doctors
    }


@app.post("/book")
def book_route(request: BookingRequest):

    confirmation = booking_agent.book(
        request.patient_name,
        request.doctor
    )

    return confirmation