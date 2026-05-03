import pandas as pd
import time
import ssl
import os
import random
import requests


def get_html(url, team_abbr):
    """Fetch HTML with headers + caching"""
    cache_dir = "../data/cache"
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = f"{cache_dir}/{team_abbr}.html"

    # Use cached version if available
    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            return f.read()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    html = response.text

    # Save to cache
    with open(cache_path, "w", encoding="utf-8") as f:
        f.write(html)

    return html


def fetch_tables(url, team_abbr, max_retries=5):
    """Retry logic with exponential backoff"""
    for attempt in range(max_retries):
        try:
            html = get_html(url, team_abbr)
            return pd.read_html(html)

        except Exception as e:
            if "429" in str(e):
                wait = (2**attempt) + random.uniform(1, 3)
                print(f"⏳ Rate limited for {team_abbr}. Retrying in {wait:.2f}s...")
                time.sleep(wait)
            else:
                raise e

    raise Exception(f"Max retries exceeded for {team_abbr}")


def scrape_performance():
    # Setup SSL and Directory
    ssl._create_default_https_context = ssl._create_unverified_context
    os.makedirs("../data", exist_ok=True)

    teams = [
        "ANA",
        "ARI",
        "BOS",
        "BUF",
        "CGY",
        "CAR",
        "CHI",
        "COL",
        "CBJ",
        "DAL",
        "DET",
        "EDM",
        "FLA",
        "LAK",
        "MIN",
        "MTL",
        "NSH",
        "NJD",
        "NYI",
        "NYR",
        "OTT",
        "PHI",
        "PIT",
        "SJS",
        "STL",
        "TBL",
        "TOR",
        "VAN",
        "WPG",
        "WSH",
    ]

    custom_url_ids = {"ARI": "PHX"}
    raw_records = []

    print("🚀 Starting NHL Scraping (2005-2024)...")

    for team_abbr in teams:
        url_id = custom_url_ids.get(team_abbr, team_abbr)
        url = f"https://www.hockey-reference.com/teams/{url_id}/history.html"

        try:
            try:
                tables = fetch_tables(url, team_abbr)
            except:
                url = f"https://www.hockey-reference.com/teams/{url_id}/"
                tables = fetch_tables(url, team_abbr)

            df = tables[0]

            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(-1)

            # Rename columns by position
            df = df.rename(
                columns={
                    df.columns[0]: "Season",
                    df.columns[3]: "GP",
                    df.columns[4]: "W",
                    df.columns[13]: "Playoff_Result",
                }
            )

            # Filter seasons
            df = df[df["Season"].str.contains("-", na=False)].copy()
            df["Season_Start"] = df["Season"].str[:4].astype(int)

            window = df[
                (df["Season_Start"] >= 2005) & (df["Season_Start"] <= 2024)
            ].copy()

            for _, row in window.iterrows():
                raw_records.append(
                    {
                        "Abbr": team_abbr,
                        "Season": row["Season"],
                        "GP": row["GP"],
                        "W": row["W"],
                        "Playoff_Result": row["Playoff_Result"],
                    }
                )

            print(f"✅ Extracted: {team_abbr}")

            # Random delay to avoid rate limiting
            time.sleep(random.uniform(2.5, 5))

        except Exception as e:
            print(f"❌ Failed {team_abbr}: {e}")

    # Save results
    performance_df = pd.DataFrame(raw_records)
    performance_df.to_csv("../data/nhl_performance.csv", index=False)

    print("\n💾 Success! File saved to: data/nhl_performance.csv")


if __name__ == "__main__":
    scrape_performance()

# import pandas as pd
# import time
# import ssl
# import os


# def scrape_performance():
#     # Setup SSL and Directory
#     ssl._create_default_https_context = ssl._create_unverified_context
#     if not os.path.exists("../data"):
#         os.makedirs("../data")

#     teams = [
#         "ANA",
#         "ARI",
#         "BOS",
#         "BUF",
#         "CGY",
#         "CAR",
#         "CHI",
#         "COL",
#         "CBJ",
#         "DAL",
#         "DET",
#         "EDM",
#         "FLA",
#         "LAK",
#         "MIN",
#         "MTL",
#         "NSH",
#         "NJD",
#         "NYI",
#         "NYR",
#         "OTT",
#         "PHI",
#         "PIT",
#         "SJS",
#         "STL",
#         "TBL",
#         "TOR",
#         "VAN",
#         "WPG",
#         "WSH",
#     ]

#     custom_url_ids = {"ARI": "PHX"}
#     raw_records = []

#     print("🚀 Starting NHL Scraping (2005-2017)...")

#     for team_abbr in teams:
#         url_id = custom_url_ids.get(team_abbr, team_abbr)
#         url = f"https://www.hockey-reference.com/teams/{url_id}/history.html"

#         try:
#             try:
#                 tables = pd.read_html(url)
#             except:
#                 url = f"https://www.hockey-reference.com/teams/{url_id}/"
#                 tables = pd.read_html(url)

#             df = tables[0]
#             if isinstance(df.columns, pd.MultiIndex):
#                 df.columns = df.columns.get_level_values(-1)

#             # Map columns by position to stay robust
#             df = df.rename(
#                 columns={
#                     df.columns[0]: "Season",
#                     df.columns[3]: "GP",
#                     df.columns[4]: "W",
#                     df.columns[13]: "Playoff_Result",
#                 }
#             )

#             # Filter for the 2005-2017 window
#             df = df[df["Season"].str.contains("-", na=False)].copy()
#             df["Season_Start"] = df["Season"].str[:4].astype(int)
#             window = df[
#                 (df["Season_Start"] >= 2005) & (df["Season_Start"] <= 2024)
#             ].copy()

#             # Store every single season for that team
#             for _, row in window.iterrows():
#                 raw_records.append(
#                     {
#                         "Abbr": team_abbr,
#                         "Season": row["Season"],
#                         "GP": row["GP"],
#                         "W": row["W"],
#                         "Playoff_Result": row["Playoff_Result"],
#                     }
#                 )

#             print(f"✅ Extracted: {team_abbr}")
#             time.sleep(1.5)

#         except Exception as e:
#             print(f"❌ Failed {team_abbr}: {e}")

#     # Create DataFrame and save to data/
#     performance_df = pd.DataFrame(raw_records)
#     performance_df.to_csv("../data/nhl_performance.csv", index=False)
#     print("\n💾 Success! File saved to: data/nhl_performance.csv")


# if __name__ == "__main__":
#     scrape_performance()
