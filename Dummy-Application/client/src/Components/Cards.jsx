const Cards = () => {
  return (
    <div className="gap-4 md:gap-6 grid grid-cols-3">
      <div className="flex flex-col gap-4 bg-purple-200 px-2 py-4 rounded-lg md:rounded-xl">
        <div className="">
          <p className="font-semibold text-gray-800 text-md md:text-lg">
            Complete Profile
          </p>
          <p className="font-normal text-gray-800 text-md md:text-lg">
            Get discovered by Clients.
          </p>
        </div>
        <div className="flex justify-end items-center px-2 py-2">
          <button className="bg-gray-800 px-2 md:px-4 py-2 rounded-full font-semibold text-white">
            Build Profile
          </button>
        </div>
      </div>

      {/* {2nd} */}
      <div className="flex flex-col gap-4 bg-green-200 px-2 py-4 rounded-lg md:rounded-xl">
        <div className="">
          <p className="font-semibold text-gray-800 text-md md:text-lg">
            Complete Profile
          </p>
          <p className="font-normal text-gray-800 text-md md:text-lg">
            Get discovered by Clients.
          </p>
        </div>
        <div className="flex justify-end items-center px-2 py-2">
          <button className="bg-gray-800 px-2 md:px-4 py-2 rounded-full font-semibold text-white">
            Browse Jobs
          </button>
        </div>
      </div>
      {/* {3rd } */}
      <div className="flex flex-col gap-4 bg-yellow-200 px-2 py-4 rounded-lg md:rounded-xl">
        <div className="">
          <p className="font-semibold text-gray-800 text-md md:text-lg">
            Complete Profile
          </p>
          <p className="font-normal text-gray-800 text-md md:text-lg">
            Get discovered by Clients.
          </p>
        </div>
        <div className="flex justify-end items-center px-2 py-2">
          <button className="bg-gray-800 px-2 md:px-4 py-2 rounded-full font-semibold text-white">
            Invite Client
          </button>
        </div>
      </div>
    </div>
  );
};

export default Cards;
