import requests
from bs4 import BeautifulSoup
import sqlite3
import time

DB_NAME = "../data/nhl_drafts_raw.db"
START_YEAR = 2005
END_YEAR = 2017

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def scrape_draft_year(year):
    url = f"https://www.hockeydb.com/ihdb/draft/nhl{year}e.html"
    print(f"Scraping {year}... ({url})")

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"  WARNING: Failed to fetch {year} — {e}. Skipping.")
        return []

    try:
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="sortable")

        if not table:
            print(f"  WARNING: No table found for {year}. Skipping.")
            return []

        rows = table.find_all("tr")
        picks = []

        for row in rows:
            if "hideme" in row.get("class", []):
                continue

            cells = row.find_all("td")
            if len(cells) < 4:
                continue

            round_num = cells[0].text.strip()
            pick_num = cells[1].text.strip()
            team = cells[2].text.strip()
            player = cells[3].text.strip()
            pos = cells[4].text.strip() if len(cells) > 4 else None
            drafted_from = cells[5].text.strip() if len(cells) > 5 else None
            gp = cells[6].text.strip() if len(cells) > 6 else None
            goals = cells[7].text.strip() if len(cells) > 7 else None
            assists = cells[8].text.strip() if len(cells) > 8 else None
            points = cells[9].text.strip() if len(cells) > 9 else None
            pim = cells[10].text.strip() if len(cells) > 10 else None
            last_season = cells[11].text.strip() if len(cells) > 11 else None

            # Convert numeric fields to int where possible, else None
            def to_int(val):
                try:
                    return int(val)
                except (TypeError, ValueError):
                    return None

            picks.append(
                {
                    "draft_year": year,
                    "round": to_int(round_num),
                    "pick_number": to_int(pick_num),
                    "drafted_by": team,
                    "player_name": player,
                    "position": pos,
                    "drafted_from": drafted_from,
                    "games_played": to_int(gp),
                    "goals": to_int(goals),
                    "assists": to_int(assists),
                    "points": to_int(points),
                    "penalty_minutes": to_int(pim),
                    "last_season": last_season,
                }
            )

        print(f"  Found {len(picks)} players.")
        return picks

    except Exception as e:
        print(f"  WARNING: Error parsing {year} — {e}. Skipping.")
        return []


def init_db(conn):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS nhl_draft_picks")
    cursor.execute(
        """
        CREATE TABLE nhl_draft_picks (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            draft_year       INTEGER,
            round            INTEGER,
            pick_number      INTEGER,
            drafted_by       TEXT,
            player_name      TEXT,
            position         TEXT,
            drafted_from     TEXT,
            games_played     INTEGER,
            goals            INTEGER,
            assists          INTEGER,
            points           INTEGER,
            penalty_minutes  INTEGER,
            last_season      TEXT
        )
    """
    )
    conn.commit()
    print(f"Database '{DB_NAME}' initialized.\n")


def insert_picks(conn, picks):
    cursor = conn.cursor()
    cursor.executemany(
        """
        INSERT INTO nhl_draft_picks (
            draft_year, round, pick_number, drafted_by, player_name,
            position, drafted_from, games_played, goals, assists,
            points, penalty_minutes, last_season
        ) VALUES (
            :draft_year, :round, :pick_number, :drafted_by, :player_name,
            :position, :drafted_from, :games_played, :goals, :assists,
            :points, :penalty_minutes, :last_season
        )
    """,
        picks,
    )
    conn.commit()


def main():
    conn = sqlite3.connect(DB_NAME)
    init_db(conn)

    total_players = 0

    for year in range(START_YEAR, END_YEAR + 1):
        picks = scrape_draft_year(year)

        if picks:
            insert_picks(conn, picks)
            total_players += len(picks)

        time.sleep(1.5)  # Be polite to the server

    conn.close()
    print(f"\nDone! {total_players} players inserted into '{DB_NAME}'.")


if __name__ == "__main__":
    main()
