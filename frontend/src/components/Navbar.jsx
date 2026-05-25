function Navbar() {
  return (
    <div className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-8 shadow-sm">
      <h1 className="text-2xl font-bold bg-gradient-to-r from-green-600 to-green-500 bg-clip-text text-transparent">
        ESG Ingestion Platform
      </h1>

      <div className="text-sm text-gray-500 font-medium">Analyst Dashboard</div>
    </div>
  );
}

export default Navbar;
