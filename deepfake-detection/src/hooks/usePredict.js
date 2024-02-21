import axios from "axios";
import { useState } from "react";
const usePredict = () => {
  const [isLoadding, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [response, setResponse] = useState(null);

  const postData = async (url, data) => {
    setIsLoading(true);
    try {
      const response = await axios.post(url, data);
      setResponse(response.data);
      return response.data;
    } catch (error) {
      setError(error.message);
    } finally {
      setIsLoading(false);
    }
  };
  return { response, error, isLoadding, postData };
};

export default usePredict;
