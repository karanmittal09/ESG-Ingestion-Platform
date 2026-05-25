import { useEffect, useState } from "react";
import DashboardLayout from "../layouts/DashboardLayout";
import Loader from "../components/Loader";
import api from "../api/axios";

function Dashboard() {
  const [stats, setStats] = useState({
    total_records: 0,
    suspicious_records: 0,
    approved_records: 0,
  });

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);

      const response = await api.get("/dashboard/stats/");

      setStats(response.data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardLayout>
      <div>
        <h1 className="text-4xl font-bold mb-10 text-gray-900">ESG Overview</h1>

        {loading ? (
          <Loader />
        ) : (
          <div className="grid grid-cols-3 gap-8">
            <div className="bg-white px-8 py-8 rounded-xl shadow hover:shadow-lg transition-shadow">
              <h2 className="text-gray-500 font-medium text-sm uppercase tracking-wide">
                Total Records
              </h2>

              <p className="text-5xl font-bold mt-4 text-gray-900">
                {stats.total_records}
              </p>
            </div>

            <div className="bg-white px-8 py-8 rounded-xl shadow hover:shadow-lg transition-shadow">
              <h2 className="text-gray-500 font-medium text-sm uppercase tracking-wide">
                Suspicious Records
              </h2>

              <p className="text-5xl font-bold mt-4 text-red-600">
                {stats.suspicious_records}
              </p>
            </div>

            <div className="bg-white px-8 py-8 rounded-xl shadow hover:shadow-lg transition-shadow">
              <h2 className="text-gray-500 font-medium text-sm uppercase tracking-wide">
                Approved Records
              </h2>

              <p className="text-5xl font-bold mt-4 text-green-600">
                {stats.approved_records}
              </p>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

export default Dashboard;
