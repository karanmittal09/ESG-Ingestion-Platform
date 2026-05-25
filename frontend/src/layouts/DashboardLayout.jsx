import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

function DashboardLayout({ children }) {
  return (
    <div className="flex">
      <Sidebar />

      <div className="flex-1 bg-gray-50 min-h-screen">
        <Navbar />

        <div className="p-8">{children}</div>
      </div>
    </div>
  );
}

export default DashboardLayout;
