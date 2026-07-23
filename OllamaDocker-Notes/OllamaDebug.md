Debuging
---

After running for the first time after integrating Ollama, this was the output:

```
/Users/sebastiandorata/PycharmProjects/4020AIServer/.venv/bin/python /Users/sebastiandorata/PycharmProjects/4020AIServer/main.py 
 * Serving Flask app 'main'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5001
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: *********
127.0.0.1 - - [23/Jul/2026 13:35:00] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [23/Jul/2026 13:35:00] "GET /static/js/scripts.js HTTP/1.1" 200 -
127.0.0.1 - - [23/Jul/2026 13:35:00] "GET /static/css/styles.css HTTP/1.1" 200 -
127.0.0.1 - - [23/Jul/2026 13:35:01] "GET /static/assets/img/bg_nutrition.png HTTP/1.1" 200 -
127.0.0.1 - - [23/Jul/2026 13:35:01] "GET /static/assets/favicon.ico HTTP/1.1" 404 -
127.0.0.1 - - [23/Jul/2026 13:35:46] "POST / HTTP/1.1" 500 -
Traceback (most recent call last):
  File "/Users/sebastiandorata/PycharmProjects/4020AIServer/.venv/lib/python3.14/site-packages/flask/app.py", line 1536, in __call__
    return self.wsgi_app(environ, start_response)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/sebastiandorata/PycharmProjects/4020AIServer/.venv/lib/python3.14/site-packages/flask/app.py", line 1514, in wsgi_app
    response = self.handle_exception(e)
  File "/Users/sebastiandorata/PycharmProjects/4020AIServer/.venv/lib/python3.14/site-packages/flask/app.py", line 1511, in wsgi_app
    response = self.full_dispatch_request()
  File "/Users/sebastiandorata/PycharmProjects/4020AIServer/.venv/lib/python3.14/site-packages/flask/app.py", line 919, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/Users/sebastiandorata/PycharmProjects/4020AIServer/.venv/lib/python3.14/site-packages/flask/app.py", line 917, in full_dispatch_request
    rv = self.dispatch_request()
  File "/Users/sebastiandorata/PycharmProjects/4020AIServer/.venv/lib/python3.14/site-packages/flask/app.py", line 902, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/Users/sebastiandorata/PycharmProjects/4020AIServer/routes.py", line 178, in home
    return render_template(
    
  File "/Users/sebastiandorata/PycharmProjects/4020AIServer/.venv/lib/python3.14/site-packages/flask/templating.py", line 151, in render_template
    return _render(app, template, context)
  File "/Users/sebastiandorata/PycharmProjects/4020AIServer/.venv/lib/python3.14/site-packages/flask/templating.py", line 132, in _render
    rv = template.render(context)
  File "/Users/sebastiandorata/PycharmProjects/4020AIServer/.venv/lib/python3.14/site-packages/jinja2/environment.py", line 1295, in render
    self.environment.handle_exception()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/Users/sebastiandorata/PycharmProjects/4020AIServer/.venv/lib/python3.14/site-packages/jinja2/environment.py", line 942, in handle_exception
    raise rewrite_traceback_stack(source=source)
  File "/Users/sebastiandorata/PycharmProjects/4020AIServer/templates/result.html", line 152, in top-level template code
    {% for food in meal.nutrition.foods %}
    
  File "/Users/sebastiandorata/PycharmProjects/4020AIServer/.venv/lib/python3.14/site-packages/jinja2/environment.py", line 490, in getattr
    return getattr(obj, attribute)
jinja2.exceptions.UndefinedError: 'core.data_classes.Meal object' has no attribute 'nutrition'
```
### Analysis
**Root cause 1:** I forgot to update the field names to match the dataclass shape

---
New message after running again:

```
/Users/sebastiandorata/PycharmProjects/4020AIServer/.venv/bin/python /Users/sebastiandorata/PycharmProjects/4020AIServer/main.py 
 * Serving Flask app 'main'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5001
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: *********
127.0.0.1 - - [23/Jul/2026 13:45:04] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [23/Jul/2026 13:45:04] "GET /static/js/scripts.js HTTP/1.1" 304 -
127.0.0.1 - - [23/Jul/2026 13:45:04] "GET /static/css/styles.css HTTP/1.1" 304 -
127.0.0.1 - - [23/Jul/2026 13:45:04] "GET /static/assets/img/bg_nutrition.png HTTP/1.1" 304 -
127.0.0.1 - - [23/Jul/2026 13:45:47] "POST / HTTP/1.1" 200 -
```

### Analysis

1. Bug is gone. 
2. Remaining issue is the slow response times. I closed it myself so the duration from `13:45:04`—`13:45:47` does not represent the true response time.

---
# Debug Process

```Zsh
(.venv) sebastiandorata@Mac 4020AIServer % time curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Say hello in one word.",
  "stream": false
}'
```
Output:

```
{"model":"llama3.2","created_at":"2026-0723T17:52:58.081117794Z","response":
"Hello.","done":true,"done_reason":"stop","context":
[128006,9125,128007,271,38766,1303,33025,2696,25,6790,220,2366,18,271,128009,128006,882,128007,271,46864,24748,304,832,3492,13,128009,128006,78191,128007,271,9906,13],
"total_duration":4813960169,
"load_duration":4413876793,
"prompt_eval_count":31,
"prompt_eval_duration":236360000,
"eval_count":3,
"eval_duration":161651000}
curl http://localhost:11434/api/generate -d   0.00s user 0.01s system 0% cpu 4.835 total
```

### Analysis of the output:

* total_duration: `4.8 seconds`.
* load_duration: `4.4 seconds`.
* 91% of the total, just loading the model into memory. `load_duration / total_duration =`
  $$ \frac{4.4}{4.8} =91\% $$
   
* eval_duration (actual generation): `161ms` for `3 tokens` ~54ms per token.

1. This means the 43-second meal-plan request isn't mostly load time as it takes takes ~4.4s regardless.

2. A full day's meal plan in JSON (multiple meals, multiple foods each) could easily be 400–800 tokens.

3. Passing `"format": "json"` to force valid JSON output compounds with the token count since Constrained/schema-guided decoding in Ollama is typically noticeably slower per token than free-form text.

Next Step: Find generation length
---

```Zsh
(.venv) sebastiandorata@Mac 4020AIServer % time curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Create a one-day meal plan totaling 2000 calories, 150g protein, 200g carbs, 60g fat. Choose from common foods. Respond with ONLY valid JSON: {\"meal_plan\": [{\"meal_name\": \"Breakfast\", \"foods\": [{\"food\": \"chicken breast\", \"grams\": 150}]}]}",
  "format": "json",
  "stream": false
}'
```

Output:

```json
{
  "model":"llama3.2",
  "created_at":"2026-07-23T18:23:53.39070175Z",
  "response":
  "{
  "meal_plan": [
    {
      "meal_name": "Breakfast",
      "foods": [
        {
          "food": "scrambled eggs",
          "grams": 240
        },
        {
          "food": "whole wheat toast",
          "grams": 40
        },
        {
          "food": "fresh berries",
          "grams": 60
        }
      ]
    },
    {
      "meal_name": "Lunch",
      "foods": [
        {
          "food": "grilled chicken breast",
          "grams": 120
        },
        {
          "food": "quinoa",
          "grams": 30
        },
        {
          "food": "steamed broccoli",
          "grams": 50
        }
      ]
    },
    {
      "meal_name": "Snack",
      "foods": [
        {
          "food": "Greek yogurt",
          "grams": 100
        },
        {
          "food": "almonds",
          "grams": 20
        }
      ]
    },
    {
      "meal_name": "Dinner",
      "foods": [
        {
          "food": "baked salmon",
          "grams": 150
        },
        {
          "food": "sweet potato",
          "grams": 40
        },
        {
          "food": "green beans",
          "grams": 30
        }
      ]
    }
  ]
}"
  ,
  "done":true,
  "done_reason":"stop",
  "context":[128006,9125,128007,271,38766,1303,33025,2696,25,6790,220,2366,18,271,128009,128006,882,128007,271,4110,264,832,11477,15496,3197,82223,220,1049,15,25247,11,220,3965,70,13128,11,220,1049,70,53609,11,220,1399,70,8834,13,22991,505,4279,15657,13,40633,449,27785,2764,4823,25,5324,42880,27662,794,62853,42880,1292,794,330,23340,9533,498,330,96420,794,62853,14239,794,330,331,9890,17659,498,330,51870,794,220,3965,92,14316,14316,128009,128006,78191,128007,271,5018,42880,27662,794,62853,42880,1292,794,330,23340,9533,498,330,96420,794,62853,14239,794,330,2445,2453,38759,19335,498,330,51870,794,220,8273,2186,5324,14239,794,330,67733,34153,23211,498,330,51870,794,220,1272,2186,5324,14239,794,330,72408,63494,498,330,51870,794,220,1399,26516,2186,5324,42880,1292,794,330,43,3265,498,330,96420,794,62853,14239,794,330,911,4473,16553,17659,498,330,51870,794,220,4364,2186,5324,14239,794,330,447,80094,498,330,51870,794,220,966,2186,5324,14239,794,330,5455,3690,79276,498,330,51870,794,220,1135,26516,2186,5324,42880,1292,794,330,21380,474,498,330,96420,794,62853,14239,794,330,95448,55575,498,330,51870,794,220,1041,2186,5324,14239,794,330,278,55720,498,330,51870,794,220,508,26516,2186,5324,42880,1292,794,330,35,4481,498,330,96420,794,62853,14239,794,330,65,7897,41420,498,330,51870,794,220,3965,2186,5324,14239,794,330,95928,39834,498,330,51870,794,220,1272,2186,5324,14239,794,330,13553,27994,498,330,51870,794,220,966,92,14316,14316],
  "total_duration":16239882006,
  "load_duration":4371100168,
  "prompt_eval_count":94,
  "prompt_eval_duration":745509000,
  "eval_count":204,"eval_duration":11121244000
}
  curl http://localhost:11434/api/generate -d   0.00s user 0.01s system 0% cpu 16.263 total
```

* total_duration: `16.2 seconds`.
* load_duration: `4.3 seconds`.
* prompt_eval_duration: `74ms`
* eval_duration (actual generation): `11.12 seconds` for `204 tokens generated` ~54ms per token.

$$ \text{Time Per Token} = \frac{\text{eval\_duration}}{\text{tokens generated}} = \frac{11.12\text{ s}}{204} = 0.05451\text{ seconds} $$

* **Tokens Per Second (Throughput)**: **18.35 t/s**
$$ \text{Tokens Per Second} = \frac{\text{tokens generated}}{\text{eval\_duration}} = \frac{204}{11.12\text{ s}} = 18.35\frac{t}{s}  $$


Therefore Ollama itself when called directly is not the bottleneck. It's fast and consistent with ~54ms/token, load cost is fixed overhead.

---
Root cause <u>*theory*</u>: There is something in the Flask/Python layer between receiving the POST and rendering result.html that is adding half a minute.


* After searching through the code, I noticed unindexed, case-folded lookups against the food database, run in a loop in the file  `ollama_provider.py` `in _resolve_food`

```python
    @staticmethod
    def _resolve_food(food_name: str) -> Optional[Food]:
        """Same two-step lookup as SampleMealPlanProvider: curated alias
        first, then exact name match as a fallback."""
        normalized = food_name.strip().lower()

        alias = db.session.execute(
            db.select(FoodAlias).where(
                db.func.lower(FoodAlias.search_term) == normalized
            )
        ).scalar_one_or_none()

        if alias:
            return db.session.get(Food, alias.food_id)

        return db.session.execute(
            db.select(Food).where(
                db.func.lower(Food.food_name) == normalized
            )
        ).scalar_one_or_none()

```

Two problems compound here:

1. `db.func.lower(...)`on the column prevents SQLite from using any index on `search_term` or `food_name`, even if one exists. Every call becomes a full table scan, computing `LOWER()` on every row.
2. This runs once or twice per food item, in a loop, synchronously. When reviewing `_build_meal_plan_result`, a 4-meal plan with ~3 foods each means up to ~24 sequential full-table-scan queries 12 foods × up to 2 queries each result in alias' miss falls through to the Food table scan.

This is because we’re using USDA MyFoodData with thousands of rows *Which I forgot to factor in*.

3. `docker-compose.yml` bind-mounts ./instance:/app/instance for the sqlite file. On macOS (Which I’m using), Docker Desktop's bind-mounted volumes (osxfs/gRPC-FUSE) have historically added significant per-I/O latency compared to a native volume<sup>1 & 2</sup>
   
---
### Theory Testing:

1. Add timestamps around just the `build_meal_plan_result` call in `generate_meal_plan`:

```python
import time
t0 = time.perf_counter()
raw = json.loads(response.json()["response"])
t1 = time.perf_counter()
result = self._build_meal_plan_result(raw)
t2 = time.perf_counter()
print(f"JSON parse: {t1-t0:.2f}s | DB resolution: {t2-t1:.2f}s")
```

- Integrated:

```python
def build_meal_plan_result(self, raw: dict) -> MealPlanResult:
    """Same resolution + totalling logic as SampleMealPlanProvider: look each
    AI-suggested food up via the alias table, then exact-match fallback, and
    compute real calories/macros from the per-100g values in the database."""
    t_start = time.perf_counter()
    db_time = 0.0  # running total spent inside resolve_food

    meals: List[Meal] = []
    total_calories = total_protein = total_carbs = total_fat = 0.0

    for meal_data in raw["meal_plan"]:
        items: List[MealPlanItem] = []
        meal_calories = meal_protein = meal_carbs = meal_fat = 0.0

        for entry in meal_data["foods"]:
            t0 = time.perf_counter()
            food = self.resolve_food(entry["food"])
            db_time += time.perf_counter() - t0

            if not food:
                continue  # AI suggested something not in the catalog — skip it

            multiplier = entry["grams"] / 100
            calories = round(food.calories * multiplier, 2)
            protein = round(food.protein * multiplier, 2)
            carbs = round(food.carbs * multiplier, 2)
            fat = round(food.fat * multiplier, 2)

            items.append(MealPlanItem(
                food_name=entry["food"].title(),
                portion_grams=entry["grams"],
                calories=calories,
                protein_g=protein,
                carbs_g=carbs,
                fat_g=fat,
            ))

            meal_calories += calories
            meal_protein += protein
            meal_carbs += carbs
            meal_fat += fat

        meals.append(Meal(
            meal_name=meal_data["meal_name"],
            items=items,
            total_calories=round(meal_calories, 2),
            total_protein_g=round(meal_protein, 2),
            total_carbs_g=round(meal_carbs, 2),
            total_fat_g=round(meal_fat, 2),
        ))

        total_calories += meal_calories
        total_protein += meal_protein
        total_carbs += meal_carbs
        total_fat += meal_fat

    total_time = time.perf_counter() - t_start
    print(f"[TIMING] build_meal_plan_result total: {total_time:.2f}s | "
          f"DB resolution (sum of resolve_food calls): {db_time:.2f}s | "
          f"other work: {total_time - db_time:.2f}s")

    return MealPlanResult(
        meals=meals,
        total_calories=round(total_calories, 2),
        total_protein_g=round(total_protein, 2),
        total_carbs_g=round(total_carbs, 2),
        total_fat_g=round(total_fat, 2),
    )

```

Console output:

```
/Users/sebastiandorata/PycharmProjects/4020AIServer/.venv/bin/python /Users/sebastiandorata/PycharmProjects/4020AIServer/main.py 
 * Serving Flask app 'main'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5001
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: **************
127.0.0.1 - - [23/Jul/2026 15:30:24] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [23/Jul/2026 15:30:24] "GET /static/js/scripts.js HTTP/1.1" 304 -
127.0.0.1 - - [23/Jul/2026 15:30:24] "GET /static/css/styles.css HTTP/1.1" 304 -
127.0.0.1 - - [23/Jul/2026 15:30:24] "GET /static/assets/img/bg_nutrition.png HTTP/1.1" 304 -
[TIMING] build_meal_plan_result total: 0.02s | DB resolution (sum of resolve_food calls): 0.02s | other work: 0.00s
127.0.0.1 - - [23/Jul/2026 15:31:00] "POST / HTTP/1.1" 200 -
127.0.0.1 - - [23/Jul/2026 15:31:00] "GET /static/css/styles.css HTTP/1.1" 304 -
127.0.0.1 - - [23/Jul/2026 15:31:00] "GET /static/js/charts.js HTTP/1.1" 200 -
127.0.0.1 - - [23/Jul/2026 15:31:00] "GET /static/js/scripts.js HTTP/1.1" 304 -
127.0.0.1 - - [23/Jul/2026 15:31:00] "GET /static/assets/img/bg_nutrition.png HTTP/1.1" 304 -
```
### Food-lookup queries are not the problem.

2. Check generate_meal_plan

```python
def generate_meal_plan(
    self, target: MacroTarget, available_foods: List[FoodItem]
) -> MealPlanResult:
    prompt = self._build_prompt(target, available_foods)

    t0 = time.perf_counter()
    response = requests.post(
        f"{self.host}/api/generate",
        json={
            "model": self.model,
            "prompt": prompt,
            "format": "json",
            "stream": False,
        },
        timeout=60,
    )
    response.raise_for_status()
    t1 = time.perf_counter()

    raw = json.loads(response.json()["response"])
    t2 = time.perf_counter()

    result = self_build_meal_plan_result(raw)
    t3 = time.perf_counter()

    print(f"[TIMING] Ollama request: {t1-t0:.2f}s | JSON parse: {t2-t1:.2f}s | "
          f"build_meal_plan_result: {t3-t2:.2f}s | TOTAL: {t3-t0:.2f}s")

    return result

```

Output: 

```
127.0.0.1 - - [23/Jul/2026 15:36:35] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [23/Jul/2026 15:36:35] "GET /static/css/styles.css HTTP/1.1" 304 -
127.0.0.1 - - [23/Jul/2026 15:36:35] "GET /static/js/scripts.js HTTP/1.1" 304 -
127.0.0.1 - - [23/Jul/2026 15:36:35] "GET /static/assets/img/bg_nutrition.png HTTP/1.1" 304 -
[TIMING] build_meal_plan_result total: 0.03s | DB resolution (sum of resolve_food calls): 0.03s | other work: 0.00s
[TIMING] Ollama request: 28.47s | JSON parse: 0.00s | build_meal_plan_result: 0.03s | TOTAL: 28.50s
127.0.0.1 - - [23/Jul/2026 15:37:09] "POST / HTTP/1.1" 200 -
127.0.0.1 - - [23/Jul/2026 15:37:09] "GET /static/css/styles.css HTTP/1.1" 304 -
127.0.0.1 - - [23/Jul/2026 15:37:09] "GET /static/js/scripts.js HTTP/1.1" 304 -
127.0.0.1 - - [23/Jul/2026 15:37:09] "GET /static/js/charts.js HTTP/1.1" 304 -
127.0.0.1 - - [23/Jul/2026 15:37:09] "GET /static/assets/img/bg_nutrition.png HTTP/1.1" 304 -
```

# Root Cause:

The bottleneck is Ollama generation.
One useful thing this also reveals is that the raw curl test for the same kind of prompt was 16.26s, but Flask's actual call was 28.47s.



## Speed Optimizations Applied

Following the root-cause finding above (Ollama generation itself was the bottleneck,
not Flask or the DB), three targeted changes were made to `ollama_provider.py`:

1. **`"keep_alive": "30m"`** — keeps the model resident in memory between requests
   instead of letting Ollama unload it after its default idle timeout. Avoids paying
   the ~4.4s model load cost again on subsequent requests during a demo/testing session.

2. **`"options": {"num_predict": 400, "num_ctx": 1024}`** — `num_predict` caps the
   maximum number of tokens the model can generate per request (our real output has
   been ~200 tokens for a full 3-meal plan, so 400 gives headroom without risking a
   run-on generation). `num_ctx` shrinks the context window from Ollama's 2048-token
   default to 1024, since our prompt + response comfortably fits well under that,
   reducing per-request allocation overhead.

3. **Tightened prompt constraints** — `_build_prompt()` now explicitly states
   "exactly 3 meals: Breakfast, Lunch, and Dinner" and "2 to 3 foods only" per meal.
   This bounds the output shape, meaning fewer tokens the model has to generate and
   more predictable, parseable JSON.

**Scope:** all three changes are isolated to `ollama_provider.py` — no changes to
`routes.py`, templates, or the DB layer, so this was tested independently of other
in-progress work.

**Results:**

| Run                         | Ollama request time | Notes                                                      |
|-----------------------------|---------------------|------------------------------------------------------------|
| Baseline (before changes)   | 28.47s              | Cold-ish, no `keep_alive`, default `num_predict`/`num_ctx` |
| After optimization, 1st run | 19.77s              | ~31% faster                                                |
| After optimization, 2nd run | 18.12s              | Model already warm via `keep_alive`                        |

**Takeaway:** Bounding generation length and tightening
the prompt shape; `keep_alive` gives an additional, consistent benefit across repeated
requests (e.g. during a live demo), since the model doesn't reload between them.

---

## References


* <sup>1</sup>https://blog.stackademic.com/my-docker-bind-mount-made-npm-install-take-47-minutes-the-vm-was-fine-c0718f513603
* <sup>2</sup>https://www.cncf.io/blog/2023/02/02/docker-on-macos-is-slow-and-how-to-fix-it/


---

