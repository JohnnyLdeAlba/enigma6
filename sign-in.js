
function SignInInterface() {

    this.username = '';
    this.password = '';
    this.persistent = false;

    return; }


function button_signIn_onClick() {

    var signInInstance = component_get('signInInstance');
    var dialogInstance = component_get('dialogInstance');
 
    try {

        user_validate_username(
            signInInstance.username);

        user_validate_password(
            signInInstance.password); }

    catch (journalException) { 

        var body = user_journal_glossary(
            journalException.journalEntry);

        dialog_alert(dialogInstance, body);

    return; }

    dialog_alert(dialogInstance, null);
    return; }

function signIn_redirect(uri) {

    dialog_redirect(
        component_get('dialogInstance'),
        uri);

    return; }

function signIn_initialize($window) {

        var dialogInstance = new DialogInterface();
        var signInInstance = new SignInInterface();

        dialogInstance.$window = $window;

        component_add('dialogInstance', dialogInstance);
        component_add('signInInstance', signInInstance);

    return; }

angular.module('EnigmaModule', [])

    .controller('SignInController', 

        ['$scope', '$window',
    
        function($scope, $window) {

            signIn_initialize($window);

            $scope.dialogInstance = component_get('dialogInstance');
            $scope.signInInstance = component_get('signInInstance');

            $scope.redirect = signIn_redirect;
            $scope.button_signIn_onClick = button_signIn_onClick;

            return; }]);
