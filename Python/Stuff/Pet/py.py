import sqlite3

with open("bugcat_capoo_12.png", "rb") as f : 
    data = f.read()


con = sqlite3.connect('src.db')
con.row_factory = sqlite3.Row
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS [Files]([Path] TEXT COLLATE NOCASE PRIMARY KEY, [Type] TEXT COLLATE NOCASE NOT NULL, [Content] BLOB NOT NULL)''')
cur.execute("INSERT OR REPLACE INTO [Files] VALUES (@Path, @Type, @Content)", {
    "Path": "/favicon.ico",
    "Type": "image/png",
    "Content": data
})

con.commit()
row = cur.execute("SELECT * FROM [Files] WHERE [Path]=@Path", {"Path": "/favicon.ico"}).fetchone()
print(row is None)
con.close()
