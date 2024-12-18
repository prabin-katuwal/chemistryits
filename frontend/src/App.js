import React from "react";
import "./index.css"; // Ensure Tailwind CSS is imported
import PeriodicTable from "./components/PeriodicTable";
import Quiz from "./components/Quize";

const App = () => {
  return (
    <div className="min-h-screen  px-32">
      <p className="text-center text-2xl my-10">Basic <strong>Periodic Table </strong><sub><small>(1-20)</small></sub> with Ontology</p>
      <PeriodicTable />
      <Quiz/>
    </div>
  );
};

export default App;
