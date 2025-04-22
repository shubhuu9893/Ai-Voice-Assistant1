import sqlite3

def setup_database():
    con = sqlite3.connect("jarvis.db")
    cursor = con.cursor()

    # Create tables if they don't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))")
    cursor.execute("CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))")

    # Add some basic system commands
    system_commands = [
        ('notepad', 'notepad.exe'),
        ('calculator', 'calc.exe'),
        ('chrome', 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'),
        ('edge', 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'),
        ('explorer', 'explorer.exe'),
        ('cmd', 'cmd.exe'),
        ('task manager', 'taskmgr.exe'),
        ('control panel', 'control.exe'),
        ('paint', 'mspaint.exe'),
        ('word', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE'),
        ('excel', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE'),
        ('powerpoint', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE'),
    ]

    # Add some web commands
    web_commands = [
        ('youtube', 'https://www.youtube.com'),
        ('google', 'https://www.google.com'),
        ('gmail', 'https://mail.google.com'),
        ('facebook', 'https://www.facebook.com'),
        ('twitter', 'https://twitter.com'),
        ('linkedin', 'https://www.linkedin.com'),
        ('github', 'https://github.com'),
        ('stackoverflow', 'https://stackoverflow.com'),
    ]

    # Insert system commands
    for name, path in system_commands:
        try:
            cursor.execute("INSERT OR IGNORE INTO sys_command (name, path) VALUES (?, ?)", (name, path))
        except:
            print(f"Could not add {name}")

    # Insert web commands
    for name, url in web_commands:
        try:
            cursor.execute("INSERT OR IGNORE INTO web_command (name, url) VALUES (?, ?)", (name, url))
        except:
            print(f"Could not add {name}")

    con.commit()
    con.close()





if __name__ == "__main__":
    setup_database()
    print("Database setup completed!") 