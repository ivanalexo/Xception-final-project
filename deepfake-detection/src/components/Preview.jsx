const Preview = ({ response, errorResponse, loading }) => {
  return (
    <div className="md:w-1/2 lg:w-3/5 md:h-screen overflow-y-scroll">
      {errorResponse && (
        <p className="text-lg mt-5 text-center">{errorResponse}</p>
      )}
      {response ? (
        <>
          <h2 className="font-black text-3xl text-center">Resultado</h2>
          <p className="text-lg mt-5 text-center">
            El proceso llegó a {""}
            <span className="text-indigo-600 font-bold">
              los siguientes resultados:
            </span>
            {response?.predictions.map((item, key) => {
              const value = parseFloat(item);
              const confidence = Number(value).toFixed(2) * 100;
              const label = value >= 0.5 ? "Real" : "Falsa";
              return (
                <p key={key}>
                  La imagen {key + 1} es {label} con una confianza de{" "}
                  {confidence}%
                </p>
              );
            })}
          </p>
          <div className="flex justify-center bg-white items-center shadow-md rounded-lg py-10 px-5 mb-10">
            <img
              className=" w-100"
              src={`data:image/jpeg;base64,${response?.image}`}
              alt="result"
            />
          </div>
        </>
      ) : (
        <>
          <h2 className="font-black text-3xl text-center">No hay datos</h2>
          <p className="text-lg mt-5 text-center">
            Los resultados {""}
            <span className="text-indigo-600 font-bold">apareceran aqui</span>
          </p>
        </>
      )}
      {loading && (
        <div>
          <p>LOADING...</p>
        </div>
      )}
    </div>
  );
};

export default Preview;
