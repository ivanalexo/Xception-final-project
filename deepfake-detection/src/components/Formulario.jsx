import { useState, useEffect } from "react";
import usePredict from "../hooks/usePredict";
import Error from "./Error";

const Formulario = ({ setResponse, setLoading }) => {
  const [image, setImage] = useState(null);
  const [error, setError] = useState(false);
  const { postData, isLoadding, error: serverError, response } = usePredict();

  const handleImageChange = (e) => {
    e.preventDefault();
    const file = e.target.files[0];
    const reader = new FileReader();

    reader.onloadend = () => {
      const imageData = reader.result;
      setImage(imageData);
    };
    if (file) {
      reader.readAsDataURL(file);
    }
  };
  const handleSumit = async (e) => {
    e.preventDefault();
    console.log("LOADING: ", isLoadding);
    setLoading(isLoadding);
    console.log(image);
    const data = {
      image: image,
    };
    const response = await postData("http://127.0.0.1:5000/predict", data);
    if (serverError) {
      setError(serverError);
    }
    setError(false);
    setResponse(response);
  };

  return (
    <div className="md:w-1/2 lg:w-2/5 mx-5">
      <h2 className="font-black text-3xl text-center mb-5">Cargar Imagen</h2>
      <div className="bg-white shadow-md rounded-lg py-10 px-5 mb-10">
        {error && (
          <Error>
            <p>{serverError}</p>
          </Error>
        )}
        <div className="flex justify-center items-center mb-5">
          <label
            className="block text-gray-700 uppercase font-bold"
            htmlFor="image"
          >
            Imagen
          </label>
          <input
            id="image"
            className="border-2 w-full p-2 mt-2 placholder-gray-400 rounded-md"
            type="file"
            accept="image/*"
            onChange={handleImageChange}
          />
        </div>
        {image && (
          <img
            src={image}
            className="mb-5"
            alt="uploaded"
            style={{ maxWidth: "100%" }}
          />
        )}
        <button
          className={`${
            image ? "bg-indigo-600" : "bg-slate-600"
          } w-full p-3 text-white uppercase font-bold ${
            image ? "hover:bg-indigo-700" : "hover:bg-none"
          } cursor-pointer transition-all`}
          onClick={handleSumit}
          disabled={image ? false : true}
        >
          Predecir
        </button>
      </div>
    </div>
  );
};

export default Formulario;
