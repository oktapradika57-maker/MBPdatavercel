"use client";

import { useState, useEffect } from "react";
import Papa from "papaparse";
import { Server, Database, RefreshCw, AlertCircle, CheckCircle } from "lucide-react";

export default function Dashboard() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Mengubah link Google Sheets biasa menjadi link download CSV direktori
  const SPREADSHEET_ID = "1CrupWIBU3NP49ORN3AxC6ave7SD01ds_odu7NVBOIoI";
  const GID = "0";
  const csvUrl = `https://docs.google.com/spreadsheets/d/${SPREADSHEET_ID}/export?format=csv&gid=${GID}`;

  const fetchData = () => {
    setLoading(true);
    Papa.parse(csvUrl, {
      download: true,
      header: true, // Menggunakan baris pertama spreadsheet sebagai nama kolom/key
      skipEmptyLines: true,
      complete: (results) => {
        setData(results.data);
        setLoading(false);
      },
      error: (err) => {
        console.error("Gagal mengambil data:", err);
        setError("Gagal memuat data dari Google Spreadsheet. Pastikan pengaturan share sudah 'Anyone with the link can view'.");
        setLoading(false);
      },
    });
  };

  useEffect(() => {
    fetchData();
  }, []);

  // --- LOGIKAL PERHITUNGAN BACKUP TIME ---
  // Catatan: Sesuaikan nama properti (misal: row["Nama Kolom"]) dengan header asli di file Google Sheets Anda.
  const totalSchedules = data.length;
  
  // Contoh kalkulasi: Menghitung rata-rata durasi backup (jika ada kolom durasi dalam menit)
  const totalDuration = data.reduce((acc, row) => {
    const duration = parseFloat(row["Durasi (Menit)"] || row["Duration"] || 0);
    return acc + (isNaN(duration) ? 0 : duration);
  }, 0);
  const avgDuration = totalSchedules > 0 ? (totalDuration / totalSchedules).toFixed(1) : 0;

  // Contoh status: Menghitung berapa backup yang sukses hari ini
  const successCount = data.filter(row => {
    const status = (row["Status"] || "").toLowerCase();
    return status === "success" || status === "berhasil" || status === "done";
  }).length;

  const failedCount = data.filter(row => {
    const status = (row["Status"] || "").toLowerCase();
    return status === "failed" || status === "gagal";
  }).length;

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-6 font-sans">
      {/* Header */}
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center md:justify-between border-b border-slate-800 pb-6 mb-8">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
            <Database className="text-indigo-400 w-8 h-8" />
            Backup Time Dashboard
          </h1>
          <p className="text-slate-400 mt-1 text-sm">
            Monitoring data waktu dan status backup terintegrasi dengan Google Spreadsheet
          </p>
        </div>
        <button
          onClick={fetchData}
          disabled={loading}
          className="mt-4 md:mt-0 inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium px-4 py-2 rounded-lg transition-colors text-sm disabled:opacity-50"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin" : ""}`} />
          {loading ? "Memuat..." : "Refresh Data"}
        </button>
      </div>

      <div className="max-w-7xl mx-auto">
        {error && (
          <div className="mb-6 bg-red-950/50 border border-red-500/50 rounded-xl p-4 text-red-200 text-sm flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
            <p>{error}</p>
          </div>
        )}

        {/* Info Cards / KPI Perhitungan */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5 shadow-sm">
            <div className="flex items-center justify-between text-slate-400 mb-2">
              <span className="text-sm font-medium">Total Jadwal Backup</span>
              <Server className="w-5 h-5 text-indigo-400" />
            </div>
            <div className="text-3xl font-bold text-white">{loading ? "..." : totalSchedules}</div>
            <p className="text-xs text-slate-400 mt-1">Item terdaftar</p>
          </div>

          <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5 shadow-sm">
            <div className="flex items-center justify-between text-slate-400 mb-2">
              <span className="text-sm font-medium">Rata-rata Durasi</span>
              <RefreshCw className="w-5 h-5 text-emerald-400" />
            </div>
            <div className="text-3xl font-bold text-white">{loading ? "..." : `${avgDuration} m`}</div>
            <p className="text-xs text-slate-400 mt-1">Per proses backup</p>
          </div>

          <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5 shadow-sm">
            <div className="flex items-center justify-between text-slate-400 mb-2">
              <span className="text-sm font-medium">Backup Sukses</span>
              <CheckCircle className="w-5 h-5 text-teal-400" />
            </div>
            <div className="text-3xl font-bold text-teal-400">{loading ? "..." : successCount}</div>
            <p className="text-xs text-slate-400 mt-1">Selesai dengan baik</p>
          </div>

          <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5 shadow-sm">
            <div className="flex items-center justify-between text-slate-400 mb-2">
              <span className="text-sm font-medium">Backup Gagal</span>
              <AlertCircle className="w-5 h-5 text-rose-400" />
            </div>
            <div className="text-3xl font-bold text-rose-400">{loading ? "..." : failedCount}</div>
            <p className="text-xs text-slate-400 mt-1">Butuh perhatian segera</p>
          </div>
        </div>

        {/* Tabel Data Mentah */}
        <div className="bg-slate-800/40 border border-slate-700/50 rounded-xl overflow-hidden shadow-lg">
          <div className="px-6 py-4 border-b border-slate-700/50 bg-slate-800/80">
            <h2 className="text-lg font-semibold text-white">Log Rincian Data Backup</h2>
          </div>
          
          <div className="overflow-x-auto">
            {loading ? (
              <div className="p-12 text-center text-slate-400 flex flex-col items-center justify-center gap-3">
                <RefreshCw className="w-8 h-8 animate-spin text-indigo-500" />
                <p>Mengunduh data terbaru dari Google Sheets...</p>
              </div>
            ) : data.length === 0 ? (
              <div className="p-12 text-center text-slate-400">
                Tidak ada data yang ditemukan atau format kolom tidak sesuai.
              </div>
            ) : (
              <table className="w-full text-left border-collapse">
                <thead>
                  <th className="px-6 py-3 bg-slate-800/20 text-xs font-semibold text-slate-300 uppercase tracking-wider border-b border-slate-700">No</th>
                  {Object.keys(data[0] || {}).map((header, index) => (
                    <th key={index} className="px-6 py-3 bg-slate-800/20 text-xs font-semibold text-slate-300 uppercase tracking-wider border-b border-slate-700">
                      {header}
                    </th>
                  ))}
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {data.map((row, rowIndex) => (
                    <tr key={rowIndex} className="hover:bg-slate-700/30 transition-colors">
                      <td className="px-6 py-4 text-sm text-slate-400">{rowIndex + 1}</td>
                      {Object.values(row).map((val, cellIndex) => (
                        <td key={cellIndex} className="px-6 py-4 text-sm text-slate-200">
                          {val}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
