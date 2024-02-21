import { useState } from "react";
import Formulario from "./components/Formulario";
import Header from "./components/Header";
import Preview from "./components/Preview";

function App() {
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  return (
    <div className="container mx-auto mt-20">
      <Header />
      <div className="mt-12 md:flex">
        <Formulario setResponse={setResponse} setLoading={setLoading} />
        <Preview response={response} loading={loading} />
      </div>
    </div>
  );
}

export default App;
