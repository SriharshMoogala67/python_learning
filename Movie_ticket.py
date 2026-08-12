class Ticket: 
    def __init__(self, ticket_id, cust_name, movie_name, seat_number): 
        self.ticket_id = ticket_id
        self.cust_name = cust_name
        self.movie_name = movie_name
        self.seat_number = seat_number
    def show_details(self):
        print("Ticket ID:", self.ticket_id)
        print("Customer:", self.cust_name)
        print("Movie:", self.movie_name)
        print("Seat:", self.seat_number)

class MovieShow:

    next_ticket_id = 1

    def __init__(self, movie_name):
        self.movie_name = movie_name
        self.seats = {}
        self.tickets = {}

        for number in range(1, 6): 
            seat_no = f"A{number}"
            self.seats[seat_no] = "Available"

    def book_seats(self, cust_name, seat_no): 

        if seat_no not in self.seats: 
            print("seat not found")
            return False
        
        if self.seats[seat_no] == "booked":
            print("seat already taken")
            return False


        self.seats[seat_no] = "booked"
        ticket_id = self.generate_ticket_id()

        ticket = Ticket(
            ticket_id,
            cust_name,
            self.movie_name,
            seat_no, 
        )
        self.tickets[ticket_id] = ticket
        print("seat booked successfully")
        return True 

    def generate_ticket_id(self): 
        ticket_id = f"TKT{MovieShow.next_ticket_id:03d}"
        MovieShow.next_ticket_id += 1
        return ticket_id
    
    def show_ticket(self, ticket_id):
        ticket = self.tickets.get(ticket_id)

        if ticket is None:
            print("Ticket not found")
            return

        ticket.show_details()

show = MovieShow("Interstellar")
print(show.seats)

mov = MovieShow("cars")
mov.book_seats("Harsh", "A2")
print(mov.seats)

mov.book_seats("Ram", "A2")
print(mov.seats)