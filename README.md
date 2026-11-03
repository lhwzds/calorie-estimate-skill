# calorie-estimate-skill

A minimal [Agent Skill](https://agentskills.io) that estimates the calories and key nutrients of what someone ate and compares them with that person's own needs.

- `SKILL.md`: the steps and every formula (Atwater food energy, Mifflin-St Jeor BMR, TDEE, deficit, nutrient adequacy) plus the NASEM daily targets for adults 19-50.
- `scripts/calc.py`: the arithmetic. Python 3 standard library only, no network.

The agent turns a meal into grams and per-100 g nutrient values (from the label or [USDA FoodData Central](https://fdc.nal.usda.gov)); the script does the math.

## Install

Copy this folder into your agent's skills directory, for example:

```sh
git clone https://github.com/lhwzds/calorie-estimate-skill ~/.claude/skills/calorie-estimate
```

## Run it directly

```sh
python3 scripts/calc.py examples/day.json
```

```
food                             g    kcal  protein
potato, boiled                 450     392     8.4g
broccoli, boiled               300     105     7.1g
chicken breast, roasted        250     412    77.5g
olive oil                       27     239     0.0g

Total 1148 kcal | need (TDEE) 2039 | deficit 891 (~0.81 kg/week by the rough 7700 kcal/kg rule)
Energy split: protein 32% (10-35) | carbs 36% (45-65) | fat 29% (20-35)

Nutrient      intake / target   coverage
ok  protein       93.1 / 50     g     188%
LOW fiber         18.0 / 29     g      63%
LOW magnesium    234.5 / 320    mg     73%
LOW calcium      180.3 / 1000   mg     18%
LOW iron           6.2 / 18     mg     34%
ok  potassium   3224.8 / 2600   mg    124%
LOW zinc           5.2 / 8      mg     65%
LOW vit_a        246.0 / 700    µg     35%
ok  vit_c        253.2 / 75     mg    338%
LOW vit_d          0.2 / 15     µg      2%

Adequacy score (MAR): 59/100
ok  satfat          5.2 % kcal (limit < 10)
ok  added_sugar     0.0 % kcal (limit < 10)
ok  sodium        326.5 mg (limit <= 2300)
```

The example values come from USDA FoodData Central (SR Legacy).

Estimates only; not medical or clinical dietary advice.

## License

MIT
