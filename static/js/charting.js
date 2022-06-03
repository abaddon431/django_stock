// function to get django array(string), clean it and convert it into javascript array
function djangoArray(id)
{
    data_string = document.currentScript.getAttribute(id);
    const clean = data_string.replace(/[\])}[{(]/g,'');
    const data_set = clean.split(',');
    return data_set;
}

days_string = document.currentScript.getAttribute('days'); 
days_label =[]
for(let i = 0 ; i < parseInt(days_string);i++)
{
    days_label[i] = String(i)
}

const data_set = djangoArray('data_set');
const low_set = djangoArray('low_data');
const high_set = djangoArray('high_data');

const data = {
labels: days_label,
datasets: [{
    label: 'Investment Projection',
    fill: false,
    borderColor: '#616BFF',
    data: data_set,
    tension: 0
    },{    
    label: 'Low Projection',
    fill: false,
    borderColor: '#E52D2D',
    data: low_set,
    tension: 0,
    hidden: true,
    },{
    label: 'High Projection',
    fill: false,
    borderColor: '#49B049',
    data: high_set,
    tension: 0,
    hidden: true,
    }]
};

const config = {
type: 'line',
data: data,
options: {}
};

const myChart = new Chart(
    document.getElementById('line-chart'),
    config
);


