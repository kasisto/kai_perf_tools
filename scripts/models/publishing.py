import json

class PublishingObj:
    def __init__(self, doc_type, doc_id, rev_id, pub_state='PUBLISHED'):
        if doc_type == 'knowledge_conditions':
            self.document_type = doc_type
        else:
            self.document_type = doc_type if not doc_type.endswith('s') else doc_type.rstrip('s')   # Needed for when doc.get_type() is used
        self.document_name = doc_id
        self.revision_id = rev_id
        self.publishing_state = pub_state
    
    def __repr__(self):
        return str({
            'document_type': self.document_type,
            'document_name': self.document_name,
            'revision_id': self.revision_id,
            'publishing_state': self.publishing_state
        })

    def get_json(self):
        return {
            'document_type': self.document_type,
            'document_name': self.document_name,
            'revision_id': self.revision_id,
            'publishing_state': self.publishing_state
        }


class PublishingPayload:
    def __init__(self, revisions, notes='auto_published'):
        self.publishing_notes = notes
        self.revisions = revisions if isinstance(revisions, list) else [revisions]
        
    def __repr__(self):
        return str({'publishing_notes': self.publishing_notes, 'revisions': self.revisions})
    
    def get_json(self):
        return str(json.dumps(
            {'publishing_notes': self.publishing_notes, 'revisions': self.revisions}))
