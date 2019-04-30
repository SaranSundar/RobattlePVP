import argparse
import datetime
import os
import random
import sqlite3

import lorem
import names
import petname


def count(db_connection):
    print('Displaying the number of records contained within each table:')
    table_list = db_connection.cursor().execute('SELECT name FROM sqlite_master WHERE type=\'table\' ORDER BY name;')
    count_cursor = db_connection.cursor()
    for result in table_list:
        record_count = count_cursor.execute('SELECT COUNT(*) FROM {};'.format(result[0])).fetchone()
        print('Table {:20} has {} records.'.format(result[0], record_count[0]))
    db_connection.commit()


def clear(db_connection):
    table_list = db_connection.cursor().execute('SELECT name FROM sqlite_master WHERE type=\'table\' ORDER BY name;')
    delete_cursor = db_connection.cursor()
    for result in table_list:
        print('Clearing table {}...'.format(result[0]))
        delete_cursor.execute('DELETE FROM {};'.format(result[0]))
    db_connection.commit()


def fill(db_connection):
    # Fill table ARENA
    venues = ['Arena', 'Stadium', 'Bowl', 'Dome', 'Colosseum', 'Field', 'Garden', 'Ground', 'Oval']
    arena_types = ['Fire', 'Water', 'Earth', 'Sky', 'Metal', 'Electricity']
    arena_entries = [(
        random.choice(['', 'The ']) + names.get_full_name() + ' ' + random.choice(venues),  # name
        random.choice(arena_types)  # type
    ) for _ in range(198)]
    arena_entries.append(('Skyfall', 'Earth'))
    arena_entries.append(('Kirby', 'Sky'))
    db_connection.cursor().executemany('INSERT INTO arena VALUES (?, ?)', arena_entries)
    print('Filled table ARENA...')

    # Fill table ARENA_RULES
    arena_rules_entries = [(
        arena_entries[int(i / 2)][0],  # Arena name fk
        lorem.sentence()  # Arena rules
    ) for i in range(400)]
    db_connection.cursor().executemany('INSERT INTO arena_rules VALUES (?, ?)', arena_rules_entries)
    print('Filled table ARENA_RULES...')

    # Fill CHIEF_ORGANIZER
    chief_organizer_entries = [(
        4,  # Authorization
        random.getrandbits(32),  # Employee ID
        names.get_first_name(),  # First name
        names.get_last_name(),  # Last name
        round(random.randrange(70000, 100000) / 500) * 500  # Salary
    ) for _ in range(200)]
    db_connection.cursor().executemany('INSERT INTO chief_organizer VALUES (?, ?, ?, ?, ?)', chief_organizer_entries)
    print('Filled table CHIEF_ORGANIZER...')

    # Fill REFEREE
    referee_entries = [(
        2,  # Authorization
        random.getrandbits(32),  # Employee ID
        names.get_first_name(),  # First name
        names.get_last_name(),  # Last name
        round(random.randrange(50000, 80000) / 500) * 500  # Salary
    ) for _ in range(200)]
    db_connection.cursor().executemany('INSERT INTO referee VALUES (?, ?, ?, ?, ?)', referee_entries)
    print('Filled table REFEREE...')

    # Fill TOURNAMENT
    formats = ['Single Elimination', 'Double Elimination', 'Multilevel', 'Straight Round Robin',
               'Round Robin Double Split', 'Round Robin Triple Split', 'Round Robin Quadruple Split',
               'Semi Round Robin', 'Ladder', 'Pyramid']
    tournament_entries = [(
        chief_organizer_entries[i][1],  # CHIEF_ORGANIZER_FK
        datetime.datetime.now() + datetime.timedelta(days=28 + random.random() * 56),  # END_DATE
        random.choice(formats),  # FORMAT
        random.randint(1, 500),  # MATCH_COUNT
        ' '.join([lorem.sentence() for _ in range(3)]),  # RULES
        datetime.datetime.now() + datetime.timedelta(days=random.random() * 14),  # START_DATE
        names.get_full_name() + '\'s ' + random.choice(['Tournament', 'Tourney', 'Championship'])  # TOURNAMENT_NAME
    ) for i in range(200)]
    db_connection.cursor().executemany('INSERT INTO tournament VALUES (?, ?, ?, ?, ?, ?, ?)', tournament_entries)
    print('Filled table TOURNAMENT...')

    # Fill TOURNAMENT_PRIZES
    prizes = ['Cash', 'Car', 'Robot', 'All You Can Eat Pass']
    tournament_prizes_entries = [(
        tournament_entries[i][6],
        random.choice(prizes)
    ) for i in range(200)]
    db_connection.cursor().executemany('INSERT INTO tournament_prizes VALUES (?, ?)', tournament_prizes_entries)
    print('Filled table TOURNAMENT_PRIZES...')

    # Fill GAME
    game_entries = [(
        arena_entries[random.randint(0, 199)][0],  # ARENA_NAME_FK
        datetime.datetime.now() + datetime.timedelta(days=14 + random.random() * 56),  # END_TIME
        random.getrandbits(32),  # GAME_ID
        0,  # PARTICIPATION_COUNT
        referee_entries[random.randint(0, 199)][1],  # REFEREE_FK
        datetime.datetime.now() + datetime.timedelta(days=14 + random.random() * 7),  # START_TIME
        tournament_entries[random.randint(0, 199)][6],  # TOURNAMENT_NAME_FK
    ) for _ in range(200)]
    db_connection.cursor().executemany('INSERT INTO game VALUES (?, ?, ?, ?, ?, ?, ?)', game_entries)
    print('Filled table GAME...')

    # Fill ATTENDEE
    attendee_entries = [(
        names.get_first_name(),  # FIRST_NAME
        names.get_last_name(),  # LAST_NAME
        game_entries[random.randint(0, 199)][2],  # GAME_ID_FK
        random.getrandbits(32),  # TICKET_NUMBER
    ) for _ in range(2000)]
    db_connection.cursor().executemany('INSERT INTO attendee VALUES (?, ?, ?, ?)', attendee_entries)
    print('Filled table ATTENDEE...')

    # Fill CONCESSIONS_VENDOR
    concessions_vendor_entries = [(
        2,  # AUTHORIZATION
        random.getrandbits(32),  # EMPLOYEE_ID
        names.get_first_name(),  # FIRST_NAME
        names.get_last_name(),  # LAST_NAME
        round(random.randrange(40000, 60000) / 500) * 500,  # Salary
        attendee_entries[random.randint(0, 999)][3]  # TICKET_NUMBER_FK
    ) for _ in range(200)]
    db_connection.cursor().executemany('INSERT INTO concessions_vendor VALUES (?, ?, ?, ?, ?, ?)',
                                       concessions_vendor_entries)
    print('Filled table CONCESSIONS_VENDOR...')

    # Fill TICKET_VENDOR
    ticket_vendor_entries = [(
        2,  # AUTHORIZATION
        random.getrandbits(32),  # EMPLOYEE_ID
        names.get_first_name(),  # FIRST_NAME
        names.get_last_name(),  # LAST_NAME
        round(random.randrange(40000, 50000) / 500) * 500,  # Salary
        attendee_entries[random.randint(0, 999)][3]  # TICKET_NUMBER_FK
    ) for _ in range(200)]
    db_connection.cursor().executemany('INSERT INTO ticket_vendor VALUES (?, ?, ?, ?, ?, ?)',
                                       ticket_vendor_entries)
    print('Filled table TICKET_VENDOR...')

    # Fill CONTESTANT
    robot_models = ['Tank', 'Hunter', 'Tactical']
    normal_attacks = ['Punch', 'Kick', 'Scratch']
    special_attacks = ['Body Slam', 'Uppercut', 'Ram']
    titles = ['Champion', 'Contender', 'Star', 'Rising Star', 'Mythic']
    contestant_entries = [(
        random.randint(1, 100),  # DEFENSE
        names.get_first_name(),  # FIRST_NAME
        100,  # HEALTH
        names.get_last_name(),  # LAST_NAME
        1,  # LOSSES
        2,  # GAMES_PLAYED
        game_entries[random.randint(0, 199)][2],  # GAME_ID_FK
        random.choice(robot_models),  # MODEL
        random.choice(normal_attacks),  # NORMAL_ATTACK
        random.randint(1, 10),  # PRIMARY_ATK_DAMAGE
        random.randint(1, 5),  # PRIMARY_ATK_KNOCKBACK
        random.randint(15, 75),  # PRIMARY_ATK_ANGLE
        random.getrandbits(32),  # ROBOT_LICENSE
        petname.generate(separator=' ').title(),  # ROBOT_NAME
        random.randint(3, 15),  # SECONDARY_ATK_DAMAGE
        random.randint(2, 8),  # SECONDARY_ATK_KNOCKBACK
        random.randint(15, 75),  # SECONDARY_ATK_ANGLE
        random.getrandbits(32),  # SERIAL_NUMBER
        random.choice(special_attacks),  # SPECIAL_ATTACK
        random.randint(1, 100),  # SPEED
        random.choice(titles),  # TITLE
        random.randint(1, 100),  # WEIGHT
        1,  # WINS
    ) for _ in range(200)]
    db_connection.cursor().executemany('INSERT INTO contestant VALUES \
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', contestant_entries)
    print('Filled table CONTESTANT...')

    # Fill RECEPTIONIST
    receptionist_entries = [(
        2,  # AUTHORIZATION
        random.getrandbits(32),  # EMPLOYEE_ID
        names.get_first_name(),  # FIRST_NAME
        names.get_last_name(),  # LAST_NAME
        contestant_entries[random.randint(0, 199)][12],  # ROBOT_LICENSE_FK
        round(random.randrange(40000, 60000) / 500) * 500  # Salary
    ) for _ in range(200)]
    db_connection.cursor().executemany('INSERT INTO receptionist VALUES (?, ?, ?, ?, ?, ?)', receptionist_entries)
    print('Filled table RECEPTIONIST...')

    # Fill BATTLE
    for key_1 in range(200):
        key_2 = random.randint(0, 199)
        while key_1 == key_2:
            key_2 = random.randint(0, 199)
        cmd = 'INSERT INTO battle VALUES (' + str(contestant_entries[key_1][12]) + ', ' \
              + str(contestant_entries[key_2][12]) + ')'
        db_connection.cursor().execute(cmd)
    print('Filled table BATTLE...')

    # Set specific robot names
    contestant_id = db_connection.cursor().execute('SELECT robot_license FROM contestant LIMIT 3;').fetchall()
    cmd = '''
        UPDATE  contestant
        SET     robot_name=\'sumilidon\',
                primary_atk_knockback=200,
                primary_atk_damage=7,
                primary_atk_angle=360,
                secondary_atk_knockback=500,
                secondary_atk_damage=15,
                secondary_atk_angle=8
        WHERE   robot_license={}
        '''.format(contestant_id[0][0])
    db_connection.cursor().execute(cmd)
    cmd = '''
        UPDATE  contestant
        SET     robot_name=\'metabee\',
                primary_atk_knockback=500,
                primary_atk_damage=12,
                primary_atk_angle=8,
                secondary_atk_knockback=200,
                secondary_atk_damage=9,
                secondary_atk_angle=4
        WHERE   robot_license={}
        '''.format(contestant_id[1][0])
    db_connection.cursor().execute(cmd)
    cmd = 'UPDATE contestant SET robot_name=\'rokusho\' WHERE robot_license={}'.format(contestant_id[2][0])
    db_connection.cursor().execute(cmd)

    db_connection.commit()


def sample(db_connection):
    print('Displaying sample tuples of all tables. Primary keys indicated via \'PK\'.\n')
    table_list = db_connection.cursor().execute('SELECT name FROM sqlite_master WHERE type=\'table\' ORDER BY name;')
    select_cursor = db_connection.cursor()
    for table in table_list:
        print('Table: {}'.format(table[0]))
        print('=' * (len(table[0]) + 10))
        record = select_cursor.execute('SELECT * FROM {} LIMIT 1;'.format(table[0])).fetchone()
        attributes = select_cursor.execute('PRAGMA table_info({})'.format(table[0])).fetchall()
        for column in attributes:
            print('{:30} | {:40.40} | {}'.format(
                column[1], str(record[column[0]]), '' if column[5] == 0 else 'PK',
            ))
        print()


def query(db_connection):
    print('Query Examples:')

    # Largest population count
    print('How many people are currently watching a battle?')
    print('SQL Query:   SELECT COUNT(*) FROM attendee;')
    attendees = db_connection.cursor().execute('SELECT COUNT(*) FROM attendee;').fetchone()[0]
    print(attendees)
    print()

    # Listing of a key entity
    print('Who is competing in a battle? Name 10 such individuals.')
    print('SQL Query:   SELECT first_name, last_name FROM contestant LIMIT 10;')
    contestants = db_connection.cursor().execute('SELECT first_name, last_name FROM contestant LIMIT 10;').fetchall()
    for contestant in contestants:
        print('{:10.10} |  {}'.format(contestant[0], contestant[1]))
    print()

    # Join
    print('What rules are associated with which arenas? Show 10 such rules.')
    sql_join_query = 'SELECT arena_name, arena_rules.arena_rules FROM arena ' + \
                     'INNER JOIN arena_rules ON arena_name=arena_name_fk LIMIT 10;'
    print('SQL Query:   {}'.format(sql_join_query))
    arenas = db_connection.cursor().execute(sql_join_query).fetchall()
    for row in arenas:
        print('{:20}  |  {}'.format(row[0], row[1]))
    print()

    # Aggregate Function
    print('What is the average salary among all chief organizers?')
    avg_salary = db_connection.cursor().execute('SELECT AVG(salary) FROM chief_organizer;').fetchone()[0]
    print('${:08.2f}'.format(avg_salary))
    print()

    # Nested Query
    print('Display salaries of all referees and chief organizers in ascending order, alongside their names and IDs:')
    sql_union_query = 'SELECT employee_id, first_name, last_name, salary FROM ' + \
                      '(SELECT * from referee UNION SELECT * FROM chief_organizer) ORDER BY salary;'
    print('SQL Query:   {}'.format(sql_union_query))
    salaries = db_connection.cursor().execute(sql_union_query).fetchall()
    for row in salaries:
        print('{:13d}  |  {:12}  |  {:12}  |  ${:7d}'.format(row[0], row[1], row[2], row[3]))
    print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SQL scripts to manipulate Skyline\'s database.')
    parser.add_argument('action', choices=['fill', 'clear', 'count', 'sample', 'query'])
    parser.add_argument('database')
    arguments = parser.parse_args()

    if not os.path.isfile(arguments.database):
        print('Error: database file \'{}\' does not exist.'.format(arguments.database))
    else:
        db_conn = sqlite3.connect(arguments.database)
        if arguments.action == 'fill':
            fill(db_connection=db_conn)

        elif arguments.action == 'clear':
            clear(db_connection=db_conn)

        elif arguments.action == 'count':
            count(db_connection=db_conn)

        elif arguments.action == 'sample':
            sample(db_connection=db_conn)

        elif arguments.action == 'query':
            query(db_connection=db_conn)

        db_conn.close()
