function JournalEntry(id, label) {

    this.id = id;
    this.label = label; 

    return; }

function journal_entry_set(journalEntry, id, label) {

    journalEntry.id = id;
    journalEntry.label = label;

    return journalEntry; }

function JournalException(journalEntry) {

    this.journalEntry = journalEntry;
    return; }

journalInstance = new Array();

function journal_add(id, label) {

    journalEntry = new JournalEntry(id, label);
    journalInstance.push(new JournalEntry(id, label));

    throw new JournalException(journalEntry);
    return journalEntry; }

function journal_get(id) {

    id = (typeof id == 'undefined') ?
        journalInstance.length-1: id;

    if (id < journalInstance.length)
        return journalInstance[id];

    return null; }

function journal_pop() {

    if (journalInstance.length == 0)
        return null;

    return journalInstance.pop(); }
