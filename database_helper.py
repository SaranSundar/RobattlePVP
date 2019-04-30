import sqlite3


def robot_stats(robot_name):
    if not robot_name:
        return ()

    db_conn = sqlite3.connect("database.db")
    cmd = '''
            SELECT  robot_name, health,
                    primary_atk_damage, primary_atk_knockback, primary_atk_angle,
                    secondary_atk_damage, secondary_atk_knockback, secondary_atk_angle
            FROM    contestant
            WHERE   robot_name=\'{}\';
            '''.format(robot_name)
    return db_conn.cursor().execute(cmd).fetchone()


def arena_info():
    db_conn = sqlite3.connect("database.db")
    cmd = '''
            SELECT  arena_name, type
            FROM    arena
            WHERE   arena_name='Skyfall' OR arena_name='Kirby'
            '''
    return db_conn.cursor().execute(cmd).fetchall()


if __name__ == '__main__':
    arenas = arena_info()
    print(arenas)
    for robot in ['metabee', 'sumilidon', 'rokusho']:
        print(robot_stats(robot))
