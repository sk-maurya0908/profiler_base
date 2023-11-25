//arrays of dictionaries
let basicData=[];
let educationData=[];
let workExperienceData=[];
let masterThesisData=[];
let courseProjectData=[];
let certificationsData=[];

//arrays of strings
let achievementsData=[];
let technicalSkillsData=[];
let extraCurricularData=[];
let hobbiesData=[];

// add a static table to take a single row of basic data 
function addbasicDetails() {
    const tableBody = document.getElementById('basicDetailsBody');
    const newRow = tableBody.insertRow();
    const rowData={};
    const keys=['name', 'rollNumber', 'departmentName', 'programName', 'gender'];

    for (let i = 0; i <keys.length; i++) {
        const cell = newRow.insertCell(i);
        const input = document.createElement('input');
        input.type = 'text';
        input.addEventListener('input', function() {
            // Update the value in the rowData array when the user inputs data
            rowData[keys[i]] = input.value;
        });
        cell.appendChild(input);
    }
    basicData.push(rowData);
}


//add new rows dynamically for education details
function addEduDetails() {
    const tableBody = document.getElementById('eduDetailsBody');
    const newRow = tableBody.insertRow();
    const rowData={};
    const keys=['exam','univ','insti','yop','cpi'];

   
    for (let i = 0; i <keys.length; i++) {
        const cell = newRow.insertCell(i);
        const input = document.createElement('input');
        input.type = i<3? 'text':'number'; // You can change the input type as needed
        input.addEventListener('input', function() {
            // Update the value in the rowData array when the user inputs data
            rowData[keys[i]] = input.value;
        });
        cell.appendChild(input);
    }
    educationData.push(rowData);
    // eduDetails
}

//add new rows dynamically for Work details
function addWorkDetails(){
    const tableBody = document.getElementById('workExperienceDetailsBody');
    const newRow = tableBody.insertRow();
    const rowData={};
    const keys=["workDesignation","workOrganisation","workRole","workProject","workProjectResponsibilities","workDate"];
    
    for (let i = 0; i <keys.length; i++) {
        const cell = newRow.insertCell(i);
        const input = document.createElement('input');
        input.type = 'text'; // You can change the input type as needed
        input.addEventListener('input', function() {
            // Update the value in the rowData array when the user inputs data
            rowData[keys[i]] = input.value;
        });
        cell.appendChild(input);
    }
    workExperienceData.push(rowData);
    // workDetails
}

//add new rows dynamically for MasterThesis details
function addMasterThesisDetails(){
    const tableBody = document.getElementById('masterThesisDetailsBody');
    const newRow = tableBody.insertRow();
    const rowData={};
    const keys=['projectTitle','projectName','projectDescription','projectGuide','projectCurrentWork','projectFutureWork','projectDate'];

   for (let i = 0; i <keys.length; i++) {
        const cell = newRow.insertCell(i);
        const input = document.createElement('input');
        input.type = 'text'; // You can change the input type as needed
        input.addEventListener('input', function() {
            // Update the value in the rowData array when the user inputs data
            rowData[keys[i]] = input.value;
        });
        cell.appendChild(input);
    }
    masterThesisData.push(rowData);
    // masterThesisDetails
}

//add new rows dynamically for CourseProject details
function addCourseProjectDetails(){
    const tableBody = document.getElementById('courseProjectDetailsBody');
    const newRow = tableBody.insertRow();
    const rowData={};
    const keys=['courseProjectTitle','courseProjectNameAndCode','courseProjectInstructorName','courseProjectDescription','courseProjectDate'];

    for (let i = 0; i <keys.length; i++) {
        const cell = newRow.insertCell(i);
        const input = document.createElement('input');
        input.type = 'text'; // You can change the input type as needed
        input.addEventListener('input', function() {
            // Update the value in the rowData array when the user inputs data
            rowData[keys[i]] = input.value;
        });
        cell.appendChild(input);
    }
    courseProjectData.push(rowData);
    // courseProjectDetails
}

//add new rows dynamically for Certifications details
function addCertificationsDetails(){
    const tableBody = document.getElementById('certificationsDetailsBody');
    const newRow = tableBody.insertRow();
    const rowData={};
    const keys=['certificationTitle','certifcationOfferedBy','certificationPlatform','certificationDate'];
    
    for (let i = 0; i <keys.length; i++) {
        const cell = newRow.insertCell(i);
        const input = document.createElement('input');
        input.type = 'text'; // You can change the input type as needed
        input.addEventListener('input', function() {
            // Update the value in the rowData array when the user inputs data
            rowData[keys[i]] = input.value;
        });
        cell.appendChild(input);
    }
    certificationsData.push(rowData);
}

//add new rows dynamically for Achievements details
function addAchievementsDetails(){
    const tableBody = document.getElementById('achievementsDetailsBody');
    const newRow = tableBody.insertRow();
    const rowData={};
    const keys='achievements';
    
    const cell = newRow.insertCell(0);
    const input = document.createElement('input');
    input.type = 'text'; // You can change the input type as needed
    input.addEventListener('input', function() {
            // Update the value in the rowData array when the user inputs data
            rowData[keys]= input.value;
        });
    cell.appendChild(input);
    
    achievementsData.push(rowData);
    
}

//add new rows dynamically for TechnicalSkills details
function addTechnicalSkillsDetails(){
    const tableBody = document.getElementById('technicalSkillsDetailsBody');
    const newRow = tableBody.insertRow();
    const rowData={};
    const keys='technicalSkills';
    
    const cell = newRow.insertCell(0);
    const input = document.createElement('input');
    input.type = 'text'; // You can change the input type as needed
    input.addEventListener('input', function() {
            // Update the value in the rowData array when the user inputs data
            rowData[keys]=input.value;
        });
    cell.appendChild(input);
    technicalSkillsData.push(rowData);
    
    // technicalSkillsDetails
}

//add new rows dynamically for ExtraCurricular details
function addExtraCurricularDetails(){
    const tableBody = document.getElementById('extraCurricularDetailsBody');
    const newRow = tableBody.insertRow();
    const rowData={};
    const keys='extraCurricular';
    
    const cell = newRow.insertCell(0);
    const input = document.createElement('input');
    input.type = 'text'; // You can change the input type as needed
    input.addEventListener('input', function() {
            // Update the value in the rowData array when the user inputs data
            rowData[keys]= input.value;
        });
    cell.appendChild(input);
    
    extraCurricularData.push(rowData);
}

//add new rows dynamically for hobbies details
function addHobbiesDetails(){
    const tableBody = document.getElementById('hobbiesDetailsBody');
    const newRow = tableBody.insertRow();
    const rowData={};
    const keys='hobbies';
    
    const cell = newRow.insertCell(0);
    const input = document.createElement('input');
    input.type = 'text'; // You can change the input type as needed
    input.addEventListener('input', function() {
            // Update the value in the rowData array when the user inputs data
            rowData[keys]= input.value;
        });
    cell.appendChild(input);
    hobbiesData.push(rowData);
    
}

//calling all the dynamic row adding functions once to add a single row to the form
//users can call these functions to add more rows as required
addbasicDetails();
addEduDetails();
addWorkDetails();
addMasterThesisDetails();
addCourseProjectDetails();
addCertificationsDetails();
addAchievementsDetails();
addTechnicalSkillsDetails();
addExtraCurricularDetails();
addHobbiesDetails();

//get all the data from the form and make a JSON obj and pass it to server
function getData() {
    //merging all the 10 different datas into one complete array
    let completeData={};
    completeData['basicData']=basicData;
    completeData['educationData']=educationData;
    completeData['workExperienceData']=workExperienceData;
    completeData['masterThesisData']=masterThesisData;
    completeData['courseProjectData']=courseProjectData;
    completeData['certificationsData']=certificationsData;
    completeData['achievementsData']=achievementsData;
    completeData['technicalSkillsData']=technicalSkillsData;
    completeData['extraCurricularData']=extraCurricularData;
    completeData['hobbiesData']=hobbiesData;
    console.log({ completeData });

    // Make a POST request to the server
    fetch('/details', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body:JSON.stringify({ completeData }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Server response:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

//logout the user without saving the changes
function logout(){
    fetch('/logout', {
            method: 'POST', // or 'POST' depending on your server setup
            credentials: 'same-origin', // Include cookies in the request if any
        })
        .then(response => {
            if (response.ok) {
                console.log('Logout successful');
                // Redirect or update UI as needed
            } else {
                console.error('Logout failed');
                // Handle failed logout, e.g., show an error message
            }
        })
        .catch(error => {
            console.error('Error during logout:', error);
            // Handle the error, e.g., show an error message
        });
}