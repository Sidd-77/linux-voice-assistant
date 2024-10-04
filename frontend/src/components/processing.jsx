import React from "react";
import { Loader } from "lucide-react";
// import Lottie from "react-lottie";
// import animationData from "../assets/loading.json";
const ProcessingState = () => {
  // const defaultOptions = {
  //   loop: true,
  //   autoplay: true,
  //   animationData: animationData,
  //   rendererSettings: {
  //     preserveAspectRatio: "xMidYMid slice",
  //   },
  // };

  return (
    <div className="text-center">
      <div className="relative">
        {/* <Lottie options={defaultOptions} height={300} width={300} /> */}
        <Loader />
        <div className="absolute top-0 left-0 w-full h-full border-4 border-purple-300 rounded-full animate-pulse"></div>
      </div>
      <p className="mt-6 text-xl font-semibold text-gray-700">Processing...</p>
    </div>
  );
};

export default ProcessingState;
