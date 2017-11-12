function toggleOnlyChordsVisibility() {
    $('.chords_line_collapse').css('display', 'inline').addClass('chords_line_no_pre');
    $('.text_collapse').css('display', 'none');
}

function toggleOnlyTextVisibility() {
    $('.chords_line_collapse').css('display', 'none').removeClass('chords_line_no_pre').removeClass('chords_line_no_pre');
    $('.text_collapse').css('display', 'inline');

}

function toggleBothChordsAndTextVisibility() {
    $('.chords_line_collapse').css('display', 'inline').removeClass('chords_line_no_pre').removeClass('chords_line_no_pre');
    $('.text_collapse').css('display', 'inline');
}

function initializeTogglerChordsText() {
    var rad = $("[name='toggle_chords_radio']");
    console.log('len:', rad.length);

    for (var i = 0; i < rad.length; i++) {
        if (rad[i].value === 'both') {
            rad[i].parentElement.addEventListener('click', toggleBothChordsAndTextVisibility)
        } else if (rad[i].value === 'chords') {
            rad[i].parentElement.addEventListener('click', toggleOnlyChordsVisibility)
        } else if (rad[i].value === 'text') {
            rad[i].parentElement.addEventListener('click', toggleOnlyTextVisibility)
        }
    }
}

$(document).ready(function () {
    initializeTogglerChordsText();
});

