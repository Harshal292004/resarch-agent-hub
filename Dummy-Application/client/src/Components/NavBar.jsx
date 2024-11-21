import { NavLink } from "react-router-dom";
import { RiMessage2Fill } from "react-icons/ri";
import { FaBell, FaStar } from "react-icons/fa";
import { FcBusinessman } from "react-icons/fc";

const NavBar = () => {
  return (
    <nav className="flex justify-between items-center bg-white shadow-md px-6 py-3 text-blue-900">
      {/* Left Section - Dashboard Title */}
      <div>
        <p className="font-bold text-xl">Dashboard</p>
      </div>

      {/* Right Section - Navigation Links */}
      <ul className="flex items-center gap-6 md:gap-12">
        {/* Contra Pro */}
        <NavLink
          to="/"
          className="flex items-center gap-2 bg-blue-50 hover:bg-blue-100 px-4 py-2 border border-blue-900 rounded-full font-semibold text-blue-900 transition duration-300"
        >
          <li className="flex items-center">
            <span>Contra Pro</span>
            <FaStar className="text-yellow-500" />
          </li>
        </NavLink>

        {/* Messages */}
        <NavLink
          to="/messages"
          className="hover:text-blue-400 transition duration-300"
        >
          <li>
            <RiMessage2Fill className="text-blue-900 text-xl" />
          </li>
        </NavLink>

        {/* Notifications */}
        <NavLink
          to="/notifications"
          className="hover:text-blue-400 transition duration-300"
        >
          <li>
            <FaBell className="text-blue-900 text-xl" />
          </li>
        </NavLink>

        {/* Profile */}
        <NavLink
          to="/profile"
          className="hover:text-blue-400 transition duration-300"
        >
          <li>
            <FcBusinessman className="text-xl" />
          </li>
        </NavLink>
      </ul>
    </nav>
  );
};

export default NavBar;
