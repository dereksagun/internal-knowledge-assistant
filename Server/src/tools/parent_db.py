class ParentDB:
    def __init__(self):
        self._documents: dict[str, dict] = {}
        
    def add_document(self, pid, doc):
        self._documents[pid] = doc

    def get_record(self, pid: str):
        return self._documents[pid]

    def get_all_records(self):
        return self._documents
    
    def get_content(self, pid:str):
        return self._documents[pid].get("content")
