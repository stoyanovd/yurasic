var ch_to_num = {
    'C': 0,
    'C#': 1,
    'D': 2,
    'D#': 3,
    'Eb': 3,
    'E': 4,
    'F': 5,
    'F#': 6,
    'Gb': 6,
    'G': 7,
    'G#': 8,
    'Ab': 8,
    'A': 9,
    'A#': 10,
    'Bb': 10,
    'B': 11
};
var num_to_ch = {
    0: 'C',
    1: 'C#',
    2: 'D',
    3: 'Eb',
    4: 'E',
    5: 'F',
    6: 'F#',
    7: 'G',
    8: 'Ab',
    9: 'A',
    10: 'Bb',
    11: 'B'
};
// import $ from "jquery";
// import $ = require("jquery");
function separateChord(ch) {
    var number_general = 1;
    if (ch.length >= 2 && (ch[1] == '#' || ch[1] == 'b'))
        number_general = 2;
    var general_ch = ch.slice(0, number_general);
    var modificators = ch.slice(number_general);
    return [general_ch, modificators];
}
function transposeChordAddOne(index) {
    var ch = $(this).text();
    // console.log('ch', ch);
    var _a = separateChord(ch), general_ch = _a[0], modificators = _a[1];
    var new_gen_chord = num_to_ch[(ch_to_num[general_ch] + 1) % 12];
    $(this).text(new_gen_chord + modificators);
}
function transposeChordSubOne(index) {
    var ch = $(this).text();
    // console.log('ch', ch);
    var _a = separateChord(ch), general_ch = _a[0], modificators = _a[1];
    var new_gen_chord = num_to_ch[(ch_to_num[general_ch] - 1 + 12) % 12];
    $(this).text(new_gen_chord + modificators);
}
function transposeFullAddOne() {
    console.log('transposeFullAddOne');
    $('.chord').each(transposeChordAddOne);
}
function transposeFullSubOne() {
    console.log('transposeFullSubOne');
    $('.chord').each(transposeChordSubOne);
}
function initializeChordsTransposer() {
    $("#chords_transpose_add_button").on('click', "", transposeFullAddOne);
    $("#chords_transpose_sub_button").on('click', "", transposeFullSubOne);
}
$(document).ready(function () {
    console.log('get transposer file.');
    initializeChordsTransposer();
});
