function user_guid(id) { return 3000+id; }

function user_journal_glossary(journalEntry) {

    var id = journalEntry.id;
    switch (id) {

        case 3052: return id+": The username field must not be empty.";
        case 3053: return id+": Username's must contain between 3 and 32 characters.";
        case 3054: return id+": Username's must only contain letters, numbers, "
            +"the dash '-' or underscore '_' characters.";
 
        case 3071: return id+": The password field must not be empty.";
        case 3072: return id+": Password's must contain between 4 and 32 characters.";
        case 3073: return id+": Password's must only contain letters, numbers, "
            +"the dash '-' or underscore '_' characters.";
        case 3074: return id+": The password and verify password fields must match."; }
 
    return journalEntry.id+': '+journalEntry.label; }

function user_validate_username(username) {

    if (username == '') {
        journal_add(
            user_guid(52),
            'USER_EMPTY_USERNAME');
        return -1; }
 
    var r = username.match(/.{3,32}/g);
    if (r == null) {
        journal_add(
            user_guid(53),
            'USER_CHARCOUNT_USERNAME');
        return -2; }
 
    r = username.match(/^[A-Za-z0-9-_]+$/g);
    if (r == null) {
        journal_add(
            user_guid(54),
            'USER_ILLEGALCHARS_USERNAME');
        return -4; }
 
    return 0; }

function user_validate_password(password) {

    if (password == '') {
        journal_add(
            user_guid(71),
            'USER_EMPTY_PASSWORD');
        return -1; }
 
    var r = password.match(/.{4,32}/g);
    if (r == null) {
        journal_add(
            user_guid(72),
            'USER_CHARCOUNT_PASSWORD');
        return -2; }
 
    r = password.match(/^[A-Za-z0-9-_]+$/g);
    if (r == null) {
        journal_add(
            user_guid(73),
            'USER_ILLEGALCHARS_PASSWORD');
        return -1; }
 
    return 0; }

function user_verify_password(password, verify_password) {

    if (password != verify_password) {
        journal_add(
            user_guid(74),
            'USER_NOMATCH_PASSWORD');
        return -1; }

   return 0; }
