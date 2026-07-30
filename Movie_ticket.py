class TicketIDGenerator:
    next_id = 1

    @classmethod
    def generate_id(cls) -> str:
        ticket_id = f"TKT{cls.next_id:04d}"
        cls.next_id += 1
        return ticket_id


class Ticket:
    def __init__(
        self,
        ticket_id: str,
        customer_name: str,
        movie_name: str,
        seat_number: str,
        price: float,
    ):
        self.ticket_id = ticket_id
        self.customer_name = customer_name
        self.movie_name = movie_name
        self.seat_number = seat_number
        self.price = price

    def display(self) -> None:
        print("\n--- Movie Ticket ---")
        print(f"Ticket ID: {self.ticket_id}")
        print(f"Customer: {self.customer_name}")
        print(f"Movie: {self.movie_name}")
        print(f"Seat: {self.seat_number}")
        print(f"Price: £{self.price:.2f}")


class MovieShow:
    def __init__(
        self,
        movie_name: str,
        seat_count: int,
        ticket_price: float,
    ):
        if not movie_name.strip():
            raise ValueError("Movie name cannot be empty.")

        if seat_count <= 0:
            raise ValueError("Seat count must be greater than zero.")

        if ticket_price < 0:
            raise ValueError("Ticket price cannot be negative.")

        self.movie_name = movie_name.strip()
        self.ticket_price = ticket_price
        self.seats: dict[str, str] = {}
        self.tickets: dict[str, Ticket] = {}

        for number in range(1, seat_count + 1):
            seat_number = f"A{number}"
            self.seats[seat_number] = "Available"

    def show_seats(self) -> None:
        print(f"\n--- Seats for {self.movie_name} ---")

        for seat_number, status in self.seats.items():
            print(f"{seat_number}: {status}")

    def book_seat(
        self,
        customer_name: str,
        seat_number: str,
    ) -> Ticket | None:
        customer_name = customer_name.strip()
        seat_number = seat_number.strip().upper()

        if not customer_name:
            print("Customer name cannot be empty.")
            return None

        if seat_number not in self.seats:
            print("Invalid seat number.")
            return None

        if self.seats[seat_number] == "Booked":
            print(f"Seat {seat_number} is already booked.")
            return None

        self.seats[seat_number] = "Booked"

        ticket_id = TicketIDGenerator.generate_id()

        ticket = Ticket(
            ticket_id=ticket_id,
            customer_name=customer_name,
            movie_name=self.movie_name,
            seat_number=seat_number,
            price=self.ticket_price,
        )

        self.tickets[ticket_id] = ticket

        print(f"Seat {seat_number} booked successfully.")
        print(f"Ticket ID: {ticket_id}")

        return ticket

    def cancel_ticket(self, ticket_id: str) -> bool:
        ticket_id = ticket_id.strip().upper()
        ticket = self.tickets.get(ticket_id)

        if ticket is None:
            print("Ticket not found.")
            return False

        seat_number = ticket.seat_number
        self.seats[seat_number] = "Available"

        del self.tickets[ticket_id]

        print(f"Ticket {ticket_id} cancelled successfully.")
        print(f"Seat {seat_number} is available again.")

        return True

    def find_ticket(self, ticket_id: str) -> Ticket | None:
        return self.tickets.get(ticket_id.strip().upper())

    def show_bookings(self) -> None:
        if not self.tickets:
            print("No bookings found.")
            return

        print("\n--- Current Bookings ---")

        for ticket in self.tickets.values():
            print(
                f"{ticket.ticket_id} | "
                f"{ticket.customer_name} | "
                f"{ticket.seat_number}"
            )

    def available_seat_count(self) -> int:
        count = 0

        for status in self.seats.values():
            if status == "Available":
                count += 1

        return count



if __name__ == "__main__":
    show = MovieShow(
        movie_name="Interstellar",
        seat_count=5,
        ticket_price=12.50,
    )

    show.show_seats()

    ticket1 = show.book_seat("Harsh", "A1")
    ticket2 = show.book_seat("Rahul", "A2")

    # Tries to book an already-booked seat
    ticket3 = show.book_seat("Aman", "A1")

    show.show_seats()
    show.show_bookings()

    if ticket1:
        ticket1.display()

    print(
        "Available seats:",
        show.available_seat_count(),
    )

    if ticket1:
        show.cancel_ticket(ticket1.ticket_id)

    show.show_seats()