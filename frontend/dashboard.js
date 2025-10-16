const API_BASE = "http://localhost:5000";
async function api(endpoint) {
    const res = await fetch(API_BASE + endpoint);
    return res.json();
}

let filterStartDate = null;
let filterEndDate = null;

function getDateParams() {
  let params = [];
  if (filterStartDate) params.push(`start=${filterStartDate}`);
  if (filterEndDate) params.push(`end=${filterEndDate}`);
  return params.length ? `?${params.join("&")}` : "";
}

async function setDatePickerLimits() {
    const data = await api('/api/date_range');
    const startInput = document.getElementById('filterStart');
    const endInput = document.getElementById('filterEnd');
    if (data.min_date && data.max_date) {
        startInput.min = data.min_date;
        startInput.max = data.max_date;
        endInput.min = data.min_date;
        endInput.max = data.max_date;
        startInput.value = data.min_date;
        endInput.value = data.max_date;
        filterStartDate = data.min_date;
        filterEndDate = data.max_date;
    }
}

document.getElementById('filterBtn').onclick = function() {
  filterStartDate = document.getElementById('filterStart').value || null;
  filterEndDate = document.getElementById('filterEnd').value || null;
  drawKpis();
  tripsByDay();
  tripsPerHourByVendor();
  avgSpeedHourByVendor();
  tripsByVendor();
};

document.getElementById('clearDateBtn').onclick = function() {
    document.getElementById('filterStart').value = "2016-01-01";
    document.getElementById('filterEnd').value = "2016-06-30";
    filterStartDate = "2016-01-01";
    filterEndDate = "2016-06-30";
    drawKpis();
    tripsByDay();
    tripsPerHourByVendor();
    avgSpeedHourByVendor();
    tripsByVendor();
  };
  

function formatNumber(n) {
    if (n === null || n === undefined) return '-';
    return Number(n).toLocaleString();
}

async function drawKpis() {
    const dateParams = getDateParams();
    const kpisAll = await api(`/api/kpi${dateParams}`);
    const kpisV1 = await api(`/api/kpi?vendor=1${dateParams ? "&" + dateParams.slice(1) : ""}`);
    const kpisV2 = await api(`/api/kpi?vendor=2${dateParams ? "&" + dateParams.slice(1) : ""}`);

    document.getElementById('kpi-total-trips').innerHTML = `
      <div class="kpi-vendor-values">
        <span style="color:#1976D2;font-weight:bold;">${formatNumber(kpisV1.total_trips) || '-'}</span>
        <span style="color:#FFD600;font-weight:bold;">${formatNumber(kpisV2.total_trips) || '-'}</span>
      </div>
      <div class="kpi-total-value">
        Total Trips:<strong>${formatNumber(kpisAll.total_trips) || '-'}</strong>
      </div>
    `;

    document.getElementById('kpi-avg-distance').innerHTML = `
      <div class="kpi-vendor-values">
        <span style="color:#1976D2;font-weight:bold;">${(kpisV1.avg_distance || 0).toFixed(2)}</span>
        <span style="color:#FFD600;font-weight:bold;">${(kpisV2.avg_distance || 0).toFixed(2)}</span>
      </div>
      <div class="kpi-total-value">
        Total Avg Distance (km):<strong>${(kpisAll.avg_distance || 0).toFixed(2)}</strong>
      </div>
    `;

    document.getElementById('kpi-avg-duration').innerHTML = `
      <div class="kpi-vendor-values">
        <span style="color:#1976D2;font-weight:bold;">${(kpisV1.avg_duration || 0).toFixed(1)}</span>
        <span style="color:#FFD600;font-weight:bold;">${(kpisV2.avg_duration || 0).toFixed(1)}</span>
      </div>
      <div class="kpi-total-value">
        Total Avg Duration (min):<strong>${(kpisAll.avg_duration || 0).toFixed(1)}</strong>
      </div>
    `;

    document.getElementById('kpi-avg-passengers').innerHTML = `
      <div class="kpi-vendor-values">
        <span style="color:#1976D2;font-weight:bold;">${(kpisV1.avg_passengers || 0).toFixed(2)}</span>
        <span style="color:#FFD600;font-weight:bold;">${(kpisV2.avg_passengers || 0).toFixed(2)}</span>
      </div>
      <div class="kpi-total-value">
        Total Avg Passengers:<strong>${(kpisAll.avg_passengers || 0).toFixed(2)}</strong>
      </div>
    `;
}

// TRIP COUNT & PASSENGERS BY DAY (line chart)
async function tripsByDay() {
    const dateParams = getDateParams();
    const data = await api(`/api/trips_by_day${dateParams}`);
    const days = data.map(d => d.day);
    const trips = data.map(d => d.trip_count);
    const passengers = data.map(d => d.passenger_count);
    new Chart(document.getElementById('lineTripsByDay').getContext('2d'), {
        type: 'line',
        data: {
            labels: days,
            datasets: [
                { label: 'Trips', data: trips, borderColor: '#1976D2', backgroundColor: 'rgba(25,118,210,0.05)', fill: true },
                { label: 'Passengers', data: passengers, borderColor: '#FFA000', backgroundColor: 'rgba(255,160,0,0.06)', fill: true }
            ]
        },
        options: { interaction:{mode:'index',intersect:false}, scales: { x: {ticks:{maxTicksLimit:12}} } }
    });
}

// TRIP PER HOUR, BY VENDOR (bar chart)
async function tripsPerHourByVendor() {
    const dateParams = getDateParams();
    const raw = await api(`/api/trips_per_hour_by_vendor${dateParams}`);
    const hours = [...new Set(raw.map(r => r.hour))];
    const vendors = [...new Set(raw.map(r => r.vendor_id))];
    const dataMap = {};
    raw.forEach(r => {
        if (!dataMap[r.hour]) dataMap[r.hour] = {};
        dataMap[r.hour][r.vendor_id] = r.trip_count;
    });
    new Chart(document.getElementById('barTripsHourVendor').getContext('2d'), {
        type: 'bar',
        data: {
            labels: hours,
            datasets: vendors.map((v,i) => ({
                label: 'Vendor ' + v,
                data: hours.map(h => (dataMap[h][v]||0)),
                backgroundColor: i==0 ? '#1976D2':'#FFA000'
            }))
        },
        options: {plugins:{title:{display:true,text:'Trips per Hour (by Vendor)'}}, scales: { x:{stacked:true}, y:{stacked:true} } }
    });
}

// AVG SPEED PER HOUR, BY VENDOR (bar chart)
async function avgSpeedHourByVendor() {
    const dateParams = getDateParams();
    const raw = await api(`/api/avg_speed_by_hour_by_vendor${dateParams}`);
    const hours = [...new Set(raw.map(r => r.hour))];
    const vendors = [...new Set(raw.map(r => r.vendor_id))];
    const dataMap = {};
    raw.forEach(r => {
        if (!dataMap[r.hour]) dataMap[r.hour] = {};
        dataMap[r.hour][r.vendor_id] = r.avg_km_h;
    });
    new Chart(document.getElementById('barAvgSpeedHourVendor').getContext('2d'), {
        type: 'bar',
        data: {
            labels: hours,
            datasets: vendors.map((v,i) => ({
                label: 'Vendor ' + v,
                data: hours.map(h => (dataMap[h][v]||0)),
                backgroundColor: i==0 ? '#0288d1':'#f57c00'
            }))
        },
        options: {plugins:{title:{display:true,text:'Avg Speed (km/h) per Hour (by Vendor)'}}, scales: { x:{stacked:true}, y:{stacked:true} } }
    });
}

// TRIPS BY VENDOR (pie chart)
async function tripsByVendor() {
    const dateParams = getDateParams();
    const data = await api(`/api/trips_by_vendor${dateParams}`);
    new Chart(document.getElementById('pieVendorShare').getContext('2d'), {
        type: 'pie',
        data: {
            labels: data.map(d => 'Vendor ' + d.vendor_id),
            datasets: [{ data: data.map(d => d.trip_count), backgroundColor: ['#1976D2','#FFA000','#388E3C','#D32F2F'] }]
        },
        options: {plugins:{title:{display:true, text:'Trip Share by Vendor'}}}
    });
}

function renderTable(containerId, columns, data) {
    const maxRows = 20;
    let html = '<table class="dashboard-table"><thead><tr>';
    columns.forEach(col => html += `<th>${col}</th>`);
    html += '</tr></thead><tbody>';
    data.slice(0, maxRows).forEach(row => {
        html += '<tr>';
        columns.forEach(col => html += `<td>${row[col]}</td>`);
        html += '</tr>';
    });
    html += '</tbody></table>';
    document.getElementById(containerId).innerHTML = html;
}

// Initialize date pickers and dashboard on page load
window.onload = function() {
    setDatePickerLimits();
    drawKpis();
    tripsByDay();
    tripsPerHourByVendor();
    avgSpeedHourByVendor();
    tripsByVendor();
};
