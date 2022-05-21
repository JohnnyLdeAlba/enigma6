var componentInstance = {};

function component_add(label, entry) {
    
    componentInstance[label] = entry;
    return componentInstance[label]; }

function component_get(id) {

    if (componentInstance[id] == 'undefined')
        return null;

    return componentInstance[id]; }

function IOInterface() {

    this.$scope = null;
    this.$window = null;

    return; }

function io_uri_encode(uri) {
    return encodeURIComponent(uri); }

function io_json_encode(table) {
    return JSON.stringify(table); }

function io_json_decode(source) {

    if (typeof source != 'string')
        return null;

    var table = null;
 
    try { table = JSON.parse(source); }
    catch (syntaxError) { return null; } 

    return table; }

function DialogInterface() {

    this.ioInstance = null;
    this.fadeIn = true;

    this.alertShow = false;
    this.alertBody = '';

    return; }

function dialog_redirect(dialogInstance, uri) {

    dialogInstance.fadeIn = false;

    setTimeout(
        function() { 

            dialogInstance.ioInstance.
            $window.location.href = uri;

            return; },

        1000);

    return; }

function dialog_alert(dialogInstance, body) {

    if (body == null) {

        dialogInstance.alertShow = false;
        dialogInstance.alertBody = '';

        return; }

    dialogInstance.alertShow = true;
    dialogInstance.alertBody = body;

    return; }

