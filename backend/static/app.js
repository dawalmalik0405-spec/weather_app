const API_URL = "";

async function getWeather() {

    try {

        const location =
            document.getElementById("location").value;

        const startDate =
            document.getElementById("startDate").value;

        const endDate =
            document.getElementById("endDate").value;

        const url = window.currentEditId
            ? `/weather/${window.currentEditId}`
            : "/weather/";

        const method = window.currentEditId
            ? "PUT"
            : "POST";

        document.getElementById(
            "weatherResult"
        ).innerHTML = `
            <p>Loading weather data...</p>
        `;

        const response = await fetch(
            url,
            {
                method: method,
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    location: location,
                    start_date: startDate,
                    end_date: endDate
                })
            }
        );

        if (!response.ok) {

            const error =
                await response.json();

            throw new Error(
                error.detail
            );
        }

        const data = await response.json();


        document.getElementById(
            "editStatus"
        ).innerHTML = "";

        window.currentEditId = null;

        document.getElementById(
            "location"
        ).value = "";

        document.getElementById(
            "startDate"
        ).value = "";

        document.getElementById(
            "endDate"
        ).value = "";

        document.getElementById(
            "weatherButton"
        ).innerText = "Get Weather";

        displayWeather(data);

        loadRecords();

    } catch (error) {

        document.getElementById(
            "weatherResult"
        ).innerHTML = `
            <div
                style="
                    color:red;
                    font-weight:bold;
                "
            >
                ${error.message || "Something went wrong"}
            </div>
        `;
    }
}



function displayWeather(data) {

    let forecastHtml = "";

    data.forecast.forEach(day => {

        forecastHtml += `
            <li>
                ${day.date}
                -
                ${day.condition}
                -
                ${day.max_temp}°C /
                ${day.min_temp}°C
            </li>
        `;
    });

    document.getElementById(
        "weatherResult"
    ).innerHTML = `
        <h2>${data.location}</h2>

        <p>
            Temperature:
            ${data.current_weather.temperature}°C
        </p>

        <p>
            Humidity:
            ${data.current_weather.humidity}%
        </p>

        <h3>Location Map</h3>

        <div
            id="map"
            style="
                height:300px;
                margin-top:15px;
                border-radius:10px;
            "
        ></div>

        <h3>Forecast</h3>

        <ul>
            ${forecastHtml}
        </ul>
    `;

    if (window.weatherMap) {
        window.weatherMap.remove();
    }

    window.weatherMap = L.map(
        "map"
    ).setView(
        [
            data.latitude,
            data.longitude
        ],
        10
    );

    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            attribution:
                "&copy; OpenStreetMap contributors"
        }
    ).addTo(window.weatherMap);

    L.marker([
        data.latitude,
        data.longitude
    ])
    .addTo(window.weatherMap)
    .bindPopup(data.location)
    .openPopup();
}



async function loadRecords() {

    const response = await fetch(
        "/weather/"
    );

    const data = await response.json();

    let html = "";

    data.forEach(record => {

        html += `
            <div>
                <h3>${record.location}</h3>

                <p>
                    Temperature:
                    ${record.temperature}°C
                </p>

                <button onclick="viewRecord(${record.id})">
                    View
                </button>

                <button
                    onclick="deleteRecord(${record.id})"
                >
                    Delete
                </button>
                <button
                    onclick="editRecord(${record.id})"
                >
                    Edit
                </button>
            </div>
        `;
    });

    document.getElementById(
        "records"
    ).innerHTML = html;
}



async function deleteRecord(id) {

    await fetch(
        `/weather/${id}`,
        {
            method: "DELETE"
        }
    );

    document.getElementById(
        "recordDetails"
    ).style.display = "none";

    document.getElementById(
        "recordDetails"
    ).innerHTML = "";

    loadRecords();
}


function exportJson() {

    
    window.open(
        "/weather/export/json",
        "_blank"
    );
}

function exportCsv() {
    window.open(
        "/weather/export/csv",
        "_blank"
    );
}



async function editRecord(id) {

    const response = await fetch(
        `/weather/${id}`
    );

    const data = await response.json();

    document.getElementById("location").value =
        data.location;

    document.getElementById("startDate").value =
        data.start_date;

    document.getElementById("endDate").value =
        data.end_date;

    window.currentEditId = id;

    document.getElementById(
        "editStatus"
    ).innerHTML =
        `Editing Record #${id}`;

    document.getElementById(
        "weatherButton"
    ).innerText =
        "Update Weather";

}


async function viewRecord(id) {

    const detailsDiv =
        document.getElementById(
            "recordDetails"
        );

    if (
        detailsDiv.style.display === "block" &&
        detailsDiv.dataset.recordId == id
    ) {
        detailsDiv.style.display = "none";
        detailsDiv.innerHTML = "";
        detailsDiv.dataset.recordId = "";
        return;
    }

    const response = await fetch(
        `/weather/${id}`
    );

    const data = await response.json();

    let forecastHtml = "";

    data.forecast.forEach(day => {

        forecastHtml += `
            <li>
                ${day.forecast_date}
                -
                ${day.condition}
                -
                ${day.max_temp}°C /
                ${day.min_temp}°C
            </li>
        `;
    });

    detailsDiv.style.display = "block";
    detailsDiv.dataset.recordId = id;

    detailsDiv.innerHTML = `
        <h2>${data.location}</h2>

        <p>Temperature: ${data.temperature}°C</p>
        <p>Humidity: ${data.humidity}%</p>
        <p>Condition: ${data.weather_condition}</p>

        <p>Start Date: ${data.start_date}</p>
        <p>End Date: ${data.end_date}</p>

        <h3>Forecast</h3>

        <ul>
            ${forecastHtml}
        </ul>
    `;
}

loadRecords();



async function searchLocation() {

    const query =
        document.getElementById(
            "location"
        ).value;

    if (query.length < 2) {

        document.getElementById(
            "suggestions"
        ).innerHTML = "";

        return;
    }

    const response = await fetch(
        `/weather/search?query=${query}`
    );

    console.log(response.status);

    const data = await response.json();

    console.log(data);

    let html = "";

    data.forEach(place => {

        html += `
            <div
                onclick="selectLocation('${place.name}')"
                class="suggestion"
            >
                ${place.name}
                ${
                    place.country
                    ? `, ${place.country}`
                    : ""
                }
            </div>
        `;
    });

    document.getElementById(
        "suggestions"
    ).innerHTML = html;
}

function selectLocation(
    location
) {

    document.getElementById(
        "location"
    ).value = location;

    document.getElementById(
        "suggestions"
    ).innerHTML = "";
}