document.addEventListener('DOMContentLoaded', ()=>{
    const options = {
        chart: {
            type: 'column'
        },
        title: {
            text: 'covid19 sdfsdg'
        }

    };
     $.get('covid19.csv', csv=>{
         options.data = {
             csv
         };
         Highcharts.chart('container', options);
     });
});