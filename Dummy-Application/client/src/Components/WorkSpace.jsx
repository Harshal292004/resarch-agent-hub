const WorkSpace = () => {
  return (
    <div className="flex md:flex-row flex-col border-gray-300 bg-gray-50 py-6 border-b">
      {/* Text Section */}
      <div className="mb-6 md:mb-0 w-full md:w-1/3">
        <p className="font-bold text-2xl text-gray-800 md:text-3xl leading-tight">
          Your all-in-one
        </p>
        <p className="mb-4 font-bold text-2xl text-gray-800 md:text-3xl leading-tight">
          Workspace
        </p>
        <p className="text-base text-gray-600 leading-relaxed">
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Corrupti
          optio similique, recusandae cum reprehenderit quos. Manage everything
          in one place.
        </p>
      </div>

      {/* Cards Section */}
      <div className="flex-1 gap-4 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3">
        {/* Card 1 */}
        <div className="flex flex-col justify-between border-gray-200 bg-white shadow-md hover:shadow-lg p-4 border rounded-lg transition duration-300">
          <p className="font-semibold text-gray-800 text-lg">Projects</p>
          <p className="mt-2 text-gray-600 text-sm">No new project updates</p>
        </div>

        {/* Card 2 */}
        <div className="flex flex-col justify-between border-gray-200 bg-white shadow-md hover:shadow-lg p-4 border rounded-lg transition duration-300">
          <p className="font-semibold text-gray-800 text-lg">Tasks</p>
          <p className="mt-2 text-gray-600 text-sm">No new task updates</p>
        </div>

        {/* Card 3 */}
        <div className="flex flex-col justify-between border-gray-200 bg-white shadow-md hover:shadow-lg p-4 border rounded-lg transition duration-300">
          <p className="font-semibold text-gray-800 text-lg">Messages</p>
          <p className="mt-2 text-gray-600 text-sm">No new messages</p>
        </div>
      </div>
    </div>
  );
};

export default WorkSpace;
