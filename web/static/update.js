var previous_status = null;

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

            if (previous_status !== status) {
                previous_status = status;

                // get elemets to fade out
                var elements_to_fade = $('[do_fade]');
                var first_load = false;
                if (elements_to_fade.length <= 0) {
                    elements_to_fade = $('body>>:hidden');
                    first_load = true;
                }

                var fade_out_time = 0;

                if (first_load !== true) {
                    // do the fade out in reverse order otherwise the elements jump around (because the DOM is changing)
                    $(elements_to_fade.get().reverse()).each(function() {
                        const element = $(this);

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
                    elements_to_fade.each(function() {
                        const element = $(this);
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