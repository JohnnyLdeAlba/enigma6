function RegisterInterface() {

    this.username = '';
    this.email = '';
    this.password = '';
    this.verify_password = '';
    this.persistent = false;

    this.buttonRegisterDisabled = false;

    return; }

/* This needs to be a universal controller for 'UserController' */

function post_register_success() {

    var ioInstance = component_get('ioInstance');
    var dialogInstance = component_get('dialogInstance');
    var ajaxInstance = component_get('ajaxInstance');

    if (ajaxInstance.journalEntry['id'] == 0)
        return;

    else if (ajaxInstance.journalEntry['id'] < 0) {
   
        var body = user_journal_glossary(
            ajaxInstance.journalEntry);

        dialog_alert(dialogInstance, body);
        ioInstance.$scope.$apply();

        return; }

    var row  = null;

    if (typeof ajaxInstance.responseData == 'string')
        row = io_json_decode(ajaxInstance.responseData);

    if ((typeof row == 'undefined') || row == null)

        row = {
            'journalEntryId': 100,
            'journalEntryLabel': 'JSON_DECODE_FAILED' }; 

    if (row['journalEntryId'] > 0) {

        var body = user_journal_glossary(
            new JournalEntry(
                row['journalEntryId'],
                row['journalEntryLabel']));

        dialog_alert(dialogInstance, body);
        ioInstance.$scope.$apply();

        return; }

    return; }

function button_register_onClick() {

    var ioInstance = component_get('ioInstance');
    var dialogInstance = component_get('dialogInstance');
    var ajaxInstance = component_get('ajaxInstance');
    var registerInstance = component_get('registerInstance');

    dialog_alert(dialogInstance, null);
 
    try {

        user_validate_username(
            registerInstance.username);

        user_validate_password(
            registerInstance.password);

        user_verify_password(
            registerInstance.password,
            registerInstance.verify_password);
 
        registerInstance.buttonRegisterDisabled = false; }

    catch (journalException) { 

        var body = user_journal_glossary(
            journalException.journalEntry);

        dialog_alert(dialogInstance, body);

    return; }

    var row = {

        'username': registerInstance.username,
        'email': registerInstance.email,
        'password': registerInstance.password,
        'persistent': registerInstance.persistent };
           
    ajax_send(
        ajaxInstance,
        'POST',
        'm_register.py',
        row);
 
    return; }

function register_redirect(uri) {

    dialog_redirect(
        component_get('dialogInstance'),
        uri);

    return; }

function register_initialize($scope, $window) {

        var ioInstance = new DialogInterface();
        var dialogInstance = new DialogInterface();
        var ajaxInstance = new AjaxInterface();
        var registerInstance = new RegisterInterface();

        ioInstance.$scope = $scope;
        ioInstance.$window = $window;

        dialogInstance.ioInstance = ioInstance;
        ajaxInstance.controller = post_register_success;

        ajax_initialize(ajaxInstance);

        component_add('ioInstance', ioInstance);
        component_add('dialogInstance', dialogInstance);
        component_add('ajaxInstance', ajaxInstance);
        component_add('registerInstance', registerInstance);

    return; }

angular.module('EnigmaModule', [])

    .controller('RegisterController', 

        ['$scope', '$window',
    
        function($scope, $window) {

            register_initialize($scope, $window);

            $scope.ioInstance = component_get('ioInstance');
            $scope.dialogInstance = component_get('dialogInstance');
            $scope.ajaxInstance = component_get('ajaxInstance');
            $scope.registerInstance = component_get('registerInstance');

            $scope.redirect = register_redirect;
            $scope.button_register_onClick = button_register_onClick;

            return; }]);
