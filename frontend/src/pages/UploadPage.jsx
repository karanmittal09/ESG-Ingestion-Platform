import { useState } from "react";

import DashboardLayout from "../layouts/DashboardLayout";

import api from "../api/axios";

function UploadPage() {

  const [file, setFile] = useState(null);

  const [loading, setLoading] = useState(false);

  const [message, setMessage] = useState("");

  const [sourceType, setSourceType] = useState("SAP");

  const handleUpload = async () => {

    if (!file) {

      alert("Please select a file");

      return;
    }

    try {

      setLoading(true);

      const formData = new FormData();

      formData.append("file", file);

      formData.append("organization_id", 1);

      formData.append("uploaded_by", "karan");

      let endpoint = "";

      if (sourceType === "SAP") {

        endpoint = "/upload/sap/";
      }

      else if (sourceType === "UTILITY") {

        endpoint = "/upload/utility/";
      }

      else {

        endpoint = "/upload/travel/";
      }

      const response = await api.post(
        endpoint,
        formData,
        {
          headers: {
            "Content-Type":
              "multipart/form-data",
          },
        }
      );

      setMessage(response.data.message);

    } catch (error) {

      console.error(error);

      setMessage("Upload failed");

    } finally {

      setLoading(false);
    }
  };

  return (

    <DashboardLayout>

      <div>

        <h1 className="text-4xl font-bold mb-10 text-gray-900">
          Upload ESG Data
        </h1>

        <div className="bg-white p-10 rounded-2xl shadow max-w-2xl">

          <div className="mb-6">

            <label className="block text-sm font-semibold text-gray-700 mb-3">
              Select Data Source
            </label>

            <select
              value={sourceType}
              onChange={(e) => {
                setSourceType(e.target.value);
                setMessage("");
              }}
              className="w-full border-2 border-gray-200 rounded-lg p-4 focus:outline-none focus:border-green-500"
            >

              <option value="SAP">
                SAP Fuel / Procurement
              </option>

              <option value="UTILITY">
                Utility Electricity
              </option>

              <option value="TRAVEL">
                Corporate Travel
              </option>

            </select>

          </div>

          <div className="mb-8">

            <label className="block text-sm font-semibold text-gray-700 mb-3">
              Select CSV File
            </label>

            <input
              type="file"
              accept=".csv"
              onChange={(e) => {

                setFile(e.target.files[0]);

                setMessage("");

              }}
              className="w-full border-2 border-gray-200 rounded-lg p-4 focus:outline-none focus:border-green-500 transition-colors"
            />

            {
              file && (

                <p className="text-sm text-gray-600 mt-3">
                  📄 Selected: {file.name}
                </p>
              )
            }

          </div>

          <button
            onClick={handleUpload}
            disabled={loading || !file}
            className="w-full bg-green-700 hover:bg-green-800 active:bg-green-900 disabled:bg-gray-400 text-white px-6 py-4 rounded-lg font-semibold transition-colors text-lg"
          >

            {
              loading
                ? "Uploading..."
                : "Upload & Process"
            }

          </button>

          {
            message && (

              <p
                className={`mt-6 text-lg font-medium p-4 rounded-lg ${
                  message
                    .toLowerCase()
                    .includes("failed")
                    ? "bg-red-100 text-red-700"
                    : "bg-green-100 text-green-700"
                }`}
              >
                {message}
              </p>
            )
          }

        </div>

      </div>

    </DashboardLayout>
  );
}

export default UploadPage;