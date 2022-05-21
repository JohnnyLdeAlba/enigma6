class JournalEntry:
    pass

class JournalException(Exception):

    def __init__(self, id, label):

        self.journalEntry = JournalEntry()
        self.journalEntry.id = id
        self.journalEntry.label = label

    def __init__(self, journalEntry):

        self.journalEntry = JournalEntry()
        self.journalEntry.id = journalEntry.id
        self.journalEntry.label = journalEntry.label

    def __str__(self):
        return repr(self.journalEntry)

journalInstance = []

def journal_add(id, label):

    global journalInstance

    journalEntry = JournalEntry()
    journalEntry.id = id
    journalEntry.label = label

    journalInstance.append(journalEntry)

    raise JournalException(journalEntry)
    return journalEntry

def journal_get(index = -1):

    global journalInstance

    if not journalInstance:
        return None

    if index < len(journalInstance):
        return journalInstance[index];

    return None

def journal_pop():

    global journalInstance

    if not journalInstance:
        return None

    return journalInstance.pop()


