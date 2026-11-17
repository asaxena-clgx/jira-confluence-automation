import { createRoot } from "react-dom/client";

type RunStatus = "Passed" | "Failed" | "Pending approval";

const mockRuns: { id: string; phase: string; engineer: string; status: RunStatus }[] = [
  { id: "RUN-1041", phase: "Phase 1: Accounts", engineer: "A. Patel", status: "Pending approval" },
  { id: "RUN-1040", phase: "Phase 2: Orders", engineer: "J. Lee", status: "Passed" },
  { id: "RUN-1039", phase: "Phase 2: Invoices", engineer: "M. Chen", status: "Failed" },
];

function App() {
  return (
    <main style={{ fontFamily: "system-ui, sans-serif", margin: "2rem", maxWidth: 900 }}>
      <h1>Migration QA</h1>
      <p style={{ background: "#fff4cc", padding: "0.5rem", border: "1px solid #e0c200" }}>
        MOCK DATA: static placeholder, not connected to the API.
      </p>
      <button type="button" disabled>
        Trigger run (not wired yet)
      </button>
      <h2>Team runs</h2>
      <table style={{ borderCollapse: "collapse", width: "100%" }}>
        <thead>
          <tr>
            {["Run", "Phase", "Engineer", "Status"].map((h) => (
              <th key={h} style={{ textAlign: "left", borderBottom: "2px solid #333", padding: "0.4rem" }}>
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {mockRuns.map((r) => (
            <tr key={r.id}>
              <td style={{ padding: "0.4rem" }}>{r.id}</td>
              <td style={{ padding: "0.4rem" }}>{r.phase}</td>
              <td style={{ padding: "0.4rem" }}>{r.engineer}</td>
              <td style={{ padding: "0.4rem" }}>{r.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(<App />);
