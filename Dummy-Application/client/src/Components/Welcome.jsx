import { FaHandsClapping } from "react-icons/fa6";

const Welcome = () => {
  return (
    <div className="flex justify-start items-center gap-4 py-6">
      <p className="font-bold text-2xl text-gray-800 md:text-3xl lg:text-4xl">
        Welcome ,Jane
      </p>
      <FaHandsClapping className="text-2xl text-yellow-600 md:text-3xl lg:text-4xl" />
    </div>
  );
};

export default Welcome;
