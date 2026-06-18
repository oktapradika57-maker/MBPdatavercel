<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Genset Backup Time Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
</head>
<body class="bg-slate-900 text-slate-100 font-sans min-h-screen">

    <div class="max-w-7xl mx-auto p-6">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between border-b border-slate-800 pb-6 mb-8">
            <div>
                <h1 class="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
                    <i data-lucide="cpu" class="text-amber-500 w-8 h-8"></i>
                    Genset Backup Monitor
                </h1>
                <p class="text-slate-400 mt-1 text-sm">
                    Komparasi Durasi Nyata (Waktu Start/Stop) vs Running Hours (RH) Genset
                </p>
            </div>
            <button id="refreshBtn" class="mt-4 md:mt-0 inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium px-4 py-2 rounded-lg transition-colors text-sm cursor-pointer">
                <i data-lucide="refresh-cw" id="refreshIcon" class="w-4 h-4"></i>
                <span id="btnText">Refresh Data</span>
            </button>
        </div>

        <div id="errorAlert" class="hidden mb-6 bg-red-950/50 border border-red-500/50 rounded-xl p-4 text-red-200 text-sm flex items-start gap-3">
            <i data-lucide="alert-circle" class="w-5 h-5 text-red-400 flex-shrink-0"></i>
            <p id="errorText"></p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            <div class="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5 shadow-sm">
                <div class="flex items-center justify-between text-slate-400 mb-2">
                    <span class="text-sm font-medium">Total Kejadian Backup</span>
                    <i data-lucide="database" class="w-5 h-5 text-indigo-400"></i>
                </div>
                <div id="totalBackup" class="text-3xl font-bold text-white">-</div>
            </div>

            <div class="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5 shadow-sm">
                <div class="flex items-center justify-between text-slate-400 mb-2">
                    <span class="text-sm font-medium">Total Akumulasi Waktu Nyata</span>
                    <i data-lucide="clock" class="w-5 h-5 text-emerald-400"></i>
                </div>
                <div id="totalTimeDuration" class="text-3xl font-bold text-emerald-400">-</div>
            </div>

            <div class="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5 shadow-sm">
                <div class="flex items-center justify-between text-slate-400 mb-2">
                    <span class="text-sm font-medium">Total Akumulasi RH Genset</span>
                    <i data-lucide="gauge" class="w-5 h-5 text-amber-400"></i>
                </div>
                <div id="totalRhDuration" class="text-3xl font-bold text-amber-400">-</div>
            </div>
        </div>

        <div class="bg-slate-800/40 border border-slate-700/50 rounded-xl overflow-hidden shadow-lg">
            <div class="px-6 py-4 border-b border-slate-700/50 bg-slate-800/80">
                <h2 class="text-lg font-semibold text-white">Log Perhitungan & Komparasi Data</h2>
            </div>
            
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="bg-slate-800/50 text-xs font-semibold text-slate-300 uppercase tracking-wider border-b border-slate-700">
                            <th class="px-6 py-3">No</th>
                            <th class="px-6 py-3">Waktu Start / Stop</th>
                            <th class="px-6 py-3">Durasi Waktu Nyata</th>
                            <th class="px-6 py-3">RH Start / Stop</th>
                            <th class="px-6 py-3">Durasi RH</th>
                            <th class="px-6 py-3">Selisih (Discrepancy)</th>
                        </tr>
                    </thead>
                    <tbody id="tableBody" class="divide-y divide-slate-800">
                        <tr>
                            <td colspan="6" class="p-12 text-center text-slate-400">Mengambil data dari Google Sheets...</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        const SPREADSHEET_ID = "1CrupWIBU3NP49ORN3AxC6ave7SD01ds_odu7NVBOIoI";
        const csvUrl = `https://docs.google.com/spreadsheets/d/${SPREADSHEET_ID}/export?format=csv&gid=0`;

        function initIcons() {
            lucide.createIcons();
        }

        function calculateTimeDiffHours(startStr, endStr) {
            if (!startStr || !endStr) return 0;
            const start = new Date(startStr);
            const end = new Date(endStr);
            if (isNaN(start) || !isNaN(end)) {
                const diffMs = Math.abs(end - start);
                return diffMs / (1000 * 60 * 60); // Mengembalikan nilai dalam satuan Jam
            }
            return 0;
        }

        function fetchData() {
            document.getElementById('refreshIcon').classList.add('animate-spin');
            document.getElementById('btnText').innerText = "Loading...";

            Papa.parse(csvUrl, {
                download: true,
                header: true,
                skipEmptyLines: true,
                complete: function(results) {
                    const data = results.data;
                    renderDashboard(data);
                },
                error: function(err) {
                    console.error(err);
                    document.getElementById('errorText').innerText = "Gagal memuat spreadsheet. Pastikan opsi 'Anyone with link can view' sudah aktif.";
                    document.getElementById('errorAlert').classList.remove('hidden');
                    document.getElementById('refreshIcon').classList.remove('animate-spin');
                    document.getElementById('btnText').innerText = "Refresh Data";
                }
            });
        }

        function renderDashboard(rows) {
            const tableBody = document.getElementById('tableBody');
            tableBody.innerHTML = '';

            let sumTimeDuration = 0;
            let sumRhDuration = 0;
            let validRowsCount = 0;

            rows.forEach((row, index) => {
                // --- STANDARISASI KEY KOLOM SPREADSHEET ---
                // Kode ini otomatis mencari kolom yang namanya mirip/mengandung kata kunci tertentu
                const keys = Object.keys(row);
                
                const startBackupKey = keys.find(k => k.toLowerCase().includes('start') && k.toLowerCase().includes('backup')) || keys.find(k => k.toLowerCase().includes('start') && k.toLowerCase().includes('waktu')) || '';
                const stopBackupKey = keys.find(k => k.toLowerCase().includes('stop') && k.toLowerCase().includes('backup')) || keys.find(k => k.toLowerCase().includes('stop') && k.toLowerCase().includes('waktu')) || '';
                
                const rhStartKey = keys.find(k => k.toLowerCase().includes('rh') && k.toLowerCase().includes('start')) || keys.find(k => k.toLowerCase().includes('start') && k.toLowerCase().includes('rh')) || '';
                const rhStopKey = keys.find(k => k.toLowerCase().includes('rh') && k.toLowerCase().includes('stop')) || keys.find(k => k.toLowerCase().includes('stop') && k.toLowerCase().includes('rh')) || '';

                // Ambil value mentah
                const startVal = row[startBackupKey] || '';
                const stopVal = row[stopBackupKey] || '';
                const rhStartVal = parseFloat(row[rhStartKey]) || 0;
                const rhStopVal = parseFloat(row[rhStopKey]) || 0;

                // 1. Hitung Durasi Waktu Jam Nyata
                const timeDuration = calculateTimeDiffHours(startVal, stopVal);

                // 2. Hitung Durasi Running Hours
                const rhDuration = rhStopVal >= rhStartVal ? (rhStopVal - rhStartVal) : 0;

                // 3. Hitung Selisih Perbedaan Komparasi
                const discrepancy = Math.abs(timeDuration - rhDuration);

                // Akumulasi total jika baris datanya valid
                if(startVal || rhStartVal) {
                    sumTimeDuration += timeDuration;
                    sumRhDuration += rhDuration;
                    validRowsCount++;
                } else {
                    return; // Skip baris kosong jika ada
                }

                // Append ke tabel UI
                const tr = document.createElement('tr');
                tr.className = "hover:bg-slate-700/30 transition-colors text-sm";
                tr.innerHTML = `
                    <td class="px-6 py-4 text-slate-400 font-medium">${index + 1}</td>
                    <td class="px-6 py-4">
                        <div class="text-slate-200"><span class="text-xs text-slate-500">In:</span> ${startVal || '-'}</div>
                        <div class="text-slate-400"><span class="text-xs text-slate-500">Out:</span> ${stopVal || '-'}</div>
                    </td>
                    <td class="px-6 py-4 font-semibold text-slate-200">${timeDuration.toFixed(2)} Jam</td>
                    <td class="px-6 py-4">
                        <div class="text-slate-200"><span class="text-xs text-slate-500">Awal:</span> ${rhStartVal}</div>
                        <div class="text-slate-400"><span class="text-xs text-slate-500">Akhir:</span> ${rhStopVal}</div>
                    </td>
                    <td class="px-6 py-4 font-semibold text-slate-200">${rhDuration.toFixed(2)} Jam</td>
                    <td class="px-6 py-4">
                        <span class="px-2.5 py-1 rounded-full text-xs font-medium ${discrepancy > 0.5 ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'}">
                            ${discrepancy.toFixed(2)} Jam Selisih
                        </span>
                    </td>
                `;
                tableBody.appendChild(tr);
            });

            // Update Angka Summary Atas
            document.getElementById('totalBackup').innerText = validRowsCount;
            document.getElementById('totalTimeDuration').innerText = sumTimeDuration.toFixed(1) + " Jam";
            document.getElementById('totalRhDuration').innerText = sumRhDuration.toFixed(1) + " Jam";

            // Matikan Animasi Loading Button
            document.getElementById('refreshIcon').classList.remove('animate-spin');
            document.getElementById('btnText').innerText = "Refresh Data";
            initIcons();
        }

        // Event Listener & Run Pertama kali
        document.getElementById('refreshBtn').addEventListener('click', fetchData);
        window.addEventListener('DOMContentLoaded', () => {
            fetchData();
            initIcons();
        });
    </script>
</body>
</html>
