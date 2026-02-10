import Table from "./components/Table";
import { Route, Routes } from "react-router-dom";
import AIdashboard from "./pages/AIdashboard";
import PolicyCreator from "./pages/PolicyCreator";

function App() {
    return (
        //<main className="w-screen h-screen">
        //  <Table />
        //</main>

        <Routes>
            <Route index element={<Table />} />
            <Route path="/ai-dashboard" element={<AIdashboard />} />
            <Route path="/policy-editor" element={<PolicyCreator />} />
        </Routes>
    );
}

export default App;
