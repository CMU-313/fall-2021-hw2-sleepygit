'use strict';

var reviewerSelectionTemplate = function (reviewer, container) {
    var $reviewer = $(
        '<span class="label label-reviewer" style="background: ' + reviewer.element.dataset.color + ';"> ' + reviewer.text + '</span>'
    );
    container[0].style.background = reviewer.element.dataset.color;
    return $reviewer;
}

var reviewerResultTemplate = function (reviewer) {
    if (!reviewer.element) { return ''; }
    var $reviewer = $(
        '<span class="label label-reviewer" style="background: ' + reviewer.element.dataset.color + ';"> ' + reviewer.text + '</span>'
    );
    return $reviewer;
}

jQuery(document).ready(function() {
    $('.select2-reviewers').select2({
        templateSelection: reviewerSelectionTemplate,
        templateResult: reviewerResultTemplate,
        width: '100%'
    });
});
