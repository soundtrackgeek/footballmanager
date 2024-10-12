import random
from player import Player, Position

class TransferMarket:
    def __init__(self):
        self.transfer_list = []
        self.loan_list = []
        self.pending_transfers = []
        self.bids = {}  # New attribute to track bids

    def update_transfer_list(self, teams):
        for team in teams:
            if random.random() < 0.1:  # 10% chance
                if team.squad:
                    player = random.choice(team.squad)
                    if not any(p == player for p, _ in self.transfer_list):
                        self.transfer_list.append((player, team))
                        print(f"{player.name} from {team.name} has been added to the transfer list.")

    def update_loan_list(self, teams):
        for team in teams:
            if random.random() < 0.1:  # 10% chance
                if team.squad:
                    player = random.choice(team.squad)
                    loan_fee = random.randint(5000, 50000)  # Weekly loan fee
                    loan_duration = random.randint(1, 20)  # 1 to 20 weeks
                    if not any(p == player for p, _, _, _ in self.loan_list):
                        self.loan_list.append((player, team, loan_fee, loan_duration))
                        print(f"{player.name} from {team.name} has been added to the loan list.")

    def buy_player(self, buying_team):
        print("\nAvailable players for transfer:")
        for i, (player, team) in enumerate(self.transfer_list, 1):
            print(f"{i}. {player.name} - {player.position.name} - Rating: {player.rating} - Age: {player.age} - Value: £{player.value:,} - Team: {team.name}")
            if player in self.bids:
                print(f"   (Bids: {len(self.bids[player])})")

        while True:
            try:
                choice = int(input("Enter the number of the player you want to bid for (0 to cancel): ")) - 1
                if choice == -1:
                    return False
                if 0 <= choice < len(self.transfer_list):
                    player, selling_team = self.transfer_list[choice]
                    if buying_team == selling_team:
                        print("You can't buy a player from your own team.")
                        return False
                    if buying_team.finances['bank_balance'] >= player.value:
                        if player not in self.bids:
                            self.bids[player] = []
                        self.bids[player].append((buying_team, player.value))
                        print(f"Transfer bid for {player.name} has been submitted. It will be processed at the end of the week.")
                        return True
                    else:
                        print("Insufficient funds to buy this player.")
                        return False
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    def sell_player(self, selling_team):
        print("\nYour squad:")
        for i, player in enumerate(selling_team.squad, 1):
            print(f"{i}. {player.name} - {player.position.name} - Rating: {player.rating} - Age: {player.age} - Value: £{player.value:,}")

        while True:
            try:
                choice = int(input("Enter the number of the player you want to sell (0 to cancel): ")) - 1
                if choice == -1:
                    return False
                if 0 <= choice < len(selling_team.squad):
                    player = selling_team.squad[choice]
                    self.transfer_list.append((player, selling_team))
                    print(f"{player.name} has been added to the transfer list.")
                    return True
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    def loan_player(self, loaning_team):
        print("\nAvailable players for loan:")
        for i, (player, team, loan_fee, duration) in enumerate(self.loan_list, 1):
            print(f"{i}. {player.name} - {player.position.name} - Rating: {player.rating} - Age: {player.age} - Loan Fee: £{loan_fee}/week - Duration: {duration} weeks - Team: {team.name}")

        while True:
            try:
                choice = int(input("Enter the number of the player you want to loan (0 to cancel): ")) - 1
                if choice == -1:
                    return False
                if 0 <= choice < len(self.loan_list):
                    player, team, loan_fee, duration = self.loan_list[choice]
                    if loaning_team == team:
                        print("You can't loan a player from your own team.")
                        return False
                    total_loan_cost = loan_fee * duration
                    if loaning_team.finances['bank_balance'] >= total_loan_cost:
                        self.pending_transfers.append(('loan', loaning_team, team, player, loan_fee, duration))
                        print(f"Loan offer for {player.name} has been submitted. It will be processed at the end of the week.")
                        return True
                    else:
                        print("Insufficient funds to loan this player.")
                        return False
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    def ai_transfer_actions(self, teams):
        for team in teams:
            if random.random() < 0.1:  # 10% chance for AI to perform a transfer action
                action = random.choice(['buy', 'sell', 'loan'])
                if action == 'buy' and self.transfer_list:
                    player, selling_team = random.choice(self.transfer_list)
                    if team != selling_team and team.finances['bank_balance'] >= player.value:
                        if player not in self.bids:
                            self.bids[player] = []
                        self.bids[player].append((team, player.value))
                        print(f"AI: {team.name} has submitted a transfer bid for {player.name} from {selling_team.name}")
                elif action == 'sell' and team.squad:
                    player = random.choice(team.squad)
                    if not any(p == player for p, _ in self.transfer_list):
                        self.transfer_list.append((player, team))
                        print(f"AI: {team.name} has put {player.name} on the transfer list")
                elif action == 'loan' and self.loan_list:
                    player, loaning_team, loan_fee, duration = random.choice(self.loan_list)
                    if team != loaning_team:
                        total_loan_cost = loan_fee * duration
                        if team.finances['bank_balance'] >= total_loan_cost:
                            self.pending_transfers.append(('loan', team, loaning_team, player, loan_fee, duration))
                            print(f"AI: {team.name} has submitted a loan offer for {player.name} from {loaning_team.name}")

    def process_transfers(self):
        print("\nProcessing transfers:")
        for player, bids in self.bids.items():
            if bids:
                winning_bid = random.choice(bids)
                buying_team, value = winning_bid
                selling_team = next(team for p, team in self.transfer_list if p == player)
                
                if player in selling_team.squad:
                    buying_team.finances['bank_balance'] -= value
                    selling_team.finances['bank_balance'] += value
                    buying_team.squad.append(player)
                    selling_team.squad.remove(player)
                    if player in selling_team.selected_players:
                        selling_team.selected_players.remove(player)
                    self.transfer_list = [(p, t) for p, t in self.transfer_list if p != player]
                    print(f"{player.name} has been transferred to {buying_team.name} from {selling_team.name} for £{value:,}")
                else:
                    print(f"Transfer of {player.name} to {buying_team.name} failed: Player not in {selling_team.name}'s squad.")

        self.bids.clear()

        for transfer in self.pending_transfers:
            if transfer[0] == 'loan':
                _, loaning_team, team, player, loan_fee, duration = transfer
                if player in team.squad:
                    total_loan_cost = loan_fee * duration
                    loaning_team.finances['bank_balance'] -= total_loan_cost
                    team.finances['bank_balance'] += total_loan_cost
                    loaning_team.squad.append(player)
                    team.squad.remove(player)
                    if player in team.selected_players:
                        team.selected_players.remove(player)
                    self.loan_list = [(p, t, f, d) for p, t, f, d in self.loan_list if p != player]
                    print(f"{player.name} has been loaned to {loaning_team.name} from {team.name} for {duration} weeks at £{loan_fee}/week")
                else:
                    print(f"Loan of {player.name} to {loaning_team.name} failed: Player not in {team.name}'s squad.")
        
        self.pending_transfers = []

def transfer_market_menu(player_team, transfer_market, teams):
    while True:
        print("\nTransfer Market Menu:")
        print("1. Buy Player")
        print("2. Sell Player")
        print("3. Loan Player")
        print("0. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            transfer_market.buy_player(player_team)
        elif choice == "2":
            transfer_market.sell_player(player_team)
        elif choice == "3":
            transfer_market.loan_player(player_team)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")

        # AI teams perform transfer actions
        transfer_market.ai_transfer_actions([team for team in teams if team != player_team])

# This function should be called every week in the main game loop
def update_transfer_market(transfer_market, teams):
    transfer_market.update_transfer_list(teams)
    transfer_market.update_loan_list(teams)
    transfer_market.process_transfers()