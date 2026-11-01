#!/usr/bin/env python3
"""Calories and key nutrients of a day's food vs the person's needs.

Usage: python3 calc.py day.json      (or pipe the JSON on stdin)
Input:  {"person": {"sex": "m", "age": 26, "height_cm": 180, "weight_kg": 87, "activity": "light"},
         "foods": [{"name": "potato, boiled", "grams": 450,
                    "per100g": {"kcal": 87, "protein": 1.9, "carbs": 20, "fat": 0.1, "fiber": 1.8, ...}}]}
Nutrient keys and units are listed in UNITS; leave out what you don't know (it shows as missing).
"""
import json
import sys

ACTIVITY = {"sedentary": 1.2, "light": 1.375, "moderate": 1.55, "active": 1.725, "very_active": 1.9}

UNITS = {"kcal": "kcal", "protein": "g", "carbs": "g", "fat": "g", "fiber": "g", "satfat": "g",
         "added_sugar": "g", "sodium": "mg", "calcium": "mg", "iron": "mg", "magnesium": "mg",
         "potassium": "mg", "zinc": "mg", "vit_a": "µg", "vit_c": "mg", "vit_d": "µg"}

# NASEM daily targets for adults 19-50 (men, women). Protein, fiber and magnesium depend on the person.
TARGETS = {"calcium": (1000, 1000), "iron": (8, 18), "potassium": (3400, 2600),
           "zinc": (11, 8), "vit_a": (900, 700), "vit_c": (90, 75), "vit_d": (15, 15)}


def bmr(sex, kg, cm, age):
    """Mifflin-St Jeor."""
    return 10 * kg + 6.25 * cm - 5 * age + (5 if sex == "m" else -161)


def atwater(n):
    fiber = n.get("fiber", 0)
    return 4 * n.get("protein", 0) + 4 * max(n.get("carbs", 0) - fiber, 0) + 2 * fiber + 9 * n.get("fat", 0)


def main():
    day = json.load(open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin)
    p = day["person"]
    tdee = bmr(p["sex"], p["weight_kg"], p["height_cm"], p["age"]) * ACTIVITY[p.get("activity", "sedentary")]

    total, missing = {k: 0.0 for k in UNITS}, {k: [] for k in UNITS}
    print(f"{'food':<28}{'g':>6}{'kcal':>8}{'protein':>9}")
    for f in day["foods"]:
        n = {k: v * f["grams"] / 100 for k, v in f["per100g"].items()}
        n["kcal"] = n.get("kcal", atwater(n))  # label energy first, else Atwater
        for k in UNITS:
            if k in n:
                total[k] += n[k]
            elif k != "kcal":
                missing[k].append(f["name"])
        print(f"{f['name']:<28}{f['grams']:>6.0f}{n['kcal']:>8.0f}{n.get('protein', 0):>8.1f}g")

    kcal = total["kcal"] or 1
    print(f"\nTotal {total['kcal']:.0f} kcal | need (TDEE) {tdee:.0f} | deficit {tdee - total['kcal']:.0f}"
          f" -> about {(tdee - total['kcal']) * 7 / 7700:.2f} kg/week")
    print(f"Energy split: protein {400 * total['protein'] / kcal:.0f}% (10-35) | "
          f"carbs {400 * max(total['carbs'] - total['fiber'], 0) / kcal:.0f}% (45-65) | fat {900 * total['fat'] / kcal:.0f}% (20-35)")

    sex = 0 if p["sex"] == "m" else 1
    targets = {"protein": 0.8 * p["weight_kg"], "fiber": 14 * tdee / 1000}
    targets["magnesium"] = (400, 310)[sex] if p["age"] <= 30 else (420, 320)[sex]
    targets.update({k: v[sex] for k, v in TARGETS.items()})
    nar = []
    print("\nNutrient      intake / target   coverage")
    for k, t in targets.items():
        nar.append(min(1, total[k] / t))
        gap = f"  (no data: {', '.join(missing[k])})" if missing[k] else ""
        print(f"{'ok ' if total[k] >= t else 'LOW'} {k:<10}{total[k]:>8.1f} / {t:<7.0f}{UNITS[k]:<4}"
              f"{100 * total[k] / t:>5.0f}%{gap}")
    print(f"\nAdequacy score (MAR): {100 * sum(nar) / len(nar):.0f}/100")

    limits = [("satfat", 100 * 9 * total["satfat"] / kcal, 10, "% kcal"),
              ("added_sugar", 100 * 4 * total["added_sugar"] / kcal, 10, "% kcal"),
              ("sodium", total["sodium"], 2300, "mg")]
    for k, value, limit, unit in limits:
        print(f"{'ok ' if value <= limit else 'MAX'} {k:<12}{value:>7.1f} {unit} (limit {limit})")


if __name__ == "__main__":
    main()
