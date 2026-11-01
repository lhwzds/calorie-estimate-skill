---
name: calorie-estimate
description: Estimate the calories and key nutrients of what someone ate and compare them with their own needs (Atwater energy, Mifflin-St Jeor BMR/TDEE, NASEM targets, nutrient adequacy). Use when a person describes or photographs meals and asks how much they ate, whether they are in a deficit, or what nutrients they are missing.
---

# Calorie estimate

A minimal skill: you turn the meal into grams and per-100 g nutrient values; `scripts/calc.py` does the arithmetic.

## Steps

1. **Person**: sex (`m`/`f`), age (adults 19–50), height cm, weight kg, activity (`sedentary`, `light`, `moderate`, `active`, `very_active`).
2. **Foods → grams.** If no weights are given, estimate and say so: cooked meat palm ≈ 100 g, cooked rice/potato fist ≈ 150 g, egg ≈ 50 g, 1 tbsp oil ≈ 13.5 g, 1 cup yogurt ≈ 170 g, 1 cup milk ≈ 245 g. Ask about oil, sauces, drinks and snacks, the usual missing calories.
3. **Nutrients per 100 g**: from the package label, else USDA FoodData Central (fdc.nal.usda.gov). Do not invent values you can look up; omit unknown nutrients rather than guessing (the script reports them as missing).
4. **Run** with a JSON file (or stdin):
   ```json
   {"person": {"sex": "f", "age": 35, "height_cm": 165, "weight_kg": 62, "activity": "moderate"},
    "foods": [{"name": "potato, boiled", "grams": 450,
               "per100g": {"kcal": 87, "protein": 1.87, "carbs": 20.1, "fat": 0.1, "fiber": 1.8,
                           "potassium": 379, "vit_c": 13}}]}
   ```
   `python3 scripts/calc.py day.json`. Keys: `kcal` (kcal), `protein carbs fat fiber alcohol satfat added_sugar` (g; `carbs` is total carbohydrate including fiber), `sodium calcium iron magnesium potassium zinc vit_c` (mg), `vit_a vit_d` (µg).
5. **Answer**: food table (grams, kcal, protein), total vs TDEE with the deficit, energy split, then the top 3 gaps or excesses, each with one concrete food fix. State your portion assumptions in one line. One day below a target is not a deficiency (targets apply to usual intake; fiber and potassium are Adequate Intakes): look at several days before calling a gap. Not for pregnancy, breastfeeding, children or medical diets; not medical advice.

## Formulas

**Energy**
- Amount eaten: `amount = per_100g × grams / 100`
- Food energy (general Atwater factors, fiber at 2 kcal/g): `kcal = 4·protein + 4·(carbs − fiber) + 2·fiber + 9·fat + 7·alcohol`; the label's kcal is used when given
- Energy split: `protein% = 4·P / kcal`, `carbs% = (4·(C − fiber) + 2·fiber) / kcal`, `fat% = 9·F / kcal`; healthy ranges 10–35 / 45–65 / 20–35 %
- Resting energy expenditure, used as BMR (Mifflin–St Jeor 1990): `10·kg + 6.25·cm − 5·age + 5` (men), `… − 161` (women)
- Daily need: `TDEE = BMR × activity` (1.2 / 1.375 / 1.55 / 1.725 / 1.9)
- Deficit: `TDEE − intake`; weekly loss ≈ `deficit × 7 / 7700` kg, a rough energy equivalent, not a prediction (real loss slows as weight drops)

**Nutrients**
- Coverage: `NAR_i = min(1, intake_i / target_i)`
- Adequacy score (MAR, Madden & Yoder 1976): `100 × mean(NAR_i)` over the 10 nutrients below; missing data counts as 0, so the script flags it
- Limits: saturated fat < 10 % kcal, added sugar < 10 % kcal (Dietary Guidelines 2020–2025), sodium ≤ 2300 mg

**Daily targets, adults 19–50 (NASEM DRIs)**

| | Men | Women |
| --- | --- | --- |
| Protein | 0.8 g/kg (1.2–1.6 g/kg is common when cutting with strength training) | 0.8 g/kg |
| Fiber | 14 g per 1000 kcal of TDEE | same |
| Calcium | 1000 mg | 1000 mg |
| Iron | 8 mg | 18 mg |
| Magnesium | 400 mg (19–30), 420 mg (31–50) | 310 mg, 320 mg |
| Potassium | 3400 mg | 2600 mg |
| Zinc | 11 mg | 8 mg |
| Vitamin A (RAE) | 900 µg | 700 µg |
| Vitamin C | 90 mg | 75 mg |
| Vitamin D | 15 µg | 15 µg |
