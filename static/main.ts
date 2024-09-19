// Search by Applicant Name
async function searchByApplicant() {
    const name = (document.getElementById('applicant-name') as HTMLInputElement).value;
    const status = (document.getElementById('applicant-status') as HTMLSelectElement).value;

    const response = await fetch(`/search/applicant?name=${name}&status=${status}`);
    const results = await response.json();
    displayResults(results);
}

// Search by Street Name
async function searchByStreet() {
    const streetName = (document.getElementById('street-name') as HTMLInputElement).value;

    const response = await fetch(`/search/street?address=${streetName}`);
    const results = await response.json();
    displayResults(results);
}

// Search by Latitude and Longitude
async function searchByLocation() {
    const latitude = (document.getElementById('latitude') as HTMLInputElement).value;
    const longitude = (document.getElementById('longitude') as HTMLInputElement).value;
    const allStatus = (document.getElementById('all-status') as HTMLInputElement).checked ? 'true' : 'false';

    const response = await fetch(`/search/location?latitude=${latitude}&longitude=${longitude}&all_status=${allStatus}`);
    const results = await response.json();
    displayResults(results);
}

// Function to display results
function displayResults(results: any[]) {
    const resultsDiv = document.getElementById('results');
    resultsDiv!.innerHTML = '';  // Clear previous results

    if (results.length === 0) {
        resultsDiv!.innerHTML = 'No results found';
        return;
    }

    results.forEach(result => {
        const div = document.createElement('div');
        div.className = 'result-item';
        div.innerHTML = `<strong>${result.applicant}</strong><br>Address: ${result.address}<br>Status: ${result.status}`;
        resultsDiv!.appendChild(div);
    });
}

// Function to clear displayed results and search boxes
function clearResults() {
    // Clear displayed results
    const resultsDiv = document.getElementById('results');
    resultsDiv!.innerHTML = '';

    // Clear input fields and select elements
    (document.getElementById('applicant-name') as HTMLInputElement).value = '';
    (document.getElementById('applicant-status') as HTMLSelectElement).selectedIndex = 0;

    (document.getElementById('street-name') as HTMLInputElement).value = '';

    (document.getElementById('latitude') as HTMLInputElement).value = '';
    (document.getElementById('longitude') as HTMLInputElement).value = '';
    
    (document.getElementById('all-status') as HTMLInputElement).checked = false;
}


// Event listeners for search and clear buttons
document.getElementById('search-applicant-btn')!.addEventListener('click', searchByApplicant);
document.getElementById('search-street-btn')!.addEventListener('click', searchByStreet);
document.getElementById('search-location-btn')!.addEventListener('click', searchByLocation);
document.getElementById('clear-results-btn')!.addEventListener('click', clearResults);
