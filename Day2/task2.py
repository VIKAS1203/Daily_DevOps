import json
from datetime import datetime
from collections import defaultdict

# -------------------------------
# Configuration / Assumptions
# -------------------------------
S3_COST_PER_GB = 0.023  # USD per GB per month
TODAY = datetime.now()

# -------------------------------
# Load JSON
# -------------------------------
with open("buckets.json", "r") as f:
    data = json.load(f)

buckets = data["buckets"]

# -------------------------------
# Helper Functions
# -------------------------------
def days_since(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return (TODAY - date).days

# -------------------------------
# 1. Bucket Summary
# -------------------------------
print("\n=== Bucket Summary ===")
for b in buckets:
    print(
        f"Name: {b['name']}, "
        f"Region: {b['region']}, "
        f"Size: {b['sizeGB']} GB, "
        f"Versioning: {'Enabled' if b['versioning'] else 'Disabled'}"
    )

# -------------------------------
# 2. Buckets >80GB and Unused 90+ Days
# -------------------------------
print("\n=== Large & Unused Buckets (>80GB, 90+ days) ===")
large_unused = []

for b in buckets:
    unused_days = days_since(b["createdOn"])
    if b["sizeGB"] > 80 and unused_days >= 90:
        large_unused.append(b)
        print(
            f"{b['name']} | Region: {b['region']} | "
            f"Size: {b['sizeGB']} GB | Unused: {unused_days} days"
        )

# -------------------------------
# 3. Cost Report by Region & Department
# -------------------------------
print("\n=== Cost Report (Grouped by Region & Department) ===")

cost_report = defaultdict(lambda: defaultdict(float))
cleanup_recommendations = []
deletion_queue = []

for b in buckets:
    region = b["region"]
    department = b["tags"].get("team", "unknown")
    size = b["sizeGB"]
    cost = size * S3_COST_PER_GB

    cost_report[region][department] += cost

    unused_days = days_since(b["createdOn"])

    if size > 50:
        cleanup_recommendations.append(b["name"])

    if size > 100 and unused_days >= 20:
        deletion_queue.append(b)

# Print cost breakdown
for region, departments in cost_report.items():
    print(f"\nRegion: {region}")
    for dept, cost in departments.items():
        print(f"  Department: {dept} → ${cost:.2f}/month")

print("\nBuckets recommended for cleanup (Size > 50GB):")
for b in cleanup_recommendations:
    print(f" - {b}")

# -------------------------------
# 4. Final Deletion & Archival Recommendations
# -------------------------------
print("\n=== Deletion Queue ===")
for b in deletion_queue:
    print(
        f"{b['name']} | Size: {b['sizeGB']} GB | "
        f"Unused: {days_since(b['createdOn'])} days"
    )

print("\n=== Archival Candidates (Move to Glacier) ===")
for b in deletion_queue:
    print(f"{b['name']} → Recommend Glacier")

