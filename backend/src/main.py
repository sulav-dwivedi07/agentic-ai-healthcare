from agents.triage_agent import TriageAgent
from tools.search_engine import DoctorSearchEngine
from agents.booking_agent import BookingAgent


def run_agent():

    triage = TriageAgent()
    search_engine = DoctorSearchEngine()
    booking_agent = BookingAgent()

    print("🏥 Agentic AI Healthcare Assistant")
    print("----------------------------------")

    symptoms = input("Describe your symptoms: ")
    city = input("Enter your city: ")

    # Phase 1: Triage
    triage_result = triage.analyze(symptoms, city)

    urgency = triage_result["urgency"]
    specialty = triage_result["specialty"]

    print("\n🧠 Triage Result:")
    print(triage_result)

    # Phase 2: Real World Lookup
    doctors = search_engine.search(specialty, city, urgency)

    print("\n👨‍⚕️ Recommended Doctors:")

    if not doctors:
        print("No doctors found matching your condition.")
        return

    # Show doctors with numbering
    for index, doc in enumerate(doctors, start=1):
        print("----------------------------------")
        print(f"{index}. Doctor: {doc['name']}")
        print(f"   Hospital: {doc['hospital']}")
        print(f"   City: {doc['city']}")
        print(f"   Specialty: {doc['specialty']}")
        print(f"   Experience: {doc['experience_years']} years")
        print(f"   Rating: {doc['rating']} ⭐ ({doc['reviews']} reviews)")
        print(f"   Fees: ₹{doc['fees_inr']}")
        print(f"   Phone: {doc['phone']}")
        print(f"   Availability: {doc['availability']}")

    # Phase 3: Booking Option
    print("\n----------------------------------")
    choice = input("Enter doctor number to book appointment (or type 'no' to exit): ")

    if choice.lower() == "no":
        print("Thank you for using Healthcare Assistant.")
        return

    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(doctors):
        print("Invalid selection.")
        return

    selected_doctor = doctors[int(choice) - 1]

    patient_name = input("Enter your name for booking: ")

    confirmation = booking_agent.book(patient_name, selected_doctor)

    print("\n✅ Appointment Confirmed!")
    print("----------------------------------")
    print(f"Patient: {patient_name}")
    print(f"Doctor: {confirmation['doctor']}")
    print(f"Hospital: {confirmation['hospital']}")
    print(f"Date: {confirmation['date']}")
    print(f"Time: {confirmation['time']}")
    print("Status: Confirmed")
    print("----------------------------------")


# Important: Call the function
if __name__ == "__main__":
    run_agent()