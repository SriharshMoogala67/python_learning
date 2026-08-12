import json 

class ContactBook: 
    def __init__(self): 
        self.contacts = {}

    def add_contact(self, CID, name, phone, email): 
        if CID in self.contacts: 
            print("contact already exists") 
            return False 

        self.contacts[CID] = {
            "name" = name,
            "phone" = phone, 
            "email" = email, 

        }

        return True 

    def show_contacts(self):
        for contact_id, contact in self.contacts.items():
            print("ID:", contact_id)
            print("Name:", contact["name"])
            print("Phone:", contact["phone"])
            print("Email:", contact["email"])
            print()


    def search_contact(self, keyword): 
        keyword = keyword.lower()

        for CID, contact in self.contacts.items(): 
            if(
                keyword in contact["name"].lower() or
               keyword in contact["phone"] or 
               keyword in contact["email"].lower()
               ): 

                print("ID:", CID)
                print("Name:", contact["name"])
                print("Phone:", contact["phone"])
                print("Email:", contact["email"])
                print()

    
