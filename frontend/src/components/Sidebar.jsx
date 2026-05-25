import { Link, useLocation } from "react-router-dom";

function Sidebar() {
  const location = useLocation();

  const isActive = (path) => {
    if (path === "/" && location.pathname === "/") return true;
    if (path !== "/" && location.pathname.startsWith(path)) return true;
    return false;
  };

  return (
    <div className="w-64 bg-gray-900 text-white min-h-screen p-6">
      <h2 className="text-2xl font-bold mb-10 text-green-400">CarbonTrace</h2>

      <nav className="flex flex-col gap-2">
        <Link
          to="/"
          className={`px-4 py-3 rounded-lg transition-all ${
            isActive("/")
              ? "bg-green-600 text-white font-semibold"
              : "hover:bg-gray-800 text-gray-300"
          }`}
        >
          Dashboard
        </Link>

        <Link
          to="/upload"
          className={`px-4 py-3 rounded-lg transition-all ${
            isActive("/upload")
              ? "bg-green-600 text-white font-semibold"
              : "hover:bg-gray-800 text-gray-300"
          }`}
        >
          Upload Data
        </Link>

        <Link
          to="/reviews"
          className={`px-4 py-3 rounded-lg transition-all ${
            isActive("/reviews")
              ? "bg-green-600 text-white font-semibold"
              : "hover:bg-gray-800 text-gray-300"
          }`}
        >
          Review Queue
        </Link>
      </nav>
    </div>
  );
}

export default Sidebar;
