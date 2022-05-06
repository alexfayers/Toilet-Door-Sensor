var previous_data = null;

const FADE_TIME = 1000;
const FADE_INTERVAL = 100;
const LOADING_RATE = 1000;


function loadingPing() {
    const loading_indicator = $('#loading-indicator');

    const half_loading_rate = LOADING_RATE / 2;
    loading_indicator.fadeToggle(half_loading_rate).promise().then(() => {
        loading_indicator.fadeToggle(half_loading_rate);
    });
}


function update() {
    const host = `${window.location.protocol}//${window.location.hostname}:${window.location.port}`;
    const url = `${host}/api/current_full`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            // get information from the data

            console.log("Got update");
            const status = data.status;
            const color = data.color; // derived from status
            const subtext = `<i>${data.subtext}</i>`; // derived from status

            const timestamp = data.timestamp;
            const wait_message = data.wait_message;
            const minutes_ago = data.minutes_ago;
            const footer_message = `(door was ${status === 'Yes' ? 'opened' : 'closed'} at ${timestamp}${minutes_ago})`;

            const status_element = $("#status");
            const subtext_element = $("#subtext");
            const wait_message_element = $("#wait_message");
            const footer_element = $("#footer");

            // Update the status
            var differences = [];
            if (previous_data !== null) {
                differences = _.reduce(previous_data, (result, value, key) => _.isEqual(value, data[key]) ? result : result.concat(key), [])
            }

            if (differences.length > 0 || previous_data === null) {
                previous_data = data;

                // get all elements that can be faded out
                var elements_to_fade = $('[do_fade]');
                var first_load = false;
                if (elements_to_fade.length <= 0) {
                    elements_to_fade = $('body>>:hidden');
                    first_load = true;
                }

                // calculate which elements need to be updated
                var to_update = [];

                if (differences.includes('status')) {  // if the status changes, update everything
                    elements_to_fade.each(function() {
                        to_update.push($(this));
                    });
                }
                else {
                    if (differences.length > 0) {  // if there are any differences
                        // if the wait message changes, update it
                        if (differences.includes("minutes_ago") || differences.includes("timestamp")) {
                            to_update.push(footer_element);
                        }

                        // scan all possible fade elements and check if their id is in the differences array
                        // if so, add it to the update array
                        elements_to_fade.each(function() {
                            const element = $(this);
                            const element_id = element.attr('id');

                            if (differences.includes(element_id)) {
                                to_update.push(element);
                            }
                        });
                    }
                    else { // no differences - this can only happen on first load, so update everything
                        elements_to_fade.each(function() {
                            to_update.push($(this));
                        });
                    }    
                }
                
                var fade_out_time = 0;

                if (first_load !== true) {
                    // do the fade out in reverse order otherwise the elements jump around (because the DOM is changing)
                    to_update.slice().reverse().forEach(element => {
                        setTimeout(function() {
                            element.fadeOut(FADE_TIME);
                        }, fade_out_time);
                        fade_out_time += FADE_INTERVAL;
                    });
                }

                // do the fade in
                setTimeout(function() {
                    // update text
                    status_element.html(status);
                    subtext_element.html(subtext);
                    wait_message_element.html(wait_message);
                    footer_element.html(footer_message);
        
                    status_element.attr('class', `status ${color}`);
        
                    var time = 0;
                    to_update.forEach(element => {
                        element.attr('do_fade', 'true');

                        setTimeout(function() {
                            element.fadeIn(FADE_TIME);
                        }, time);
                        time += FADE_INTERVAL;
                    });
                }, fade_out_time + (fade_out_time > 0 ? FADE_TIME : 0));
                      
            }
            // else {
            //     loadingPing();
            // }
            
        })
        .catch(error => console.error(error));
}