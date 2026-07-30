import json
import os
import re


class ContactBook:
    def __init__(self, filename: str = "contacts.json"):
        self.filename = filename
        self.contacts: dict[str, dict] = {}
        self.load_contacts()

    def load_contacts(self) -> None:
        """Load contacts from the JSON file."""
        if not os.path.exists(self.filename):
            self.contacts = {}
            return

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, dict):
                self.contacts = data
            else:
                print("Invalid contacts file format.")
                self.contacts = {}

        except json.JSONDecodeError:
            print("The contacts file is empty or damaged.")
            self.contacts = {}

        except OSError as error:
            print(f"Could not load contacts: {error}")
            self.contacts = {}

    def save_contacts(self) -> None:
        """Save all contacts to the JSON file."""
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(
                    self.contacts,
                    file,
                    indent=4,
                    ensure_ascii=False,
                )

        except OSError as error:
            print(f"Could not save contacts: {error}")

    def generate_contact_id(self) -> str:
        """Generate a unique contact ID."""
        if not self.contacts:
            return "C001"

        numeric_ids = []

        for contact_id in self.contacts:
            try:
                number = int(contact_id[1:])
                numeric_ids.append(number)
            except ValueError:
                continue

        next_number = max(numeric_ids, default=0) + 1
        return f"C{next_number:03d}"

    def is_valid_email(self, email: str) -> bool:
        """Check whether an email address has a basic valid format."""
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    def is_valid_phone(self, phone: str) -> bool:
        """Check whether a phone number contains enough digits."""
        digits = "".join(character for character in phone if character.isdigit())
        return 7 <= len(digits) <= 15

    def add_contact(
        self,
        name: str,
        phone: str,
        email: str,
    ) -> bool:
        """Add a new contact."""
        name = name.strip()
        phone = phone.strip()
        email = email.strip().lower()

        if not name:
            print("Name cannot be empty.")
            return False

        if not self.is_valid_phone(phone):
            print("Please enter a valid phone number.")
            return False

        if not self.is_valid_email(email):
            print("Please enter a valid email address.")
            return False

        for contact in self.contacts.values():
            if contact["phone"] == phone:
                print("A contact with this phone number already exists.")
                return False

            if contact["email"].lower() == email:
                print("A contact with this email already exists.")
                return False

        contact_id = self.generate_contact_id()

        self.contacts[contact_id] = {
            "name": name,
            "phone": phone,
            "email": email,
        }

        self.save_contacts()

        print(f"Contact added successfully with ID {contact_id}.")
        return True

    def show_contacts(self) -> None:
        """Display all contacts."""
        if not self.contacts:
            print("No contacts found.")
            return

        print("\n--- Contact Book ---")

        sorted_contacts = sorted(
            self.contacts.items(),
            key=lambda item: item[1]["name"].lower(),
        )

        for contact_id, contact in sorted_contacts:
            print(
                f"\nID: {contact_id}\n"
                f"Name: {contact['name']}\n"
                f"Phone: {contact['phone']}\n"
                f"Email: {contact['email']}"
            )

    def search_contacts(self, keyword: str) -> list[tuple[str, dict]]:
        """Search by name, phone number, email, or contact ID."""
        keyword = keyword.strip().lower()

        if not keyword:
            print("Search keyword cannot be empty.")
            return []

        matches = []

        for contact_id, contact in self.contacts.items():
            searchable_values = [
                contact_id.lower(),
                contact["name"].lower(),
                contact["phone"].lower(),
                contact["email"].lower(),
            ]

            if any(keyword in value for value in searchable_values):
                matches.append((contact_id, contact))

        return matches

    def display_search_results(self, keyword: str) -> None:
        """Search and display matching contacts."""
        matches = self.search_contacts(keyword)

        if not matches:
            print("No matching contacts found.")
            return

        print(f"\n--- Search results for '{keyword}' ---")

        for contact_id, contact in matches:
            print(
                f"\nID: {contact_id}\n"
                f"Name: {contact['name']}\n"
                f"Phone: {contact['phone']}\n"
                f"Email: {contact['email']}"
            )

    def update_contact(
        self,
        contact_id: str,
        name: str | None = None,
        phone: str | None = None,
        email: str | None = None,
    ) -> bool:
        """Update an existing contact."""
        contact_id = contact_id.strip().upper()
        contact = self.contacts.get(contact_id)

        if contact is None:
            print("Contact not found.")
            return False

        if name is not None and name.strip():
            contact["name"] = name.strip()

        if phone is not None and phone.strip():
            phone = phone.strip()

            if not self.is_valid_phone(phone):
                print("Invalid phone number.")
                return False

            contact["phone"] = phone

        if email is not None and email.strip():
            email = email.strip().lower()

            if not self.is_valid_email(email):
                print("Invalid email address.")
                return False

            contact["email"] = email

        self.save_contacts()

        print("Contact updated successfully.")
        return True

    def delete_contact(self, contact_id: str) -> bool:
        """Delete a contact using its ID."""
        contact_id = contact_id.strip().upper()

        if contact_id not in self.contacts:
            print("Contact not found.")
            return False

        deleted_contact = self.contacts.pop(contact_id)
        self.save_contacts()

        print(f"{deleted_contact['name']} deleted successfully.")
        return True


def show_menu() -> None:
    print("\n--- Contact Book ---")
    print("1. Show all contacts")
    print("2. Add contact")
    print("3. Search contacts")
    print("4. Update contact")
    print("5. Delete contact")
    print("6. Exit")


def main() -> None:
    contact_book = ContactBook()

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            contact_book.show_contacts()

        elif choice == "2":
            name = input("Enter name: ")
            phone = input("Enter phone number: ")
            email = input("Enter email address: ")

            contact_book.add_contact(name, phone, email)

        elif choice == "3":
            keyword = input(
                "Enter name, phone number, email, or ID: "
            )

            contact_book.display_search_results(keyword)

        elif choice == "4":
            contact_id = input("Enter contact ID to update: ")
            print("Leave a field blank to keep its current value.")

            name = input("Enter new name: ")
            phone = input("Enter new phone number: ")
            email = input("Enter new email address: ")

            contact_book.update_contact(
                contact_id,
                name=name or None,
                phone=phone or None,
                email=email or None,
            )

        elif choice == "5":
            contact_id = input("Enter contact ID to delete: ")
            contact_book.delete_contact(contact_id)

        elif choice == "6":
            print("Goodbye.")
            break

        else:
            print("Invalid choice. Enter a number from 1 to 6.")


if __name__ == "__main__":
    main()