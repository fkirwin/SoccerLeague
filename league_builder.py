import csv
import sys


# Open CSV and read to a list.
# The list return contain each player stored in a dictionary.
def read_players_to_list(str_player_file_location):
    list_players = []
    with open(str_player_file_location) as players:
        try:
            player_reader = csv.DictReader(players)
            for row in player_reader:
                list_players.append(dict(row))
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(str_player_file_location, player_reader.line_num, e))
    return list_players


# Split players by experience.
# Keep adding to each team's roster until the experienced players have been distributed.
# Same for inexperienced.  Twist would be to reverse the order in case of odd number of kids.
def balance_league(str_player_file_location, dict_teams):
    experienced = []
    inexperienced = []
    rosters = list(dict_teams.values())

    for each in read_players_to_list(str_player_file_location):
        if each['Soccer Experience'].upper() == "YES":
            experienced.append(each)
        else:
            inexperienced.append(each)

    while experienced:
        for roster in rosters:
            roster.append(experienced.pop())

    while inexperienced:
        for roster in rosters[::-1]:
            roster.append(inexperienced.pop())


# Open the plain text file and write a team and its players.
# Move on to the next until all the teams/players are gone.
def write_rosters(str_team_file_loc, dict_teams):
    with open(str_team_file_loc, 'w+', newline='\n') as txtfile:
        try:
            for team_name, roster in dict_teams.items():
                txtfile.writelines(team_name + '\n')
                for player in roster:
                    txtfile.writelines("{}, {}, {}".format(player["Name"], player["Soccer Experience"],
                                                           player["Guardian Name(s)"]) + "\n")
        except Exception as e:
            sys.exit("{}".format(e))


# Generate a file for every player.
def generate_notifications(first_practice, dict_teams):
    try:
        for team_name, roster in dict_teams.items():
            for player in roster:
                with open(player["Name"] + ".txt", 'w+', newline='\n') as txtfile:
                    txtfile.writelines("Dear {}:\n" \
                                       "{} has been drafted by the {}.  First practice is {}.  See you there!"
                                       .format(player["Guardian Name(s)"], player["Name"], team_name, first_practice))
    except Exception as e:
        sys.exit("{}".format(e))


# Stage with args to allow future command line operations.
def run_league(*args):
    playerfile, teamfile, firstpractice, dict_teams = args
    try:
        balance_league(playerfile, dict_teams)
        write_rosters(teamfile, dict_teams)
        generate_notifications(firstpractice, dict_teams)
    except Exception as e:
        sys.exit("{}".format(e))
    else:
        print("Program ran successfully.")


if __name__ == '__main__':
    # Static targets...for now.
    PLAYERS_CSV = "soccer_players.csv"
    TEAMS_TXT = "teams.txt"
    FIRST_PRACTICE = "June 12 at 6PM"

    # Initialize teams with empty roster.
    # Roster is a list.  To be filled with player profiles
    teams = {"Sharks": [], "Dragons": [], "Raptors": []}

    run_league(PLAYERS_CSV, TEAMS_TXT, FIRST_PRACTICE, teams)
