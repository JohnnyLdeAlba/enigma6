function AjaxInterface() {

    this.controller = null;

    this.journalEntry = null;
    this.responseData = null;
    this.transferCurrent = 0;
    this.transferTotal = 0;

    this.httpRequest = null;

    return; }

function ajax_transfer_complete(event) {

    var ajaxInstance = component_get('ajaxInstance');

    journal_entry_set(
        ajaxInstance.journalEntry,
        1, 'AJAX_TRANSFER_COMPLETE'); 

    if (this.readyState == 4)
        if (this.status == 200) {

            ajaxInstance.responseData = this.response; }
    
    ajaxInstance.controller();
    return; }

function ajax_transfer_failed(event) {

    var ajaxInstance = component_get('ajaxInstance');

    journal_entry_set(
        ajaxInstance.journalEntry,
        -2, 'AJAX_TRANSFER_FAILED'); 

    ajaxInstance.controller();
    return; }

function ajax_transfer_userAborted(event) {

    var ajaxInstance = component_get('ajaxInstance');

    journal_entry_set(
        ajaxInstance.journalEntry,
        -3, 'AJAX_TRANSFER_USERABORTED'); 

    // ajaxInstance.controller();
    return; }

function ajax_transfer_updateProgress(event) {

    var ajaxInstance = component_get('ajaxInstance');

    if (event.lengthComputable) {

        if (ajaxInstance.transferTotal == 0)
            ajaxInstance.transferTotal = event.total;
        
        ajaxInstance.transferCurrent = event.loaded; }

    else ajaxInstance.transferTotal = -1;  

    // ajaxInstance.controller();
    return; }

function ajax_initialize(ajaxInstance) {

    var httpRequest = null;

    if (window.XMLHttpRequest && window.FormData)
        httpRequest = new XMLHttpRequest();
    else return -1;

    ajaxInstance.journalEntry = new JournalEntry(0, '');

    httpRequest.addEventListener(
        'abort', ajax_transfer_userAborted, false);
    httpRequest.addEventListener(
        'error', ajax_transfer_failed, false);
    httpRequest.addEventListener(
        'load', ajax_transfer_complete, false); 
    httpRequest.addEventListener(
        'progress', ajax_transfer_updateProgress, false); 

    ajaxInstance.httpRequest = httpRequest; 
    return 0; }

function ajax_send(ajaxInstance, method, uri, row) {

    if (ajaxInstance.httpRequest == null)
        return -1;

    var httpRequest = ajaxInstance.httpRequest;
    var formData = (row == null) ? null: new FormData();

    ajaxInstance.transferCurrent = 0;
    ajaxInstance.transferTotal = 0;
    ajaxInstance.transferStatus = 0;

    if (formData != null)
        for (var key in row)
            formData.append(key, row[key]);

    httpRequest.open(method, uri, true);
    httpRequest.send(formData);

    return 0; }
