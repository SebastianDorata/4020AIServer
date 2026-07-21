function createMacroChart(id, data){

    new Chart(
        document.getElementById(id),
        {

            type: "pie",

            plugins: [ChartDataLabels],

            data: {

                labels: [
                    "Protein",
                    "Carbohydrates",
                    "Fat"
                ],

                datasets: [
                    {
                        data: data
                    }
                ]

            },

            options: {

                responsive: true,

                plugins: {

                    legend: {
                        display: false
                    },


                    datalabels: {

                        color: "white",

                        font: {
                            weight: "bold",
                            size: 14
                        },


                        formatter: function(value, context){

                            let total =
                                context.dataset.data.reduce(
                                    (a,b)=>a+b
                                );


                            let percentage =
                                (
                                    value /
                                    total *
                                    100
                                ).toFixed(1);


                            return (
                                context.chart.data.labels[context.dataIndex]
                                + "\n"
                                + percentage
                                + "%"
                            );

                        }

                    }

                }

            }

        }
    );

}