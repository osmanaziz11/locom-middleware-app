import os
import firebase_admin
from firebase_admin import storage
from firebase_admin import firestore
from firebase_admin import credentials


class FirebaseManager:
    def __init__(self):
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        self.absPath = os.path.abspath(os.path.join(current_script_dir, ".."))
        cred = credentials.Certificate(
            f'{current_script_dir}\\firebase-config.json')
        firebase_admin.initialize_app(
            cred, {'storageBucket': 'locom-d2a62.appspot.com'})
        self.db = firestore.client()
        self.bucket = storage.bucket()

    def get_forwarded_number(self, virtual_number):
        try:
            docRef = self.db.collection('virtuals').document(virtual_number)
            doc = docRef.get()
            if doc.exists:
                return doc.to_dict()
            else:
                return None
        except Exception as exc:
            return str(exc)

    def blacklist_check(self, virtual_number, user_number):
        try:
            docRef = self.db.collection('blacklist').document(virtual_number)
            doc = docRef.get()
            if doc.exists:
                numberList = doc.to_dict()['numbers']
                if user_number in numberList:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as exc:
            return str(exc)

    def add_conversation(self, virtual_number, user_number):
        try:
            docRef = self.db.collection(
                f'virtuals/{virtual_number}/conversation').document(user_number)
            docRef.set({'mode': True})
            return True
        except Exception as exc:
            return str(exc)

    def add_message(self, payload):
        try:
            docRef = self.db.collection(
                f'virtuals/{payload["virtual_number"]}/conversation').document(payload['user_number'])
            docRef.update(
                {"messages": firestore.ArrayUnion([payload['message']])})
            return True
        except Exception as exc:
            return str(exc)

    def get_messages(self, virtual_number, user_number):
        try:
            docRef = self.db.collection(
                f'virtuals/{virtual_number}/conversation').document(user_number)
            doc = docRef.get()
            if doc.exists:
                messages = doc.to_dict()['messages']
                return messages if type(messages == list) else None
            else:
                return None
        except Exception as exc:
            return str(exc)

    def check_conversation_take_over(self, virtual_number, user_number):
        try:
            docRef = self.db.collection(
                f'virtuals/{virtual_number}/conversation').document(user_number)
            doc = docRef.get()
            if doc.exists:
                return doc.to_dict()['mode']
            else:
                return True  # Permission to send message
        except Exception as exc:
            return str(exc)

    def get_file_content_from_storage(self, filename):
        try:
            blob = self.bucket.blob(filename)
            blob.download_to_filename(f'{self.absPath}\\dataset\\.txt')
        except Exception as exc:
            print(str(exc))
