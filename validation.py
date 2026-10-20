import csv

FIELDS = {
    "HasRecovered": "HasRecovered",
    "WhyRecovered": "WhyRecovered",
    "Activity": "ncommits",
    "Pattern": "ActivityPattern",
    "Currentstatus": "Currentstatus",
    "RecentThemes": "RecentThemes",
}

with open("demarco-miniproject2/ddemarco_project_stats.csv", encoding="utf-8-sig") as f:
    stats = {r["Project"]: r for r in csv.DictReader(f, delimiter=";")}

with open("econstan_netid_validation_log.csv", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f, delimiter=";")
    columns = reader.fieldnames
    rows = list(reader)

for row in rows:
    s = stats[row["WOCProjectID"]]
    field = row["Field"]

    row["ProjectOwnerNetID"] = "ddemarco"
    row["ValidatorNetID"] = "econstan"
    row["AuthorValue"] = s[FIELDS[field]]

    row["KeyEvidence"] = (
        f"{s['ncommits']} commits, {s['nauthors']} authors; "
        f"longest gap {s['LongestGapStart']} to {s['LongestGapEnd']} "
        f"({s['LongestGapLength']} months); "
        f"{s['NumCommitsAfterLastGap']} commits after gap; "
        f"pattern {s['ActivityPattern']}; "
        f"last sampled commit {s['to']}; "
        f"last GitHub commit {s['lastGHCommitDate']}."
    )

    if field == "RecentThemes":
        row["KeyEvidence"] += f" Recent themes: {s['RecentThemes']}."

    if field == "WhyRecovered":
        row["KeyEvidence"] += (
            f" Before: {s['BeforeThemes']}; after: {s['AfterThemes']}."
        )

    row["PreDiscussAgreementstatus(Yes/No)"] = (
        "Yes" if row["AuthorValue"].strip().casefold()
        == row["ValidatorValue"].strip().casefold()
        else "No"
    ) if row["ValidatorValue"].strip() else ""

with open("econstan_validation_log.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=columns, delimiter=";")
    writer.writeheader()
    writer.writerows(rows)