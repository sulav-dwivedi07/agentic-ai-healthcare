import { useState } from "react";

export default function App() {
  const [symptoms, setSymptoms] = useState("");
  const [city, setCity] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const analyzeSymptoms = async () => {
    if (!symptoms || !city) return alert("Please fill all fields");

    setLoading(true);

    // Add user message
    setMessages((prev) => [...prev, { type: "user", text: symptoms }]);

    try {
      const res = await fetch("http://127.0.0.1:8000/triage", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symptoms, city }),
      });

      const result = await res.json();

      // Add AI response
      setMessages((prev) => [
        ...prev,
        {
          type: "ai",
          triage: result.triage,
          doctors: result.doctors,
        },
      ]);
    } catch (err) {
      alert("Backend not reachable");
    }

    setLoading(false);
    setSymptoms("");
  };

  const bookDoctor = async (doctor) => {
    try {
      const res = await fetch("http://127.0.0.1:8000/book", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          patient_name: "Test Patient",
          doctor_name: doctor.name,
          specialty: doctor.specialty,
          hospital: doctor.hospital,
          city: city,
        }),
      });

      const result = await res.json();
      alert("Appointment Booked Successfully!");
      console.log("Booking response:", result);
    } catch (err) {
      console.log("Booking error:", err);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      {/* HEADER */}
      <div className="bg-blue-700 text-white p-4 text-center text-xl font-semibold shadow">
        🏥 Agentic AI Healthcare Assistant
      </div>

      {/* CHAT AREA */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4 max-w-3xl mx-auto w-full">
        {messages.map((msg, index) => (
          <div key={index}>
            {/* USER MESSAGE */}
            {msg.type === "user" && (
              <div className="flex justify-end">
                <div className="bg-blue-600 text-white px-4 py-2 rounded-2xl max-w-md">
                  {msg.text}
                </div>
              </div>
            )}

            {/* AI RESPONSE */}
            {msg.type === "ai" && (
              <div className="flex justify-start">
                <div className="bg-white shadow-md px-5 py-4 rounded-2xl max-w-xl w-full space-y-4">
                  {/* TRIAGE INFO */}
                  <div>
                    <p className="font-semibold text-lg">
                      🧠 Triage Assessment
                    </p>

                    <div
                      className={`mt-2 p-3 rounded-xl ${
                        msg.triage?.urgency === "emergency"
                          ? "bg-red-100 border border-red-400"
                          : "bg-green-100 border border-green-400"
                      }`}
                    >
                      <p>
                        <strong>Urgency:</strong> {msg.triage?.urgency}
                      </p>
                      <p>
                        <strong>Specialty:</strong> {msg.triage?.specialty}
                      </p>
                      <p className="text-sm text-gray-600 mt-1">
                        {msg.triage?.reasoning}
                      </p>
                    </div>
                  </div>

                  {/* DOCTORS */}
                  <div>
                    <p className="font-semibold">👨‍⚕️ Recommended Doctors</p>

                    {msg.doctors?.length === 0 && (
                      <p className="text-gray-500 text-sm mt-2">
                        No doctors found in your city.
                      </p>
                    )}

                    <div className="space-y-3 mt-2">
                      {msg.doctors?.map((doctor, i) => (
                        <div
                          key={i}
                          className="border rounded-xl p-3 flex justify-between items-center hover:shadow transition"
                        >
                          <div>
                            <p className="font-medium">{doctor.name}</p>
                            <p className="text-sm text-gray-500">
                              {doctor.specialty}
                            </p>
                            <p className="text-sm text-gray-500">
                              {doctor.hospital}
                            </p>
                          </div>

                          <button
                            onClick={() => bookDoctor(doctor)}
                            className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded-lg text-sm"
                          >
                            Book
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-white shadow px-4 py-2 rounded-2xl text-gray-500">
              Analyzing symptoms...
            </div>
          </div>
        )}
      </div>

      {/* INPUT AREA */}
      <div className="border-t bg-white p-4">
        <div className="max-w-3xl mx-auto flex gap-2">
          <input
            placeholder="Enter your city"
            className="border rounded-xl p-2 w-40"
            value={city}
            onChange={(e) => setCity(e.target.value)}
          />

          <input
            placeholder="Describe your symptoms..."
            className="flex-1 border rounded-xl p-2"
            value={symptoms}
            onChange={(e) => setSymptoms(e.target.value)}
          />

          <button
            onClick={analyzeSymptoms}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 rounded-xl"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
