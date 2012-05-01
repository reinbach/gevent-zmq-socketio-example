$(function() { 
    // Open up a connection to our server 
    var socket = io.connect("", {'host': 'localhost', 'port': 9999});

    // Save our plot placeholder 
    var $placeholder = $('#placeholder'); 
    // Maximum # of data points to plot 
    var datalen = 100; 
    // This will be the plot object 
    var plot = null; 
    // Set up some options on our data series 
    var series = { 
        label: "Value", 
        lines: { 
            show: true, 
            fill: true 
        }, 
        points: { 
            show:true 
        }, 
        data: [] 
    }; 

    // What do we do when we get a message? 
    socket.on('message', function(msg) { 
        var d = $.parseJSON(msg); 
        series.data.push([d.x, d.y]); 
        // Keep the data series a manageable length 
        while (series.data.length > datalen) { 
            series.data.shift(); 
        } 
        if(plot) { 
            // Create the plot if it's not there already 
            plot.setData([series]); 
            plot.setupGrid(); 
            plot.draw(); 
        } else if(series.data.length > 10) { 
            // Update the plot 
            plot = $.plot($placeholder, [series], { 
                xaxis:{ 
                    mode: "time", 
                    timeformat: "%H:%M:%S", 
                    minTickSize: [2, "second"], 
                }, 
                yaxis: { 
                    min: 0, 
                    max: 5 
                } 
            }); 
            plot.draw(); 
        } 
    });

    // Just update our conn_status field with the connection status 
    socket.on('connect', function() { 
        $('#conn_status').html('<b>Connected</b>'); 
	// this is the call that streams the sine wave data
	socket.emit('stream', '');
    });
    socket.on('error', function() { 
        $('#conn_status').html('<b>Error</b>'); 
    });
    socket.on('disconnect', function() { 
        $('#conn_status').html('<b>Closed</b>'); 
    });
}); 