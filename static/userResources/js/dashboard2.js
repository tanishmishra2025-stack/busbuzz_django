//[Dashboard Javascript]

//Project:	EmployX - Responsive Admin Template
//Primary use:   Used only for the main dashboard (index.html)


var options = {
          series: [{
          name: 'New Ticket',
          type: 'line',
          data: [49, 62, 55, 67, 73, 110, 120, 115, 129, 123, 133]
        }, {
          name: 'Ticket Solved',
          type: 'line',
          data: [62, 76, 67, 49, 63, 70, 37, 52, 44, 61, 43]
        },],
          chart: {
            toolbar: { show: false,},
            height: 310,
            type: 'line',
        },

        stroke: {
           width: [2, 2],
          curve: 'smooth'
        },
        fill: {
          type:'solid',
          opacity: [1, 0.8],
        },
        labels: ['Jan', 'Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
        markers: {
          size: 0
        },
        legend: {
            show: false,
        },
        colors:[ '#FF6C6C', '#04a08b'],
        yaxis: [
          {
            title: {
              text: ' ',
            },
          },
          {
            opposite: true,
            title: {
              text: ' ',
            },
          },
        ],
        tooltip: {
          shared: true,
          intersect: false,
          y: {
            formatter: function (y) {
              if(typeof y !== "undefined") {
                return  y.toFixed(0) + " points";
              }
              return y;
            }
          }
        }
        };

        var chart = new ApexCharts(document.querySelector("#balance_overview"), options);
        chart.render();



    // ----------Shifts Overview-----//
    var option = {
        labels: ["Sales", "Setup", "Refund"],
        series: [45, 40, 15],
        chart: {
            type: "donut",
            height: 210,
        },
        dataLabels: {
            enabled: false,
        },
        legend: {
            show: false,
        },
        stroke: {
            width: 3,
        },
        plotOptions: {
            pie: {
                expandOnClick: false,
                donut: {
                    size: "70%",
                    labels: {
                        show: true,
                        name: {
                            offsetY: 0,
                        },
                        total: {
                            show: true,
                            fontSize: "20px",
                            fontWeight: 600,
                            label: "$ 34,098",
                            formatter: () => "Ticket",
                        },
                    },
                },
            },
        },
        states: {
            normal: {
                filter: {
                    type: "none",
                },
            },
            hover: {
                filter: {
                    type: "none",
                },
            },
            active: {
                allowMultipleDataPointsSelection: false,
                filter: {
                    type: "none",
                },
            },
        },
        colors: ["#0d6efd", "#dc3545", "#0dcaf0"],
    };

    var chart = new ApexCharts(
        document.querySelector("#shifts-overview"),
        option
    );
    chart.render();



var options = {
          series: [50, 80],
          chart: {
          height: 210,
          type: 'radialBar',
        },
        plotOptions: {
          radialBar: {
            dataLabels: {
              name: {
                fontSize: '22px',
              },
              value: {
                fontSize: '16px',
              },

              total: {
                show: true,
                label: 'Total',
                formatter: function (w) {
                  // By default this function returns the average of all series. The below is just an example to show the use of custom formatter function
                  return 249
                }
              }
            }
          }
        },
        colors: ["#3762EA", "#04a08b"],
        labels: ['New', 'Returned'],
        };

        var chart = new ApexCharts(document.querySelector("#chart-redio"), options);
        chart.render();



         var options = {
          series: [{
          name: 'series1',
          data: [90, 60, 45, 40, 65, 52, 41]
        }, {
          name: 'series2',
          data: [50, 40, 55, 100, 42, 80, 60]
        }],
          chart: {
          height: 290,
          type: 'area',
          toolbar: {
            show: false,
            },
            offsetY: 30,
        },
        colors: ["#0dcaf0", "#fd7e14"],
        fill: {
          colors: ["#0dcaf0", "#fd7e14"],
          type: "gradient",
          gradient: {
            shade: "light",
            type: "vertical",
            shadeIntensity: 0.4,
            inverseColors: false,
            opacityFrom: 0.9,
            opacityTo: 0.5,
            stops: [0, 100],
          },
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
        width: [2, 2],
          curve: 'smooth'
        },
        grid: {
          show: false,
          padding: {
            left: -10,
            top: -25,
            right: -60,
          },
        },
        xaxis: {
          type: 'datetime',
          categories: ["2018-09-19T00:00:00.000Z", "2018-09-19T01:30:00.000Z", "2018-09-19T02:30:00.000Z", "2018-09-19T03:30:00.000Z", "2018-09-19T04:30:00.000Z", "2018-09-19T05:30:00.000Z", "2018-09-19T06:30:00.000Z"]
        },
        legend: {
            show: false,
        },
        tooltip: {
          x: {
            format: 'dd/MM/yy HH:mm'
          },
        },
        yaxis: {
          axisBorder: {
            show: false
          },
          axisTicks: {
            show: false,
          },
          labels: {
            show: false,
            formatter: function (val) {
              return val + "%";
            }
          },
        },
        xaxis: {
          axisBorder: {
            show: false
          },
          axisTicks: {
            show: false,
          },
          labels: {
            show: false,
          },
        },
        };

        var chart = new ApexCharts(document.querySelector("#chart-58"), options);
        chart.render();


          var options = {
          series: [{
          name: 'Online Sales',
          data: [44, 55, 57, 56, 61, 58, 63, 60, 66]
        }, {
          name: 'Offline Sales',
          data: [76, 85, 101, 98, 87, 105, 91, 114, 94]
        }],
          chart: {
          type: 'bar',
          height: 320,
          offsetX: -15,
          offsetY: 15,
        },
        plotOptions: {
          bar: {
            horizontal: false,
            columnWidth: '55%',
            endingShape: 'rounded'
          },
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          show: true,
          width: 2,
          colors: ['transparent']
        },
        xaxis: {
          categories: ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'],
        },
        yaxis: {
          title: {
            text: ''
          }
        },
        fill: {
          opacity: 1
        },
        tooltip: {
          y: {
            formatter: function (val) {
              return "$ " + val + " thousands"
            }
          }
        }
        };

        var chart = new ApexCharts(document.querySelector("#revenue-chart"), options);
        chart.render();




$(function () {

  'use strict';
	
	  Morris.Donut({
        element: 'donut-chart',
        height: 100,
        data: [{
            label: "Male",
            value: 45,

        }, {
            label: "Female",
            value: 55,
        }],
        resize: true,
        colors:['#4d7cff', '#51ce8a']
    });
	
	

	
		var options = {
		  chart: {
			height: 150,
			width: 150,
			type: "radialBar"
		  },

		  series: [60],
			colors: ['#4d7cff'],
		  plotOptions: {
			radialBar: {
			  hollow: {
				margin: 0,
				size: "60%"
			  },
			  track: {
				background: '#e6f0ff',
			  },

			  dataLabels: {
				showOn: "always",
				name: {
				  show: false,
				},
				 grid: {
			      show: true,
			      padding: {
			        top: 10,
			        bottom: 10,
			        right: 30,
			        left: 20
			      }
			    },
				value: {
				  offsetY: 0,
				  color: "#111",
				  fontSize: "20px",
				  show: true
				}
			  }
			}
		  },

		  stroke: {
			lineCap: "round",
		  },
		  labels: ["Progress"]
		};

		var chart = new ApexCharts(document.querySelector("#revenue1"), options);

		chart.render();

		var options = {
		  chart: {
			height: 150,
			width: 150,
			type: "radialBar"
		  },

		  series: [50],
			colors: ['#51ce8a'],
		  plotOptions: {
			radialBar: {
			  hollow: {
				margin: 0,
				size: "60%"
			  },
			  track: {
				background: '#defded',
			  },
			  grid: {
			      show: true,
			      padding: {
			        top: 30,
			        bottom: 10,
			        right: 30,
			        left: 20
			      }
			    },

			  dataLabels: {
				showOn: "always",
				name: {
				  show: false,
				},
				value: {
				  offsetY: 0,
				  color: "#111",
				  fontSize: "20px",
				  show: true
				}
			  }
			}
		  },

		  stroke: {
			lineCap: "round",
		  },
		  labels: ["Progress"]
		};

		var chart = new ApexCharts(document.querySelector("#revenue2"), options);

		chart.render();

		var options = {
		  chart: {
			height: 150,
			width: 150,
			type: "radialBar"
		  },

		  series: [34],
			colors: ['#733aeb'],
		  plotOptions: {
			radialBar: {
			  hollow: {
				margin: 0,
				size: "60%"
			  },
			  track: {
				background: '#f4efff',
			  },
			  grid: {
			      show: true,
			      padding: {
			        top: 10,
			        bottom: 10,
			        right: 30,
			        left: 20
			      }
			    },

			  dataLabels: {
				showOn: "always",
				name: {
				  show: false,
				},
				value: {
				  offsetY: 0,
				  color: "#111",
				  fontSize: "20px",
				  show: true
				}
			  }
			}
		  },

		  stroke: {
			lineCap: "round",
		  },
		  labels: ["Progress"]
		};

		var chart = new ApexCharts(document.querySelector("#revenue3"), options);

		chart.render();

		
	
		var options = {
          series: [{
          data: [47, 45, 54, 38, 56, 24, 65, 31, 37, 39, 62, 51, 35, 41, 35, 27, 93, 53, 61, 27, 54, 43, 19, 46]
        }],
          chart: {
          type: 'area',
          height: 100,
          sparkline: {
            enabled: true
          },
        },
        stroke: {
          curve: 'smooth',
			width: 2,
        },
        fill: {
          opacity: 1,
        },
        yaxis: {
          min: 0
        },
        colors: ['#51ce8a'],
        };

        var chart = new ApexCharts(document.querySelector("#followers-spark"), options);
        chart.render();
	
	
		
	
		var options = {
          series: [{
          data: [51, 35, 41, 35, 27, 93, 53, 61, 27, 54, 43, 19, 46, 47, 45, 54, 38, 56, 24, 65, 31, 37, 39, 62]
        }],
          chart: {
          type: 'area',
          height: 100,
          sparkline: {
            enabled: true
          },
        },
        stroke: {
          curve: 'smooth',
			width: 2,
        },
        fill: {
          opacity: 1,
        },
        yaxis: {
          min: 0
        },
        colors: ['#4d7cff'],
        };

        var chart = new ApexCharts(document.querySelector("#growth-spark"), options);
        chart.render();
	
		
	
		var options = {
          series: [{
          data: [47, 45, 27, 93, 53, 61, 27, 54, 43, 19, 46, 54, 38, 56, 24, 65, 31, 37, 39, 62, 51, 35, 41, 35]
        }],
          chart: {
          type: 'area',
          height: 100,
          sparkline: {
            enabled: true
          },
        },
        stroke: {
          curve: 'smooth',
			width: 2,
        },
        fill: {
          opacity: 1,
        },
        yaxis: {
          min: 0
        },
        colors: ['#733aeb'],
        };

        var chart = new ApexCharts(document.querySelector("#post-spark"), options);
        chart.render();
	
	
		
	
		var options = {
          series: [{
          data: [51, 35, 41, 35, 27, 45, 54, 38, 56, 24, 65, 31, 37, 39, 62, 93, 53, 61, 27, 54, 43, 19, 46, 47]
        }],
          chart: {
          type: 'area',
          height: 100,
          sparkline: {
            enabled: true
          },
        },
        stroke: {
          curve: 'smooth',
			width: 2,
        },
        fill: {
          opacity: 1,
        },
        yaxis: {
          min: 0
        },
        colors: ['#fec801'],
        };

        var chart = new ApexCharts(document.querySelector("#interactions-spark"), options);
        chart.render();
	
	
		var options = {
          series: [41, 17, 15],
          chart: {
			 width: 300,
          type: 'donut',
        },
		 legend: {
			show: false, 
		 },
		dataLabels: {
  			enabled: false,
		},
		colors: ['#4d7cff', '#51ce8a', '#733aeb'],
		responsive: [{
          breakpoint: 1500,
          options: {
            chart: {
              width: 250
            }
          }
        }]	
		
        };
		
        var chart = new ApexCharts(document.querySelector("#revenue7"), options);
        chart.render();
	
	
		 $('.application-bx').slimScroll({
			height: '382px'
		  });
	
	
}); // End of use strict


		var options = {
          series: [{
			name: "Applications",
			data: [15, 35, 50, 23, 30, 90]
		  },
		  {
			name: "Shortlisted",
			data: [0, 48, 75, 35, 36, 70]
		  }],
          chart: {
          height: 335,
          type: 'area',
          toolbar: {
            show: false
          },
          zoom: {
            enabled: false
          }
        },
		colors: ['#51ce8a', '#733aeb'],
        dataLabels: {
          enabled: false
        },
		 legend: {
			show: false,
		 },
        stroke: {
          curve: 'smooth'
        },
        xaxis: {
          categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        },
        };

        var chart = new ApexCharts(document.querySelector("#active-jobs-chart"), options);
        chart.render();
	
		// check if the checkbox has any unchecked item
		checkLegends()

		function checkLegends() {
		  var allLegends = document.querySelectorAll(".legend input[type='checkbox']")

		  for(var i = 0; i < allLegends.length; i++) {
			if(!allLegends[i].checked) {
			  chart.toggleSeries(allLegends[i].value)
			}
		  }
		}

		// toggleSeries accepts a single argument which should match the series name you're trying to toggle
		function toggleSeries(checkbox) {
		  chart.toggleSeries(checkbox.value)
		}
	

	 $(function () {
    /* jQueryKnob */

    $(".knob").knob({
      /*change : function (value) {
       //console.log("change : " + value);
       },
       release : function (value) {
       console.log("release : " + value);
       },
       cancel : function () {
       console.log("cancel : " + this.value);
       },*/
      draw: function () {

        // "tron" case
        if (this.$.data('skin') == 'tron') {

          var a = this.angle(this.cv)  // Angle
              , sa = this.startAngle   // Previous start angle
              , sat = this.startAngle  // Start angle
              , ea                     // Previous end angle
              , eat = sat + a          // End angle
              , r = true;

          this.g.lineWidth = this.lineWidth;

          this.o.cursor
          && (sat = eat - 0.3)
          && (eat = eat + 0.3);

          if (this.o.displayPrevious) {
            ea = this.startAngle + this.angle(this.value);
            this.o.cursor
            && (sa = ea - 0.3)
            && (ea = ea + 0.3);
            this.g.beginPath();
            this.g.strokeStyle = this.previousColor;
            this.g.arc(this.xy, this.xy, this.radius - this.lineWidth, sa, ea, false);
            this.g.stroke();
          }

          this.g.beginPath();
          this.g.strokeStyle = r ? this.o.fgColor : this.fgColor;
          this.g.arc(this.xy, this.xy, this.radius - this.lineWidth, sat, eat, false);
          this.g.stroke();

          this.g.lineWidth = 2;
          this.g.beginPath();
          this.g.strokeStyle = this.o.fgColor;
          this.g.arc(this.xy, this.xy, this.radius - this.lineWidth + 1 + this.lineWidth * 2 / 3, 0, 2 * Math.PI, false);
          this.g.stroke();

          return false;
        }
      }
    });
  });
    /* END JQUERY KNOB */


      var options = {
        series: [{
          name: 'series1',
          data: [178, 223, 195, 201, 143, 189, 156, 155, 118, 167, 159]
        }],
        chart: {
		  foreColor: '#ffffff',
          height: 250,
          type: 'line',
			offsetY: -10,
			offsetX: -10,
        },
		colors:['#ffffff'],
        dataLabels: {
          enabled: false
        },
		tooltip: {
			theme: 'dark'
		  },
        stroke: {
          curve: 'smooth',
        },
			
		markers: {
			size: 0,
		},
        yaxis: {
          axisBorder: {
            show: false
          },
          axisTicks: {
            show: false,
          },
          labels: {
            show: false,
          }
        
        },
        xaxis: {
          axisBorder: {
            show: false
          },
          axisTicks: {
            show: false,
          },
          labels: {
            show: true,
            formatter: function (val) {
              return val ;
            }
          }
        
        },
		grid: {
			show: true,
			borderColor: '#5578ed',
			strokeDashArray: 0,
			position: 'back',
			xaxis: {
				lines: {
					show: false,
				}
			},   
			yaxis: {
				lines: {
					show: false
				}
			},  
			row: {
				colors: undefined,
				opacity: 0.5,
			},  
			column: {
				colors: undefined,
				opacity: 0.1
			},  
		}
      };

      var chart = new ApexCharts(document.querySelector("#statisticschart3"), options);
      chart.render();


      var options = {
        series: [{
            name: "Profit",
            data: [0, 31, 54, 38, 56, 24, 65, 45, 37, 39]
        }],
        chart: {
			foreColor:"#bac0c7",
          height: 224,
          type: 'area',
          zoom: {
            enabled: false
          }
        },
		colors:['#51ce8a'],
        dataLabels: {
          enabled: false,
        },
        stroke: {
          	show: true,
			curve: 'smooth',
			lineCap: 'butt',
			width: 3,
			dashArray: 0, 
        },		
		markers: {
			size: 5,
			colors: '#51ce8a',
			strokeColors: '#ffffff',
			strokeWidth: 3,
			strokeOpacity: 0.9,
			strokeDashArray: 0,
			fillOpacity: 1,
			discrete: [],
			shape: "circle",
			radius: 5,
			offsetX: 0,
			offsetY: 0,
			onClick: undefined,
			onDblClick: undefined,
			hover: {
			  size: undefined,
			  sizeOffset: 3
			}
		},	
        grid: {
			borderColor: '#f7f7f7', 
          row: {
            colors: ['transparent'], // takes an array which will be repeated on columns
            opacity: 0
          },			
		  yaxis: {
			lines: {
			  show: true,
			},
		  },
        },
		fill: {
			type: "gradient",
			gradient: {
			  shadeIntensity: 1,
			  opacityFrom: 0.01,
			  opacityTo: 1,
			  stops: [0, 90, 100]
			}
		  },
        xaxis: {
          categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'],
		  labels: {
			show: true,        
          },
          axisBorder: {
            show: true
          },
          axisTicks: {
            show: true
          },
          tooltip: {
            enabled: true,        
          },
        },
        yaxis: {
          labels: {
            show: true,
            formatter: function (val) {
              return val + "K";
            }
          }
        
        },
      };
      var chart = new ApexCharts(document.querySelector("#charts_widget_2_chart"), options);
      chart.render();
	
	
