import { useEffect, useState } from "react";

import DashboardLayout from "../layouts/DashboardLayout";

import Loader from "../components/Loader";

import api from "../api/axios";

function ReviewPage() {
  const [records, setRecords] = useState([]);

  const [loading, setLoading] = useState(false);

  const [initialLoading, setInitialLoading] = useState(true);

  useEffect(() => {
    fetchRecords();
  }, []);

  const fetchRecords = async () => {
    try {
      setInitialLoading(true);

      const response = await api.get("/emissions/review-queue/");

      setRecords(response.data);
    } catch (error) {
      console.error(error);
    } finally {
      setInitialLoading(false);
    }
  };

  const approveRecord = async (id) => {
    try {
      setLoading(true);

      await api.patch(`/emissions/${id}/approve/`);

      fetchRecords();
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const rejectRecord = async (id) => {
    try {
      setLoading(true);

      await api.patch(`/emissions/${id}/reject/`);

      fetchRecords();
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardLayout>
      <div>
        <div className="flex items-center justify-between mb-10">
          <h1 className="text-4xl font-bold text-gray-900">Review Queue</h1>

          <button
            onClick={() => {
              window.open("http://127.0.0.1:8000/api/emissions/export/");
            }}
            className="bg-green-700 hover:bg-green-800 active:bg-green-900 text-white px-6 py-3 rounded-lg font-medium transition-colors shadow-md hover:shadow-lg"
          >
            Export Audit Report
          </button>
        </div>

        {initialLoading ? (
          <div className="bg-white rounded-2xl shadow">
            <Loader />
          </div>
        ) : records.length === 0 ? (
          <div className="bg-white rounded-2xl shadow p-12 text-center">
            <div className="text-6xl mb-4">📋</div>
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">
              No Records to Review
            </h2>
            <p className="text-gray-500 text-lg">
              Great job! All records have been reviewed. Check back soon for new
              submissions.
            </p>
          </div>
        ) : (
          <div className="bg-white rounded-2xl shadow overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-100 border-b">
                <tr>
                  <th className="text-left px-6 py-4 font-semibold text-gray-700">
                    Source
                  </th>

                  <th className="text-left px-6 py-4 font-semibold text-gray-700">
                    Quantity
                  </th>

                  <th className="text-left px-6 py-4 font-semibold text-gray-700">
                    CO2e
                  </th>

                  <th className="text-left px-6 py-4 font-semibold text-gray-700">
                    Status
                  </th>

                  <th className="text-left px-6 py-4 font-semibold text-gray-700">
                    Actions
                  </th>
                </tr>
              </thead>

              <tbody>
                {records.map((record) => (
                  <tr
                    key={record.id}
                    className="border-t hover:bg-gray-50 transition-colors"
                  >
                    <td className="px-6 py-4 capitalize text-gray-900">
                      {record.source}
                    </td>

                    <td className="px-6 py-4 text-gray-900">
                      {record.quantity}
                    </td>

                    <td className="px-6 py-4 text-gray-900 font-semibold">
                      {record.co2e}
                    </td>

                    <td className="px-6 py-4">
                      <span
                        className={`px-3 py-1 rounded-full text-sm font-medium
                        ${
                          record.suspicious
                            ? "bg-red-100 text-red-700"
                            : record.status === "APPROVED"
                              ? "bg-green-100 text-green-700"
                              : record.status === "REJECTED"
                                ? "bg-gray-200 text-gray-700"
                                : "bg-yellow-100 text-yellow-700"
                        }`}
                      >
                        {record.suspicious ? "SUSPICIOUS" : record.status}
                      </span>
                    </td>

                    <td className="px-6 py-4 flex gap-3">
                      <button
                        onClick={() => approveRecord(record.id)}
                        disabled={loading}
                        className="bg-green-600 hover:bg-green-700 active:bg-green-800 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                      >
                        Approve
                      </button>

                      <button
                        onClick={() => rejectRecord(record.id)}
                        disabled={loading}
                        className="bg-red-600 hover:bg-red-700 active:bg-red-800 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
                      >
                        Reject
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}

export default ReviewPage;
